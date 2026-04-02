---
name: coding-bug-ops
description: 操作 Coding 平台 Bug 跟踪系统，读取 Bug 列表、详情、评论，添加评论和更新状态。基于 browser-use CLI 实现浏览器自动化操作。当用户需要查询 Coding Bug、读取 Bug 详情和评论、添加修复备注、更新 Bug 状态时使用。
allowed-tools: Bash(browser-use:*)
---
# Coding Bug Ops (Coding 平台 Bug 操作)
@author: sevenxiao

## 概述

此 skill 专注于操作 **Coding 平台** 的 Bug 跟踪系统，提供 6 大核心能力：

1. **`read-list`** 从 Bug 筛选器页面读取 Bug 列表
2. **`read-detail`** 读取单个 Bug 的完整详情（标题、描述、字段）
3. **`read-comments`** 读取 Bug 的所有评论（含补充说明、复现步骤等关键信息）
4. **`read-activity`** 读取 Bug 的活动日志（状态变更历史）
5. **`add-comment`** 向 Bug 添加评论
6. **`update-status`** 更新 Bug 状态

## 外部依赖

| 外部 Skill | 安装命令 | 说明 |
|------------|----------|------|
| `browser-use` | `npx openskills add browser-use/browser-use@browser-use` | 浏览器自动化 CLI, 安装位置: `.agents/skills/browser-use/` |

安装后执行 `browser-use doctor` 验证环境。

---

## 使用方式

```bash
# 读取 Bug 列表（从筛选器 URL）
/skill coding-bug-ops read-list <filter-url>

# 读取单个 Bug 详情 + 评论
/skill coding-bug-ops read-detail <bug-id>

# 向 Bug 添加评论
/skill coding-bug-ops add-comment <bug-id> "<评论内容>"

# 更新 Bug 状态
/skill coding-bug-ops update-status <bug-id> <目标状态>
```

**示例**:
```bash
# 读取筛选器中的所有 Bug
/skill coding-bug-ops read-list https://yldc.coding.yili.com/p/fssc/all/issues?filter=f209a5d4938a2da58718629a2f35419a

# 读取 #4992 的详情和评论
/skill coding-bug-ops read-detail 4992

# 添加前端标注评论
/skill coding-bug-ops add-comment 4992 "前端问题, 对应老代码 WebRoot/newPages/.../T044.jsp L120-L135, 新框架不修改"

# 标记为已修复
/skill coding-bug-ops update-status 4992 已修复
```

---

## Coding 平台 URL 约定

| 页面类型 | URL 模式 |
|----------|----------|
| Bug 列表 (筛选器) | `https://yldc.coding.yili.com/p/fssc/all/issues?filter=<filter-id>` |
| Bug 详情 | `https://yldc.coding.yili.com/p/fssc/bug-tracking/issues/<bug-id>/detail` |

---

## 认证策略

按优先级依次尝试：

### 1. Chrome Profile 复用（优先）

直接复用本机 Chrome 已登录的会话，无需额外配置：

```bash
browser-use --profile "Default" open <url>
```

若默认 Profile 未登录 Coding，可尝试其他 Profile：

```bash
browser-use profile list
browser-use --profile "Profile 1" open <url>
```

### 2. Cookie 导入（降级）

从预存的 Cookie 文件导入：

```bash
browser-use cookies import config/coding-cookies.json
browser-use open <url>
```

### 3. 账号密码登录（兜底）

从 `config/coding-auth.yaml` 读取配置，自动填写登录表单：

```bash
# 读取配置
# coding-auth.yaml 中的 username 和 password

browser-use open https://yldc.coding.yili.com/login
browser-use state
browser-use input <username-idx> "<username>"
browser-use input <password-idx> "<password>"
browser-use click <login-btn-idx>
browser-use wait text "项目"
```

**认证验证**: 打开页面后，检查是否被重定向到登录页：
```bash
browser-use state
# 如果 URL 包含 /login → 认证失败, 降级到下一策略
# 如果看到项目内容 → 认证成功
```

---

## 核心能力

### read-list (读取 Bug 列表)

**输入**: Coding 筛选器 URL

**执行步骤**:

```bash
# 1. 打开筛选器页面（使用 Chrome Profile 复用登录态）
browser-use --profile "Default" open "<filter-url>"

# 2. 等待列表加载
browser-use wait text "缺陷"

# 3. 获取页面状态，查看列表元素
browser-use state

# 4. 通过 JS 提取 Bug 列表数据
browser-use eval "
  const rows = document.querySelectorAll('.issue-list-item, [class*=IssueItem], tr[class*=issue]');
  const bugs = [];
  rows.forEach(row => {
    const id = row.querySelector('[class*=id], [class*=Id]')?.innerText?.trim();
    const title = row.querySelector('[class*=title], [class*=name]')?.innerText?.trim();
    const status = row.querySelector('[class*=status], [class*=Status]')?.innerText?.trim();
    const assignee = row.querySelector('[class*=assignee], [class*=Assignee]')?.innerText?.trim();
    if (id || title) bugs.push({id, title, status, assignee});
  });
  JSON.stringify(bugs, null, 2);
"

# 5. 如果列表较长，滚动加载更多
browser-use scroll down
browser-use wait selector "[class*=issue]"
# 重复 eval 提取
```

**如果 JS 提取不到数据**（Coding 使用动态渲染）:
```bash
# 降级方案: 直接提取页面文本
browser-use eval "document.body.innerText.slice(0, 15000)"
# 从文本中解析 Bug 列表
```

**输出格式**:
```markdown
| Bug ID | 标题 | 状态 | 处理人 |
|--------|------|------|--------|
| #4992 | xxx功能异常 | 处理中 | zhangsan |
| #4991 | yyy显示错误 | 待处理 | lisi |
```

---

### read-detail (读取 Bug 详情)

**输入**: Bug ID (数字)

**执行步骤**:

```bash
# 1. 打开 Bug 详情页
browser-use --profile "Default" open "https://yldc.coding.yili.com/p/fssc/bug-tracking/issues/<bug-id>/detail"

# 2. 等待详情页加载
browser-use wait text "描述"

# 3. 提取详情页内容 (描述区 + 字段区)
browser-use eval "document.body.innerText.slice(0, 12000)"

# 4. 获取页面结构化状态
browser-use state
```

**采集字段清单**:
- **标题**: Bug 标题
- **描述**: 详细描述正文（通常包含复现步骤、截图说明等）
- **状态**: 待处理 / 处理中 / 已修复 / 已验证 / 已关闭
- **处理人**: 当前负责人
- **模块/标签**: 归属模块, 如 "049杂项采购报账单"
- **优先级**: 高 / 中 / 低
- **测试阶段**: SIT / UAT

**提取模板编号**: 从标签或标题中识别报账单编号
```
标签 "049杂项采购报账单" → T049
标题 "T044差旅报账新增保存异常" → T044
描述中 "T051/T052 页面xxx" → T051, T052
```

---

### read-comments (读取评论)

**重要**: 评论中经常包含 Bug 的关键信息，如补充的复现步骤、截图说明、开发反馈、历史修复记录等。**不能只看描述，必须读评论**。

**输入**: 在 read-detail 打开详情页之后执行

**执行步骤**:

```bash
# 1. 滚动到评论区（评论通常在页面下方）
browser-use scroll down
browser-use scroll down

# 2. 等待评论加载
browser-use wait selector "[class*=comment], [class*=Comment], [class*=activity]"

# 3. 提取所有评论
browser-use eval "
  const comments = document.querySelectorAll('[class*=comment-item], [class*=CommentItem], [class*=comment-content]');
  const result = [];
  comments.forEach((c, i) => {
    const author = c.querySelector('[class*=author], [class*=user-name], [class*=nickname]')?.innerText?.trim();
    const time = c.querySelector('[class*=time], [class*=date], time')?.innerText?.trim();
    const content = c.querySelector('[class*=content], [class*=body], [class*=text]')?.innerText?.trim();
    result.push({index: i+1, author, time, content});
  });
  JSON.stringify(result, null, 2);
"

# 4. 如果 JS 选择器没命中，降级提取
browser-use eval "
  // 获取评论区域的所有文本
  const commentArea = document.querySelector('[class*=comment-list], [class*=CommentList], [class*=activity-list]');
  commentArea ? commentArea.innerText : '未找到评论区域';
"
```

**输出格式**:
```markdown
### 评论列表 (共 N 条)

**评论 #1** - zhangsan @ 2025-12-15 10:30
> 复现步骤: 在T044页面点击保存后，金额字段未校验...

**评论 #2** - lisi @ 2025-12-16 09:00
> 补充: 老代码中有一段对金额的特殊处理在 InsertT044ClaimService.java L120...
```

---

### read-activity (读取活动日志)

**输入**: 在 read-detail 打开详情页之后执行（可选）

**执行步骤**:

```bash
# 1. 查找"活动"或"日志"标签
browser-use state

# 2. 点击活动日志标签
browser-use click <activity-tab-idx>

# 3. 等待加载
browser-use wait selector "[class*=activity], [class*=log]"

# 4. 提取活动日志
browser-use eval "
  const logs = document.querySelectorAll('[class*=activity-item], [class*=log-item]');
  const result = [];
  logs.forEach(log => {
    result.push(log.innerText.trim());
  });
  JSON.stringify(result, null, 2);
"
```

---

### add-comment (添加评论)

**输入**: Bug ID + 评论内容

**执行步骤**:

```bash
# 1. 确保在 Bug 详情页（如果不在，先打开）
browser-use --profile "Default" open "https://yldc.coding.yili.com/p/fssc/bug-tracking/issues/<bug-id>/detail"

# 2. 滚动到评论区
browser-use scroll down
browser-use scroll down

# 3. 获取页面状态，找到评论输入框
browser-use state

# 4. 点击评论输入框
browser-use click <comment-input-idx>

# 5. 输入评论内容
browser-use input <comment-input-idx> "<评论内容>"

# 6. 查看提交按钮
browser-use state

# 7. 点击提交
browser-use click <submit-btn-idx>

# 8. 验证评论是否提交成功
browser-use wait text "<评论内容的前几个字>"
browser-use screenshot comment-submitted.png
```

**常见评论模板**:

- 前端 Bug 标注:
  ```
  【AI分析】前端问题
  对应老代码: <文件路径> L<行号>
  遗漏逻辑: <简要描述>
  新框架不修改, 需前端开发处理
  ```

- 后端修复说明:
  ```
  【AI修复】后端代码已修复
  对应老代码: <文件路径> L<行号>
  修复文件: <新代码文件路径>
  修复内容: <简要描述>
  编译验证: 通过
  SIT测试: <通过/未测试>
  ```

---

### update-status (更新 Bug 状态)

**输入**: Bug ID + 目标状态

**执行步骤**:

```bash
# 1. 确保在 Bug 详情页
browser-use --profile "Default" open "https://yldc.coding.yili.com/p/fssc/bug-tracking/issues/<bug-id>/detail"

# 2. 获取页面状态
browser-use state

# 3. 找到状态字段并点击
browser-use click <status-field-idx>

# 4. 选择目标状态
browser-use state
browser-use click <target-status-idx>

# 5. 验证状态更新
browser-use state
browser-use screenshot status-updated.png
```

---

## Bug 信息采集策略

读取一个 Bug 的完整上下文，需要执行以下采集流程:

```
read-detail (获取标题、描述、字段)
    ↓
read-comments (获取所有评论，含关键补充信息)
    ↓
[可选] read-activity (获取状态变更历史)
    ↓
合并输出完整 Bug 上下文
```

**为什么必须读评论**:
- 描述中经常只有简短的问题现象
- 评论中包含: 复现步骤、补充截图说明、老代码定位线索、已尝试的修复思路、测试人员的额外反馈
- 评论和描述合并后才是完整的 Bug 上下文

**完整 Bug 上下文输出格式**:

```markdown
## Bug #<id>: <标题>

### 基本信息
- 状态: <状态>
- 处理人: <处理人>
- 优先级: <优先级>
- 模块/标签: <标签>
- 识别模板编号: T<XXX>

### 描述
<描述正文>

### 评论 (共 N 条)
<逐条评论>

### 关键信息汇总
- 问题现象: <一句话总结>
- 涉及模板: T<XXX>
- 涉及功能: <功能描述>
- 复现步骤: <从描述+评论中提取>
- 历史修复线索: <从评论中提取>
```

---

## 强制约束

1. **认证优先级**: Chrome Profile → Cookie 导入 → 账号密码登录，严格按顺序尝试
2. **不能只看描述**: 读取 Bug 时必须同时读评论，评论中经常有关键信息
3. **JS 选择器可能失效**: Coding 平台使用动态渲染，选择器可能需要根据实际页面调整
4. **降级策略**: 如果结构化提取失败，降级为 `document.body.innerText` 全文提取
5. **截图存证**: 关键操作（添加评论、更新状态）后必须截图
6. **不猜测**: 没有实际读取到的信息不要推测

## 参考

- Coding 平台页面结构: [references/coding-pages.md](references/coding-pages.md)
- 认证配置模板: [config/coding-auth.yaml.example](config/coding-auth.yaml.example)
- browser-use CLI 文档: `.agents/skills/browser-use/SKILL.md`
