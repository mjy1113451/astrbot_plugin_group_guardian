# -*- coding: utf-8 -*-
"""Aho-Corasick 自动机封装，替换词库关键词的正则匹配。"""

from typing import List, Optional, Tuple

try:
    import ahocorasick
except ImportError:
    ahocorasick = None


class KeywordAutomaton:
    """AC 自动机：构建 Trie + fail 指针，一次扫描命中所有关键词。"""

    def __init__(self):
        self._auto = None  # ahocorasick.Automaton
        self._count = 0    # 关键词数量
        self._built = False

    def add_keywords(self, keywords: List[str]) -> None:
        """批量添加关键词，自动跳过空值和重复。"""
        if ahocorasick is None:
            return
        if self._auto is None:
            self._auto = ahocorasick.Automaton()
        seen = set()
        for kw in keywords:
            kw = kw.strip().lower()
            if not kw or kw in seen:
                continue
            seen.add(kw)
            self._auto.add_word(kw, kw)
            self._count += 1

    def build(self) -> None:
        """构建 fail 指针，调用后不可再添加关键词。"""
        if self._auto is not None and not self._built:
            self._auto.make_automaton()
            self._built = True

    def exists(self, text: str) -> bool:
        """检查文本中是否包含任意关键词。"""
        if not self._built or self._auto is None:
            return False
        text_lower = text.lower()
        try:
            next(self._auto.iter(text_lower))
            return True
        except StopIteration:
            return False

    def iter_matches(self, text: str) -> List[Tuple[int, str]]:
        """返回所有匹配：[(end_pos, keyword), ...]，按 end_pos 升序。"""
        if not self._built or self._auto is None:
            return []
        text_lower = text.lower()
        try:
            return list(self._auto.iter(text_lower))
        except StopIteration:
            return []

    @property
    def count(self) -> int:
        return self._count

    @property
    def available(self) -> bool:
        return ahocorasick is not None
