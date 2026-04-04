---
name: memory-setup
description: 为长链路、多步骤或批量任务初始化并维护运行记忆，同时支持持久化记忆搜索配置。适用于 Bug 修复流水线、批量问题处理、需要跨多个 skill 共享目标/约束/进度/经验的场景，以及跨会话长期记忆的持久化存储与检索。
---
# Memory Setup

## 概述

此 skill 用来建立**紧凑、可更新、可传递**的运行记忆，并支持**持久化长期记忆**。

两层记忆架构:

- **运行记忆** (Run Memory): 当前任务链的短期状态，随任务结束清空
- **持久记忆** (Persistent Memory): 跨会话的长期知识，包含人员、术语、项目、偏好等

### 运行记忆职责

把下面这些信息固定下来:

- 当前目标
- Bug 队列和游标
- 已确认约束
- 待验证假设
- 模块/服务映射
- 当前阶段
- 已完成事项
- 可沿用检查项

### 持久记忆职责

跨会话保存和检索:

- 人员信息（昵称、角色、沟通偏好）
- 术语表（缩写、代号、内部语言）
- 项目上下文（进度、关键人、代号）
- 决策记录和经验教训
- 个人偏好和工具链配置

适用场景:

- `bug-fix-pipeline` 这种跨多个 skill 的长流程
- 批量处理多个 Bug
- 需要中途暂停、恢复、重试、切换上下文
- 新会话启动时快速恢复项目上下文

兼容策略:

- 本 skill 负责**当前仓库流程编排**所需的最小运行记忆
- 如果环境里额外安装了 OpenSkill `memory-management`，可以借用它的"热缓存 + 深记忆"分层组织
- 如果环境里安装了 OpenSkill `memory-setup`(sundial-org)，可以借用其向量搜索和持久化配置
- 但在 `bug-fix-pipeline` 中，不用外部 memory skill 替代本 skill 的字段和步骤

---

## 运行记忆

### 输出格式

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

### 工作流

#### 1. 初始化

开始长流程前，先记录:

- 用户目标
- 输入来源
- 要处理的 Bug 列表
- 当前环境
- 默认验证策略
- 已知风险

#### 2. 切换当前 Bug

每处理一个 Bug 时，更新:

- `current_bug`
- `phase`
- 当前模块
- 当前接口/页面
- 本轮待验证点

#### 3. 记录已确认事实

只把**已验证**信息写入 `confirmed_constraints`，例如:

- 问题属于后端
- 对应模块是 `claim-base`
- 本地接口路径是 `/myReimbursement/AllClaimSavedList`

不确定的信息必须进入 `assumptions_to_verify`，不要混写。

#### 4. 继承检查项

如果上一个 Bug 暴露了可复用的检查项，写入 `carry_forward_checks`，例如:

- "先读评论，再读描述"
- "列表接口优先构造最小 `PageParam` 请求体"
- "前端 service 如果用 `Setaria.getHttp().claim`，先映射到 `claim-base` 再找 Controller"

#### 5. 收尾

每个 Bug 结束后:

- 记录已完成事项
- 清空过期假设
- 保留下一轮可复用检查项

---

## 持久记忆

### 记忆目录结构

```
workspace/
├── MEMORY.md              # 长期记忆热缓存（常用人员/术语/项目）
└── memory/
    ├── logs/              # 每日日志 (YYYY-MM-DD.md)
    ├── people/            # 人员档案 ({name}.md)
    ├── projects/          # 项目上下文 ({name}.md)
    ├── glossary.md        # 完整术语表
    └── system/            # 偏好、配置备忘
```

### MEMORY.md 热缓存模板

```markdown
# MEMORY.md — 长期记忆

## 常用人员 (Top 30)
| 昵称 | 全名 | 角色 | 沟通方式 |
|------|------|------|----------|
| 示例 | 张三 | 前端 | 企微 |

## 常用术语
| 缩写 | 全称 | 说明 |
|------|------|------|
| T047 | 手工发票报账单 | OTC 模块 |

## 活跃项目
- 项目名、状态、关键人

## 决策与教训
- 重要选择及原因
- 踩过的坑

## 偏好
- 沟通风格
- 工具链配置
```

### 每日日志格式

创建 `memory/logs/YYYY-MM-DD.md`:

```markdown
# YYYY-MM-DD — 每日日志

## [时间] — [事件/任务]
- 做了什么
- 做了什么决策
- 后续跟进事项

## [时间] — [另一个事件]
- 详情
```

### 记忆查找优先级

解码用户输入时按以下顺序查找:

```
1. MEMORY.md (热缓存)      → 最先检查，覆盖 90% 日常需求
2. memory/glossary.md       → 完整术语表
3. memory/people/projects/  → 详细档案
4. 询问用户                 → 未知术语，学习并记录
```

### 持久记忆搜索配置（可选）

如果使用支持向量搜索的 agent 环境，配置:

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

| 设置 | 用途 | 推荐值 |
|------|------|--------|
| `enabled` | 开启记忆搜索 | `true` |
| `provider` | 嵌入向量提供方 | `"voyage"` / `"openai"` / `"local"` |
| `sources` | 索引内容 | `["memory", "sessions"]` |
| `indexMode` | 索引时机 | `"hot"` (实时) |
| `minScore` | 相关度阈值 | `0.3` (越低结果越多) |
| `maxResults` | 最大返回数 | `20` |

### 持久记忆排障

| 问题 | 解决方案 |
|------|----------|
| 记忆搜索无结果 | 检查 MEMORY.md 是否存在，内容是否有意义 |
| 结果不相关 | 降低 `minScore` 到 `0.2`，增加 `maxResults` 到 `30` |
| Provider 报错 | 检查对应 API Key 环境变量，或改用 `local` |

---

## 强制约束

1. 运行记忆必须短，默认控制在当前任务真正需要的最小范围
2. 已确认事实和待验证假设必须分开
3. 记忆是运行导航，不是长篇总结
4. 每次阶段切换都要更新 `phase` 和 `next_action`
5. 可复用经验写进 `carry_forward_checks`，不要散落在临时说明里
6. 持久记忆热缓存（MEMORY.md）控制在 100 行以内
7. 新学到的术语/人员，频繁使用的提升到 MEMORY.md，低频的留在 memory/ 子目录
