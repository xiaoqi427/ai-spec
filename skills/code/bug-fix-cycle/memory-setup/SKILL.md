---
name: memory-setup
description: 为长链路、多步骤或批量任务初始化并维护运行记忆。适用于 Bug 修复流水线、批量问题处理、需要跨多个 skill 共享目标/约束/进度/经验的场景。
---
# Memory Setup

## 概述

此 skill 用来建立**紧凑、可更新、可传递**的运行记忆。

它不负责分析 Bug 本身，而是负责把下面这些信息固定下来:

- 当前目标
- Bug 队列和游标
- 已确认约束
- 待验证假设
- 模块/服务映射
- 当前阶段
- 已完成事项
- 可沿用检查项

适用场景:

- `bug-fix-pipeline` 这种跨多个 skill 的长流程
- 批量处理多个 Bug
- 需要中途暂停、恢复、重试、切换上下文

兼容策略:

- 本 skill 负责**当前仓库流程编排**所需的最小运行记忆
- 如果环境里额外安装了 OpenSkill `memory-management`，可以借用它的“热缓存 + 深记忆”分层组织
- 但在 `bug-fix-pipeline` 中，不用外部 memory skill 替代本 skill 的字段和步骤

---

## 输出格式

默认输出一个精简的 memory block:

```markdown
## Run Memory
- objective:
- mode: single / batch
- bug_queue:
- current_bug:
- phase:
- confirmed_constraints:
- assumptions_to_verify:
- service_map:
- carry_forward_checks:
- completed:
- risks:
- next_action:
```

如果任务需要落盘，再写到临时文件或流水线自己的运行目录。

---

## 工作流

### 1. 初始化

开始长流程前，先记录:

- 用户目标
- 输入来源
- 要处理的 Bug 列表
- 当前环境
- 默认验证策略
- 已知风险

### 2. 切换当前 Bug

每处理一个 Bug 时，更新:

- `current_bug`
- `phase`
- 当前模块
- 当前接口/页面
- 本轮待验证点

### 3. 记录已确认事实

只把**已验证**信息写入 `confirmed_constraints`，例如:

- 问题属于后端
- 对应模块是 `claim-base`
- 本地接口路径是 `/myReimbursement/AllClaimSavedList`

不确定的信息必须进入 `assumptions_to_verify`，不要混写。

### 4. 继承检查项

如果上一个 Bug 暴露了可复用的检查项，写入 `carry_forward_checks`，例如:

- “先读评论，再读描述”
- “列表接口优先构造最小 `PageParam` 请求体”
- “前端 service 如果用 `Setaria.getHttp().claim`，先映射到 `claim-base` 再找 Controller”

### 5. 收尾

每个 Bug 结束后:

- 记录已完成事项
- 清空过期假设
- 保留下一轮可复用检查项

---

## 强制约束

1. 记忆必须短，默认控制在当前任务真正需要的最小范围
2. 已确认事实和待验证假设必须分开
3. 记忆是运行导航，不是长篇总结
4. 每次阶段切换都要更新 `phase` 和 `next_action`
5. 可复用经验写进 `carry_forward_checks`，不要散落在临时说明里
