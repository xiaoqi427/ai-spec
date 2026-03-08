---
name: agile-scrum-helper
description: 基于《Scrum 指南》(2020版) 的敏捷仪式引导与工件生成技能。提供 Sprint 计划会、每日站会、Sprint 评审会、Sprint 回顾会的引导话术，以及产品待办列表、Sprint 待办列表等工件模板。当用户需要组织或改进 Scrum 仪式、创建敏捷工件、解决敏捷实践中的常见问题时使用。触发词包括："Scrum"、"敏捷"、"Sprint"、"站会"、"回顾会"、"看板"、"待办列表"、"用户故事"、"迭代"、"敏捷教练"。
---

# 敏捷 Scrum 助手

> 基于《Scrum 指南》(2020版)，提供 Scrum 仪式引导和工件生成的全套支持。
> **核心理念：Scrum 建立在经验主义和精益思维之上。经验主义认为知识来自经验以及基于观察到的事物做出决定。**

---

## 使用方式

### 1. 仪式引导

```bash
# 获取某个 Scrum 仪式的完整引导话术
/skill agile-scrum-helper ceremony <仪式名称>

# 获取针对特定问题的仪式改进建议
/skill agile-scrum-helper ceremony <仪式名称> --problem <问题描述>
```

**示例**:
```bash
/skill agile-scrum-helper ceremony "Sprint计划会"
/skill agile-scrum-helper ceremony "回顾会" --problem "团队不愿意说真话"
```

### 2. 工件生成

```bash
# 生成 Scrum 工件模板
/skill agile-scrum-helper artifact <工件类型>

# 生成用户故事
/skill agile-scrum-helper story --role <角色> --goal <目标> --benefit <价值>
```

**示例**:
```bash
/skill agile-scrum-helper artifact "产品待办列表"
/skill agile-scrum-helper story --role "财务人员" --goal "提交报销单" --benefit "快速获得报销款"
```

### 3. 敏捷健康检查

```bash
# 诊断团队敏捷实践的健康度
/skill agile-scrum-helper health-check

# 针对特定问题获取改进建议
/skill agile-scrum-helper diagnose <问题描述>
```

**示例**:
```bash
/skill agile-scrum-helper health-check
/skill agile-scrum-helper diagnose "Sprint 目标总是无法完成"
```

### 4. 回顾会活动

```bash
# 获取回顾会活动推荐
/skill agile-scrum-helper retro-activity --team-size <人数> --mood <团队氛围>
```

**示例**:
```bash
/skill agile-scrum-helper retro-activity --team-size 7 --mood "疲惫"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 命令 | ✅ | ceremony / artifact / story / health-check / diagnose / retro-activity | `ceremony` |
| --problem | ❌ | 具体问题描述 | `"团队不愿意发言"` |
| --role | ❌ | 用户故事中的角色 | `"管理员"` |
| --goal | ❌ | 用户故事中的目标 | `"查看报表"` |
| --benefit | ❌ | 用户故事中的价值 | `"做出决策"` |
| --team-size | ❌ | 团队人数 | `7` |
| --mood | ❌ | 团队当前氛围 | `"积极"`, `"疲惫"`, `"紧张"` |

---

## Scrum 框架速览

### 三大支柱

| 支柱 | 英文 | 含义 |
|------|------|------|
| **透明** | Transparency | 过程和工作对执行者和检查者必须可见 |
| **检视** | Inspection | Scrum 工件和进展必须被频繁检视 |
| **适应** | Adaptation | 如果发现偏差，必须尽快调整 |

### 五大价值观

| 价值观 | 英文 | 团队行为表现 |
|--------|------|------------|
| **承诺** | Commitment | 承诺达成 Sprint 目标 |
| **专注** | Focus | 专注于 Sprint 的工作 |
| **开放** | Openness | 对工作和挑战保持开放 |
| **尊重** | Respect | 相互尊重，认可彼此的能力 |
| **勇气** | Courage | 勇于做正确的事，处理棘手问题 |

### 三个角色

| 角色 | 英文 | 核心职责 |
|------|------|---------|
| **产品负责人** | Product Owner | 最大化产品价值，管理产品待办列表 |
| **Scrum Master** | Scrum Master | 促进 Scrum 的有效性，服务团队和组织 |
| **开发者** | Developers | 每个 Sprint 创建可用增量的专业人士 |

### 五个事件（仪式）

| 事件 | 时间盒 | 目的 | 引导话术 |
|------|--------|------|---------|
| **Sprint** | 1-4周（固定） | 将想法转化为价值的容器 | — |
| **Sprint 计划会** | 最长8小时(1个月Sprint) | 规划 Sprint 要做的工作 | [prompts/sprint-planning.md](prompts/sprint-planning.md) |
| **每日站会** | 15分钟 | 检视进展、调整计划 | [prompts/daily-standup.md](prompts/daily-standup.md) |
| **Sprint 评审会** | 最长4小时(1个月Sprint) | 检视增量并决定未来适应 | [prompts/sprint-review.md](prompts/sprint-review.md) |
| **Sprint 回顾会** | 最长3小时(1个月Sprint) | 检视并改进团队工作方式 | [prompts/sprint-retrospective.md](prompts/sprint-retrospective.md) |

### 三个工件

| 工件 | 承诺 | 用途 |
|------|------|------|
| **产品待办列表** | 产品目标 | 持续演进的有序工作清单 |
| **Sprint 待办列表** | Sprint 目标 | Sprint 期间开发者的计划 |
| **增量** | 完成的定义(DoD) | 迈向产品目标的可用基石 |

---

## 执行流程

```
1. 意图识别 → 判断用户需要仪式引导、工件生成还是问题诊断
2. 上下文收集 → 了解团队规模、Sprint 周期、当前阶段
3. 内容匹配 → 匹配对应的引导话术或模板
4. 场景适配 → 根据团队特征调整建议
5. 交付输出 → 输出可直接使用的引导话术或工件模板
```

### 响应级别

| 级别 | 触发条件 | 输出形式 |
|------|---------|---------|
| **快速** | 概念问题、角色职责查询 | 直接回答 |
| **标准** | 仪式引导、单个工件模板 | 话术/模板 + 注意事项 |
| **深度** | 健康检查、复杂问题诊断 | 完整分析 + 改进路线图 |

---

## 常见反模式与对策

| 反模式 | 症状 | 对策 |
|--------|------|------|
| **无目标Sprint** | 团队只是完成任务清单，没有 Sprint 目标 | 强制在计划会设定 Sprint 目标，每日站会围绕目标检视 |
| **站会变汇报会** | 成员对PM/领导汇报而非彼此沟通 | Scrum Master 引导改为面向团队沟通，领导后退 |
| **回顾会走形式** | 总是"挺好的没什么问题" | 使用多样化回顾活动，创造安全空间 |
| **PO不到场** | 产品负责人不参加仪式 | 明确PO是Scrum团队成员，出席是职责 |
| **迷你瀑布** | Sprint内仍是瀑布（先分析再开发再测试） | 推动跨功能协作，鼓励切片交付 |
| **Sprint延期** | Sprint截止日总是被推迟 | Sprint时间盒不可变，未完成的退回待办列表 |

---

## 强制约束

**必须做**：
1. 严格基于《Scrum 指南》2020版的定义和原则
2. 引导话术必须实用、可直接使用
3. 根据团队成熟度调整建议的深度
4. 信息不足时追问团队情况
5. 用中文回答

**不要做**：
1. 不要混淆 Scrum 与其他敏捷框架（如 SAFe、LeSS）的概念
2. 不要教条化，Scrum 是框架不是方法论
3. 不要忽视团队的实际约束和文化背景
4. 不要将 Scrum Master 描述为"项目经理"
5. 不要在引导话术中使用过于学术化的语言
