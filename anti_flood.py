# -*- coding: utf-8 -*-
import time
from collections import deque
from typing import Dict, Optional, Tuple


class AntiFloodMixin:
    """防刷屏检测模块。按 (群号, 用户ID) 追踪消息时间戳，超限自动禁言+可选撤回。

    性能：
    - _check_anti_flood 逆向单次遍历（最新→最旧），越过 3600s 立即 break，O(命中范围) 而非 O(队列长)
    - 所有限速设为 0 时直接跳过，零运行时开销
    - 每 5 分钟回收超过 2h 的过期条目，各组/用户队列上限 200 条
    特性：
    - 三档独立速率：每秒 / 每分钟 / 每小时，单档设为 0 即关闭
    - 所有消息类型均计入（文本/图片/转发/QQ收藏/JSON/App）
    - 管理员完全豁免（在 moderation.py 管线中提前 return）
    """

    def _init_anti_flood(self):
        self._anti_flood_data: Dict[str, Dict[str, deque]] = {}
        self._anti_flood_last_cleanup = 0.0

    def _record_message(self, group_id: str, user_id: str, msg_id: str):
        if group_id not in self._anti_flood_data:
            self._anti_flood_data[group_id] = {}
        if user_id not in self._anti_flood_data[group_id]:
            self._anti_flood_data[group_id][user_id] = deque(maxlen=200)
        self._anti_flood_data[group_id][user_id].append((time.time(), msg_id))

    def _get_rate_limit(self, key: str, default: int) -> int:
        return self._safe_int(self.config.get(key, default), default)

    def _check_anti_flood(self, group_id: str, user_id: str) -> Tuple[bool, Optional[dict]]:
        """按 每秒→每分钟→每小时 检测，任一档位触发即返回。逆向单次遍历 O(命中范围)。"""
        data = self._anti_flood_data
        if group_id not in data or user_id not in data[group_id]:
            return False, None

        dq = data[group_id][user_id]
        total_msgs = len(dq)
        now = time.time()

        sec_limit = self._get_rate_limit("anti_flood_rate_per_second", 5)
        min_limit = self._get_rate_limit("anti_flood_rate_per_minute", 20)
        hour_limit = self._get_rate_limit("anti_flood_rate_per_hour", 60)
        if sec_limit <= 0 and min_limit <= 0 and hour_limit <= 0:
            return False, None

        sec_count = 0
        min_count = 0
        hour_count = 0
        sec_ids = []
        min_ids = []
        hour_ids = []

        for t, mid in reversed(dq):
            dt = now - t
            if dt >= 3600:
                break
            hour_count += 1
            hour_ids.append(mid)
            if dt < 60:
                min_count += 1
                min_ids.append(mid)
            if dt < 1:
                sec_count += 1
                sec_ids.append(mid)

        if sec_limit > 0 and sec_count > sec_limit:
            return True, {"rate": "每秒", "count": sec_count, "limit": sec_limit,
                          "total_msgs": total_msgs, "msg_ids": sec_ids}
        if min_limit > 0 and min_count > min_limit:
            return True, {"rate": "每分钟", "count": min_count, "limit": min_limit,
                          "total_msgs": total_msgs, "msg_ids": min_ids}
        if hour_limit > 0 and hour_count > hour_limit:
            return True, {"rate": "每小时", "count": hour_count, "limit": hour_limit,
                          "total_msgs": total_msgs, "msg_ids": hour_ids}
        return False, None

    def _anti_flood_cleanup(self):
        now = time.time()
        if now - self._anti_flood_last_cleanup < 300:
            return
        self._anti_flood_last_cleanup = now
        expired = now - 7200
        for gid, users in list(self._anti_flood_data.items()):
            for uid in list(users.keys()):
                dq = users[uid]
                while dq and dq[0][0] < expired:
                    dq.popleft()
                if not dq:
                    del users[uid]
            if not users:
                del self._anti_flood_data[gid]

    def _get_anti_flood_status(self) -> dict:
        """返回当前防刷屏追踪快照，供 WebUI 仪表盘 API 使用。逆向单次遍历。"""
        result = {
            "enabled": self._cfg("anti_flood_enabled", True),
            "tracked_groups": 0,
            "tracked_users": 0,
            "groups": {},
        }
        if not self._anti_flood_data:
            return result
        now = time.time()
        total_users = 0
        for gid, users in self._anti_flood_data.items():
            group_users = {}
            for uid, dq in users.items():
                total_msgs = len(dq)
                if total_msgs == 0:
                    continue
                total_users += 1
                s = m = h = 0
                for t, _mid in reversed(dq):
                    dt = now - t
                    if dt >= 3600:
                        break
                    h += 1
                    if dt < 60:
                        m += 1
                    if dt < 1:
                        s += 1
                group_users[uid] = {
                    "total_msgs": total_msgs,
                    "per_second": s,
                    "per_minute": m,
                    "per_hour": h,
                }
            if group_users:
                result["groups"][gid] = {"users": group_users}
        result["tracked_groups"] = len(result["groups"])
        result["tracked_users"] = total_users
        return result
