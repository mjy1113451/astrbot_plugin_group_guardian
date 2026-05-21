# AstrBot 插件 WebUI 设置页 UI 模板

> 生成日期：2026-05-22
> 适用文件：`pages/dashboard/index.html`
> 包含：3种风格的免责声明卡片 + 长消息展开功能

---

## 📋 使用说明

### 第一部分：免责声明卡片替换

将现有 `#disclaimerCard` 区域（原第352-367行）替换为对应模板的HTML代码。

### 第二部分：长消息展开功能

将以下内容**添加到** `<style>` 标签内，并修改 `loadLogs` 函数中的消息单元格渲染逻辑。

---

# ═══════════════════════════════════════════
# 模板 A：Cloudflare 企业风
# ═══════════════════════════════════════════

## 设计理念

参考 Cloudflare Dashboard / WAF 管理面板的设计语言：
- 信息密度适中，清晰的视觉层级
- 左侧竖线色条标识状态（绿=已同意，橙=未同意）
- 底部带信息提示条（蓝色背景提示框）
- 按钮/链接使用实心填充风格
- 整体偏正式、专业、可信赖感

## A1 - CSS 样式

```css
/* Template A: Cloudflare Enterprise Style */

/* 免责声明卡片 - Cloudflare 风格 */
.cf-disclaimer-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  margin-bottom: 16px;
  overflow: hidden;
  border: 1px solid var(--border);
  position: relative;
  transition: border-color .2s, box-shadow .2s;
}

.cf-disclaimer-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--warning);
  transition: background .2s;
}

.cf-disclaimer-card.agreed::before {
  background: var(--success);
}

.cf-disclaimer-card:hover {
  box-shadow: var(--shadow-lg);
}

.cf-disclaimer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: #fafbfc;
}

.cf-disclaimer-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cf-status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .3px;
}

.cf-status-indicator.pending {
  background: var(--warning-light);
  color: var(--warning);
  border: 1px solid rgba(230, 162, 60, .3);
}

.cf-status-indicator.approved {
  background: var(--success-light);
  color: var(--success);
  border: 1px solid rgba(103, 194, 58, .3);
}

.cf-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: cf-pulse 2s infinite;
}

@keyframes cf-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: .6; transform: scale(0.9); }
}

.cf-status-indicator.approved .cf-status-dot {
  animation: none;
}

.cf-disclaimer-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.cf-disclaimer-body {
  padding: 20px;
}

.cf-disclaimer-desc {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.cf-disclaimer-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.cf-btn-read {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all .15s;
}

.cf-btn-read:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(64, 158, 255, .3);
}

.cf-btn-read svg {
  width: 14px;
  height: 14px;
  fill: currentColor;
}

.cf-toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cf-toggle-label {
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
  transition: color .15s;
}

.cf-toggle-label:hover {
  color: var(--text-primary);
}

/* Cloudflare 风格的 Toggle 开关 */
.cf-toggle {
  position: relative;
  width: 44px;
  height: 24px;
  flex-shrink: 0;
}

.cf-toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.cf-toggle-slider {
  position: absolute;
  inset: 0;
  background: #dcdfe6;
  border-radius: 24px;
  transition: all .25s cubic-bezier(.4, 0, .2, 1);
  cursor: pointer;
}

.cf-toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  left: 3px;
  bottom: 3px;
  background: #fff;
  border-radius: 50%;
  transition: all .25s cubic-bezier(.4, 0, .2, 1);
  box-shadow: 0 1px 3px rgba(0,0,0,.15);
}

.cf-toggle input:checked + .cf-toggle-slider {
  background: var(--success);
}

.cf-toggle input:checked + .cf-toggle-slider::before {
  transform: translateX(20px);
}

/* 底部信息提示条 - Cloudflare 风格 */
.cf-info-bar {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  background: #e8f4fd;
  border-top: 1px solid #bee3f8;
  font-size: 12px;
  line-height: 1.6;
  color: #2c5282;
}

.cf-info-icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-top: 1px;
  fill: #3182ce;
}

.cf-info-text a {
  color: #2b6cb0;
  text-decoration: underline;
  font-weight: 500;
}

.cf-info-text a:hover {
  color: #2c5282;
}

/* 消息展开功能 - Cloudflare 风格 */
.cf-msg-cell {
  max-width: 200px;
  position: relative;
  cursor: pointer;
  transition: background .15s;
}

.cf-msg-cell:hover {
  background: rgba(64, 158, 255, .06);
}

.cf-msg-content {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cf-msg-expandable {
  white-space: normal;
  word-break: break-all;
  max-width: 400px;
}

.cf-msg-expand-btn {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  margin-left: 4px;
  color: var(--primary);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
  opacity: .8;
  transition: opacity .15s;
}

.cf-msg-expand-btn:hover {
  opacity: 1;
}

.cf-msg-expand-btn svg {
  width: 10px;
  height: 10px;
  fill: currentColor;
  transition: transform .2s;
}

.cf-msg-expand-btn.expanded svg {
  transform: rotate(180deg);
}
```

## A2 - HTML 结构（替换 #disclaimerCard）

```html
<!-- Template A: Cloudflare Enterprise Style - Disclaimer Card -->
<div class="cf-disclaimer-card" id="disclaimerCard">
  <div class="cf-disclaimer-header">
    <div class="cf-disclaimer-header-left">
      <h2 class="cf-disclaimer-title">免责声明</h2>
      <span class="cf-status-indicator pending" id="cfStatusBadge">
        <span class="cf-status-dot"></span>
        <span id="cfStatusText">待同意</span>
      </span>
    </div>
  </div>

  <div class="cf-disclaimer-body">
    <div class="cf-disclaimer-desc">
      使用本插件前，您必须阅读并同意免责声明。未同意前，插件的所有功能（审核、群管、LLM工具等）将不会生效。
    </div>

    <div class="cf-disclaimer-actions">
      <a href="javascript:void(0)" id="openDisclaimer" class="cf-btn-read">
        <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
        阅读免责声明
      </a>

      <div class="cf-toggle-wrapper">
        <label class="cf-toggle">
          <input type="checkbox" data-key="disclaimerAgreed" id="disclaimerAgreed" />
          <span class="cf-toggle-slider"></span>
        </label>
        <span class="cf-toggle-label" id="disclaimerLabel">我已阅读并同意</span>
      </div>
    </div>
  </div>

  <div class="cf-info-bar">
    <svg class="cf-info-icon" viewBox="0 0 24 24"><path d="M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
    <div class="cf-info-text">
      同意即表示您已充分了解本插件的使用风险、数据处理方式及责任限制条款。<a href="javascript:void(0)" id="openDisclaimer">查看完整声明 →</a>
    </div>
  </div>
</div>
```

## A3 - JavaScript 逻辑

```javascript
/* Template A: Cloudflare Style JS */

// 更新免责声明卡片状态 (Cloudflare 风格)
function updateCFDisclaimerStatus(agreed) {
  var card = document.getElementById('disclaimerCard');
  var badge = document.getElementById('cfStatusBadge');
  var statusText = document.getElementById('cfStatusText');
  var label = document.getElementById('disclaimerLabel');

  if (!card || !badge) return;

  if (agreed) {
    card.classList.add('agreed');
    card.classList.remove('not-agreed');
    badge.classList.remove('pending');
    badge.classList.add('approved');
    statusText.textContent = '已生效';
    label.textContent = '已同意免责声明';
  } else {
    card.classList.remove('agreed');
    card.classList.add('not-agreed');
    badge.classList.remove('approved');
    badge.classList.add('pending');
    statusText.textContent = '待同意';
    label.textContent = '我已阅读并同意';
  }
}

// 在 loadSettings 函数中调用:
// updateCFDisclaimerStatus(CONFIG.disclaimer_agreed ? true : false);

// 监听复选框变化
document.getElementById('disclaimerAgreed').addEventListener('change', function() {
  updateCFDisclaimerStatus(this.checked);
});

// ========== 长消息展开功能 (Cloudflare 风格) ==========

function renderExpandableMessage(msgPreview) {
  if (!msgPreview) return '';
  var escaped = esc(msgPreview);
  var isLong = msgPreview.length > 30;

  if (!isLong) {
    return '<span class="cf-msg-content">' + escaped + '</span>';
  }

  return '<span class="cf-msg-cell" data-full-msg="' + escaped.replace(/"/g, '&quot;') + '">' +
    '<span class="cf-msg-content">' + escaped.slice(0, 30) + '</span>' +
    '<span class="cf-msg-expand-btn">' +
      '<svg viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>' +
      '展开' +
    '</span>' +
  '</span>';
}

// 在 loadLogs 函数中，将原来的消息单元格渲染：
// 原代码: '<td class="msg-cell" title="' + esc(l.msg_preview) + '">' + esc(l.msg_preview) + '</td>'
// 替换为: '<td>' + renderExpandableMessage(l.msg_preview) + '</td>'

// 绑定展开/收起事件
function initMsgExpand() {
  document.querySelectorAll('.cf-msg-expand-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var cell = this.closest('.cf-msg-cell');
      var content = cell.querySelector('.cf-msg-content');
      var fullMsg = cell.getAttribute('data-full-msg');

      if (this.classList.contains('expanded')) {
        // 收起
        this.classList.remove('expanded');
        this.querySelector('svg + *') || (this.innerHTML = '<svg viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>展开');
        content.classList.remove('cf-msg-expandable');
        content.textContent = fullMsg.slice(0, 30);
      } else {
        // 展开
        this.classList.add('expanded');
        this.innerHTML = '<svg viewBox="0 0 24 24"><path d="M7.41 16.59L12 12l4.59 4.58L18 18l-6-6-6 6 1.41-1.41z"/></svg>收起';
        content.classList.add('cf-msg-expandable');
        content.textContent = fullMsg;
      }
    });
  });
}

// 在 loadLogs 函数末尾调用: initMsgExpand();
```

---

# ═══════════════════════════════════════════
# 模板 B：Linear/Vercel 简约风
# ═══════════════════════════════════════════

## 设计理念

极简主义设计语言，参考 Linear.app / Vercel Dashboard：
- 大量留白，呼吸感强
- 细线条边框，无填充背景的状态指示
- 微妙的 hover 动效（0.15s ease）
- 小圆点 + 文字状态标签代替粗边框
- 干净、克制、高级感
- 单色调为主，强调功能性

## B1 - CSS 样式

```css
/* Template B: Linear/Vercel Minimalist Style */

/* 免责声明卡片 - Linear/Vercel 风格 */
.lin-disclaimer-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px 28px;
  margin-bottom: 16px;
  transition: border-color .2s ease, box-shadow .2s ease;
  position: relative;
}

.lin-disclaimer-card:hover {
  border-color: #c8ccd0;
  box-shadow: 0 1px 6px rgba(0,0,0,.04);
}

.lin-disclaimer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.lin-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.lin-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -.2px;
  margin: 0;
}

/* 极简状态指示器 - 小圆点 + 文字 */
.lin-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  padding: 3px 0;
}

.lin-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.lin-status-dot.pending { background: var(--warning); }
.lin-status-dot.approved { background: var(--success); }

.lin-status-text.pending { color: var(--warning); }
.lin-status-text.approved { color: var(--success); }

.lin-disclaimer-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.lin-description {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  max-width: 520px;
}

.lin-actions-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 极简链接风格 */
.lin-link-read {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  font-weight: 500;
  color: var(--primary);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color .15s;
  padding-bottom: 1px;
}

.lin-link-read:hover {
  border-bottom-color: var(--primary);
}

.lin-link-read svg {
  width: 13px;
  height: 13px;
  fill: currentColor;
  opacity: .7;
}

/* 极简 Toggle - 更细更轻 */
.lin-toggle-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.lin-toggle {
  position: relative;
  width: 36px;
  height: 20px;
  flex-shrink: 0;
}

.lin-toggle input { opacity: 0; width: 0; height: 0; }

.lin-toggle-track {
  position: absolute;
  inset: 0;
  background: #e2e4e8;
  border-radius: 20px;
  transition: background .2s ease;
  cursor: pointer;
}

.lin-toggle-track::after {
  content: '';
  position: absolute;
  width: 14px;
  height: 14px;
  left: 3px;
  top: 3px;
  background: #fff;
  border-radius: 50%;
  transition: transform .2s cubic-bezier(.4, 0, .2, 1);
  box-shadow: 0 1px 2px rgba(0,0,0,.1);
}

.lin-toggle input:checked + .lin-toggle-track {
  background: var(--primary);
}

.lin-toggle input:checked + .lin-toggle-track::after {
  transform: translateX(16px);
}

.lin-toggle-caption {
  font-size: 12px;
  color: var(--text-muted);
  user-select: none;
  cursor: pointer;
  transition: color .15s;
}

.lin-toggle-caption:hover {
  color: var(--text-secondary);
}

/* 底部提示 - 极简文字 */
.lin-hint {
  margin-top: 4px;
  font-size: 11.5px;
  color: var(--text-muted);
  line-height: 1.6;
  padding-left: 2px;
}

.lin-hint a {
  color: var(--text-secondary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.lin-hint a:hover {
  color: var(--text-primary);
}

/* 消息展开 - Linear/Vercel 风格 */
.lin-msg-cell {
  max-width: 220px;
  cursor: default;
}

.lin-msg-truncated {
  display: inline-block;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}

.lin-msg-full {
  display: block;
  white-space: pre-wrap;
  word-break: break-word;
  max-width: 380px;
  line-height: 1.55;
  font-size: 11.5px;
  color: var(--text-primary);
}

.lin-msg-action {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  margin-left: 6px;
  vertical-align: middle;
  font-size: 11px;
  color: var(--primary);
  cursor: pointer;
  user-select: none;
  opacity: .75;
  transition: opacity .15s;
  font-weight: 500;
}

.lin-msg-action:hover {
  opacity: 1;
}

.lin-msg-action svg {
  width: 9px;
  height: 9px;
  fill: currentColor;
}
```

## B2 - HTML 结构（替换 #disclaimerCard）

```html
<!-- Template B: Linear/Vercel Minimalist Style - Disclaimer Card -->
<div class="lin-disclaimer-card" id="disclaimerCard">
  <div class="lin-disclaimer-header">
    <div class="lin-header-left">
      <h2 class="lin-title">免责声明</h2>
      <span class="lin-status-badge">
        <span class="lin-status-dot pending" id="linStatusDot"></span>
        <span class="lin-status-text pending" id="linStatusText">未同意</span>
      </span>
    </div>
  </div>

  <div class="lin-disclaimer-body">
    <p class="lin-description">
      使用本插件前需阅读并同意免责声明。未同意时，审核、群管及 LLM 相关功能均不可用。
    </p>

    <div class="lin-actions-row">
      <a href="javascript:void(0)" id="openDisclaimer" class="lin-link-read">
        <svg viewBox="0 0 24 24"><path d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>
        阅读完整声明
      </a>

      <div class="lin-toggle-group">
        <label class="lin-toggle">
          <input type="checkbox" data-key="disclaimerAgreed" id="disclaimerAgreed" />
          <span class="lin-toggle-track"></span>
        </label>
        <span class="lin-toggle-caption" id="disclaimerLabel">同意</span>
      </div>
    </div>

    <p class="lin-hint">
      同意后插件功能立即生效。<a href="javascript:void(0)" id="openDisclaimer">了解详情</a>
    </p>
  </div>
</div>
```

## B3 - JavaScript 逻辑

```javascript
/* Template B: Linear/Vercel Minimalist Style JS */

function updateLinDisclaimerStatus(agreed) {
  var dot = document.getElementById('linStatusDot');
  var txt = document.getElementById('linStatusText');
  var label = document.getElementById('disclaimerLabel');

  if (!dot || !txt) return;

  dot.className = 'lin-status-dot ' + (agreed ? 'approved' : 'pending');
  txt.className = 'lin-status-text ' + (agreed ? 'approved' : 'pending');
  txt.textContent = agreed ? '已同意' : '未同意';

  if (label) label.textContent = agreed ? '已同意' : '同意';
}

// 在 loadSettings 中调用: updateLinDisclaimerStatus(CONFIG.disclaimer_agreed ? true : false);

document.getElementById('disclaimerAgreed').addEventListener('change', function() {
  updateLinDisclaimerStatus(this.checked);
});

// ========== 长消息展开功能 (Linear/Vercel 风格) ==========

function linRenderMsg(msg) {
  if (!msg) return '';
  var e = esc(msg);
  if (msg.length <= 28) return e;

  return '<span class="lin-msg-cell" data-lin-full="' + e.replace(/"/g, '&quot;') + '">' +
    '<span class="lin-msg-truncated">' + e.slice(0, 28) + '</span>' +
    '<span class="lin-msg-action">' +
      '<svg viewBox="0 0 24 24"><path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>' +
    '<span class="lin-msg-action-text">更多</span>' +
    '</span>' +
  '</span>';
}

// loadLogs 中使用: '<td>' + linRenderMsg(l.msg_preview) + '</td>'

function initLinMsgExpand() {
  document.querySelectorAll('.lin-msg-action').forEach(function(action) {
    action.addEventListener('click', function(e) {
      e.stopPropagation();
      var cell = this.closest('.lin-msg-cell');
      var truncated = cell.querySelector('.lin-msg-truncated');
      var fullText = cell.getAttribute('data-lin-full');

      if (cell.dataset.expanded === 'true') {
        // 收起
        cell.dataset.expanded = 'false';
        truncated.className = 'lin-msg-truncated';
        truncated.textContent = fullText.slice(0, 28);
        this.querySelector('.lin-msg-action-text').textContent = '更多';
        this.querySelector('svg').innerHTML = '<path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/>';
      } else {
        // 展开
        cell.dataset.expanded = 'true';
        truncated.className = 'lin-msg-full';
        truncated.textContent = fullText;
        this.querySelector('.lin-msg-action-text').textContent = '收起';
        this.querySelector('svg').innerHTML = '<path d="M12 8l-4.59 4.59L6 14l6-6 6 6-1.41 1.41z"/>';
      }
    });
  });
}

// loadLogs 末尾调用: initLinMsgExpand();
```

---

# ═══════════════════════════════════════════
# 模板 C：GitHub/Notion 实用风
# ═══════════════════════════════════════════

## 设计理念

参考 GitHub Settings 页面 / Notion 偏好设置的设计语言：
- 清晰的分段描述（标题 + 说明 + 操作区）
- 使用 badge/标签来标识状态
- 操作按钮明确（主要操作突出，次要操作弱化）
- 实用、清晰、易操作
- 信息层级分明，适合设置密集型页面

## C1 - CSS 样式

```css
/* Template C: GitHub/Notion Practical Style */

/* 免责声明卡片 - GitHub/Notion 风格 */
.gh-disclaimer-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  margin-bottom: 16px;
  overflow: hidden;
}

.gh-disclaimer-inner {
  padding: 20px 24px;
}

.gh-section-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.gh-section-info {
  flex: 1;
  min-width: 0;
}

.gh-section-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.gh-section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* GitHub 风格 Badge 状态标签 */
.gh-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 10px;
  border-radius: 2em;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .3px;
  text-transform: uppercase;
}

.gh-badge-warning {
  background: #fdf3dc;
  color: #9a6700;
  border: 1px solid #e0d4a0;
}

.gh-badge-success {
  background: #dafbe1;
  color: #1a7f37;
  border: 1px solid #a4d99e;
}

.gh-badge-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
}

.gh-section-desc {
  font-size: 13px;
  line-height: 1.65;
  color: var(--text-secondary);
  margin: 0;
}

.gh-section-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  flex-shrink: 0;
}

/* GitHub 风格按钮组 */
.gh-btn-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.gh-btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: #1f883d;
  color: #fff;
  border: 1px solid rgba(31, 136, 61, .4);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: background .15s, border-color .15s;
}

.gh-btn-primary:hover {
  background: #1a7f37;
  border-color: #1a7f37;
}

.gh-btn-primary svg {
  width: 14px;
  height: 14px;
  fill: currentColor;
}

/* GitHub 风格 Checkbox 行 */
.gh-checkbox-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #f6f8fa;
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-top: 4px;
}

.gh-checkbox-input {
  width: 16px;
  height: 16px;
  accent-color: #1f883d;
  cursor: pointer;
  flex-shrink: 0;
}

.gh-checkbox-label {
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
  user-select: none;
}

.gh-checkbox-label strong {
  font-weight: 600;
}

/* 底部说明区域 */
.gh-footer-note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-top: 14px;
  padding: 12px 14px;
  background: #f1f8ff;
  border-left: 3px solid #0366d6;
  border-radius: 0 6px 6px 0;
  font-size: 12px;
  line-height: 1.6;
  color: #0366d6;
}

.gh-footer-note-icon {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  fill: currentColor;
  margin-top: 1px;
}

.gh-footer-note a {
  color: #0366d6;
  font-weight: 600;
  text-decoration: none;
}

.gh-footer-note a:hover {
  text-decoration: underline;
}

/* 消息展开 - GitHub 风格 */
.gh-msg-cell {
  max-width: 200px;
}

.gh-msg-preview {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 180px;
  cursor: pointer;
  color: var(--text-primary);
  transition: color .15s;
}

.gh-msg-preview:hover {
  color: var(--primary);
}

.gh-msg-expanded {
  display: block;
  white-space: pre-wrap;
  word-break: break-all;
  max-width: 400px;
  font-size: 11.5px;
  line-height: 1.5;
  color: var(--text-primary);
  background: #f6f8fa;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid #e1e4e8;
  margin-top: 2px;
}

.gh-msg-toggle {
  display: inline-block;
  font-size: 10px;
  color: var(--primary);
  cursor: pointer;
  margin-left: 4px;
  font-weight: 500;
  user-select: none;
  vertical-align: middle;
}

.gh-msg-toggle:hover {
  text-decoration: underline;
}
```

## C2 - HTML 结构（替换 #disclaimerCard）

```html
<!-- Template C: GitHub/Notion Practical Style - Disclaimer Card -->
<div class="gh-disclaimer-card" id="disclaimerCard">
  <div class="gh-disclaimer-inner">

    <!-- 标题区：标题 + Badge + 描述 -->
    <div class="gh-section-header">
      <div class="gh-section-info">
        <div class="gh-section-title-row">
          <h2 class="gh-section-title">免责声明</h2>
          <span class="gh-badge gh-badge-warning" id="ghStatusBadge">
            <span class="gh-badge-dot"></span>
            <span id="ghStatusText">Required</span>
          </span>
        </div>
        <p class="gh-section-desc">
          使用本插件前必须同意免责声明。未同意时，所有功能（消息审核、群管理、AI 工具等）将被禁用。
        </p>
      </div>

      <div class="gh-section-actions">
        <div class="gh-btn-group">
          <a href="javascript:void(0)" id="openDisclaimer" class="gh-btn-primary">
            <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm4 18H6V4h7v5h5v11zM8 15h8v2H8zm0-4h8v2H8z"/></svg>
            View full statement
          </a>
        </div>
      </div>
    </div>

    <!-- 操作区：Checkbox -->
    <div class="gh-checkbox-row">
      <input type="checkbox" data-key="disclaimerAgreed" id="disclaimerAgreed" class="gh-checkbox-input" />
      <label for="disclaimerAgreed" class="gh-checkbox-label" id="disclaimerLabel">
        <strong>I have read and agree to the disclaimer</strong>
      </label>
    </div>

    <!-- 底部提示条 -->
    <div class="gh-footer-note">
      <svg class="gh-footer-note-icon" viewBox="0 0 24 24"><path d="M11 17h2v-6h-2v6zm1-15C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zM11 9h2V7h-2v2z"/></svg>
      <span>
        By agreeing, you acknowledge that you understand the risks, data handling policies, and liability limitations.
        <a href="javascript:void(0)" id="openDisclaimer">Read more →</a>
      </span>
    </div>

  </div>
</div>
```

## C3 - JavaScript 逻辑

```javascript
/* Template C: GitHub/Notion Practical Style JS */

function updateGHDisclaimerStatus(agreed) {
  var badge = document.getElementById('ghStatusBadge');
  var statusText = document.getElementById('ghStatusText');
  var label = document.getElementById('disclaimerLabel');

  if (!badge || !statusText) return;

  if (agreed) {
    badge.className = 'gh-badge gh-badge-success';
    statusText.textContent = 'Active';
    if (label) label.innerHTML = '<strong>I have read and agree to the disclaimer</strong> ✓';
  } else {
    badge.className = 'gh-badge gh-badge-warning';
    statusText.textContent = 'Required';
    if (label) label.innerHTML = '<strong>I have read and agree to the disclaimer</strong>';
  }
}

// 在 loadSettings 中调用: updateGHDisclaimerStatus(CONFIG.disclaimer_agreed ? true : false);

document.getElementById('disclaimerAgreed').addEventListener('change', function() {
  updateGHDisclaimerStatus(this.checked);
});

// ========== 长消息展开功能 (GitHub/Notion 风格) ==========

function ghRenderMsg(msg) {
  if (!msg) return '';
  var e = esc(msg);
  if (msg.length <= 32) return '<span class="gh-msg-preview">' + e + '</span>';

  return '<span class="gh-msg-cell" data-gh-full="' + e.replace(/"/g, '&quot;') + '">' +
    '<span class="gh-msg-preview">' + e.slice(0, 32) + '</span>' +
    '<span class="gh-msg-toggle">show more</span>' +
  '</span>';
}

// loadLogs 中使用: '<td>' + ghRenderMsg(l.msg_preview) + '</td>'

function initGHMsgExpand() {
  document.querySelectorAll('.gh-msg-cell').forEach(function(cell) {
    var preview = cell.querySelector('.gh-msg-preview');
    var toggle = cell.querySelector('.gh-msg-toggle');
    var fullText = cell.getAttribute('data-gh-full');

    if (!toggle) return;

    toggle.addEventListener('click', function(e) {
      e.stopPropagation();

      if (cell.dataset.expanded === 'true') {
        // 收起
        cell.dataset.expanded = 'false';
        preview.className = 'gh-msg-preview';
        preview.textContent = fullText.slice(0, 32);
        toggle.textContent = 'show more';
      } else {
        // 展开
        cell.dataset.expanded = 'true';
        preview.className = 'gh-msg-expanded';
        preview.textContent = fullText;
        toggle.textContent = 'show less';
      }
    });

    preview.addEventListener('click', function(e) {
      e.stopPropagation();
      toggle.click();
    });
  });
}

// loadLogs 末尾调用: initGHMsgExpand();
```

---

# ═══════════════════════════════════════════
# 通用集成指南
# ═══════════════════════════════════════════

## 步骤 1：选择模板并添加 CSS

在 `index.html` 的 `<style>` 标签末尾（第218行之前），追加所选模板的 CSS 代码。

## 步骤 2：替换 HTML

找到原 `#disclaimerCard` div（约第352-367行），整体替换为模板的 HTML。

## 步骤 3：修改 loadSettings 函数

在 `loadSettings()` 函数中（约第792行之后），将原有的状态更新代码：

```javascript
var agreed = CONFIG.disclaimer_agreed ? true : false;
var cb = $('#disclaimerAgreed');
if (cb) cb.checked = agreed;
var card = $('#disclaimerCard');
var label = $('#disclaimerLabel');
if (card) card.style.borderColor = agreed ? 'var(--success)' : 'var(--warning)';
if (card) card.querySelector('.card-header').style.background = agreed ? 'var(--success-light)' : 'var(--warning-light)';
if (card) card.querySelector('.card-header h2').style.color = agreed ? 'var(--success)' : 'var(--warning)';
if (label) label.textContent = agreed ? '已同意免责声明' : '我已阅读并同意免责声明';
```

替换为对应模板的更新函数调用：

| 模板 | 替换为 |
|------|--------|
| A - Cloudflare | `updateCFDisclaimerStatus(agreed);` |
| B - Linear/Vercel | `updateLinDisclaimerStatus(agreed);` |
| C - GitHub/Notion | `updateGHDisclaimerStatus(agreed);` |

## 步骤 4：修改 loadLogs 函数的消息渲染

### 原始代码（约第727-731行）：

```javascript
return '<tr><td>' + fmtTime(l.ts) + '</td><td>' + esc(l.group_id) + '</td><td>' + esc(l.user_name) + '<br><span style="font-size:10px;color:#909399">' + esc(l.user_id) + '</span></td><td class="msg-cell" title="' + esc(l.msg_preview) + '">' + esc(l.msg_preview) + '</td><td><span class="badge ' + cls + '">' + esc(a) + '</span></td><td class="reason-cell" title="' + esc(l.reason) + '">' + esc((l.reason || '').slice(0, 30)) + '</td></tr>';
```

### 替换为（以模板A为例）：

```javascript
return '<tr><td>' + fmtTime(l.ts) + '</td><td>' + esc(l.group_id) + '</td><td>' + esc(l.user_name) + '<br><span style="font-size:10px;color:#909399">' + esc(l.user_id) + '</span></td><td>' + renderExpandableMessage(l.msg_preview) + '</td><td><span class="badge ' + cls + '">' + esc(a) + '</span></td><td class="reason-cell" title="' + esc(l.reason) + '">' + esc((l.reason || '').slice(0, 30)) + '</td></tr>';
```

## 步骤 5：在 loadLogs 末尾添加初始化调用

在 `loadLogs()` 函数的最后（表格渲染完成后），添加：

| 模板 | 调用 |
|------|------|
| A - Cloudflare | `initMsgExpand();` |
| B - Linear/Vercel | `initLinMsgExpand();` |
| C - GitHub/Notion | `initGHMsgExpand();` |

## 步骤 6：移除旧样式（可选）

如果完全切换到新模板，可以删除或注释掉原有的：

```css
.msg-cell{max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
```

以及原有 `#disclaimerAgreed` 的 change 事件监听器中的状态更新逻辑（约第995-1003行）。

---

# ═══════════════════════════════════════════
# 三种风格对比速查表
# ═══════════════════════════════════════════

| 特性 | A: Cloudflare 企业风 | B: Linear/Vercel 简约风 | C: GitHub/Notion 实用风 |
|------|---------------------|------------------------|------------------------|
| **视觉密度** | 中等 | 低（大量留白） | 高（信息紧凑） |
| **状态标识** | 左侧竖线色条 + 徽章 | 小圆点 + 文字 | Badge 标签 |
| **边框风格** | 1px 实线 + 左侧色条 | 1px 细线 | 1px 标准 |
| **按钮风格** | 实心填充 + 图标 | 下划线链接式 | 绿色填充（GitHub绿） |
| **Toggle 尺寸** | 44×24px（标准） | 36×20px（精致） | 原生 checkbox |
| **底部提示** | 蓝色信息条（i图标） | 纯文字提示 | 左侧蓝色竖线提示框 |
| **动效强度** | 中等（transform+shadow） | 轻（opacity/border） | 无/极少 |
| **适用场景** | 企业级/正式产品 | 现代 SaaS / 开发者工具 | 设置密集型 / GitHub 用户 |
| **色彩倾向** | 蓝+橙+绿（多色系） | 单色灰阶 + 点缀 | 黑白灰 + GitHub绿 |
| **专业感** | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **现代感** | ★★★★☆ | ★★★★★ | ★★★☆☆ |

---

*文档结束*
