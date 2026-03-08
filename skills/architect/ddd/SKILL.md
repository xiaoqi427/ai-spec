---
name: ddd
description: 领域驱动设计（DDD）建模与架构技能。当用户需要进行领域建模、识别限界上下文、设计聚合根、执行事件风暴、分析领域事件、设计分层架构、定义通用语言、验证领域模型一致性、或将现有代码重构为DDD架构时使用此技能。触发词包括："领域建模"、"DDD分析"、"限界上下文"、"聚合根设计"、"事件风暴"、"防腐层"、"通用语言"等。
---

# DDD 领域驱动设计技能

> 基于《领域驱动设计：软件核心复杂性应对之道》核心概念，提供从分析到落地的完整工具链。

## 使用方式

### 1. 领域分析

```bash
# 分析现有代码库，提取领域概念
/skill ddd analyze <代码路径>

# 分析需求文档，识别领域模型
/skill ddd analyze --doc <需求文档路径>
```

**示例**:
```bash
/skill ddd analyze ./fssc-claim-service
/skill ddd analyze --doc ./docs/业务需求.md
```

### 2. 领域建模

```bash
# 从需求中生成领域模型
/skill ddd model <领域名称> --desc "业务描述"

# 基于事件风暴结果建模
/skill ddd model <领域名称> --events <事件清单文件>
```

**示例**:
```bash
/skill ddd model 报账 --desc "财务共享中心报账单全生命周期管理"
/skill ddd model 支付 --events ./events/payment-events.yaml
```

### 3. 事件风暴

```bash
# 启动事件风暴引导式会话
/skill ddd event-storm <业务主题>

# 从已有文档提取事件
/skill ddd event-storm <业务主题> --doc <文档路径>
```

**示例**:
```bash
/skill ddd event-storm 报账单提交审批流程
/skill ddd event-storm 采购到付款 --doc ./docs/PTP流程说明.md
```

### 4. 上下文映射

```bash
# 生成限界上下文映射图
/skill ddd context-map <项目路径>

# 分析两个上下文间的集成关系
/skill ddd context-map --from <上下文A> --to <上下文B>
```

**示例**:
```bash
/skill ddd context-map ./fssc-claim-service
/skill ddd context-map --from 报账 --to 支付
```

### 5. 模型验证

```bash
# 验证领域模型一致性
/skill ddd validate <模型文件或代码路径>
```

### 6. 架构重构建议

```bash
# 基于DDD原则给出重构建议
/skill ddd refactor <代码路径> --target <目标模式>
```

**target 可选值**: `aggregate`（聚合优化）、`context`（上下文拆分）、`layer`（分层调整）、`event`（事件驱动改造）

---

## 执行流程

每个命令按以下阶段执行：

```
1. 收集信息 → 读取代码/文档，提取关键业务概念
2. 分析输出 → 生成分析报告或设计方案（Markdown + Mermaid 图）
3. 交互确认 → 展示方案，等待用户确认或调整
4. 产出交付 → 输出最终模型文件、代码结构、或重构方案
```

---

## 核心能力矩阵

| 能力域 | 子能力 | 参考文档 |
|--------|--------|----------|
| **领域建模** | 实体识别、值对象设计、聚合根构建 | [references/domain-model-spec.md](references/domain-model-spec.md) |
| **限界上下文** | 上下文识别、映射关系、集成模式 | [references/bounded-context.md](references/bounded-context.md) |
| **领域事件** | 事件风暴、事件溯源、事件建模 | [references/domain-events.md](references/domain-events.md) |
| **分层架构** | 领域层/应用层/基础设施层设计 | [references/layered-architecture.md](references/layered-architecture.md) |
| **通用语言** | 术语定义、业务规则表达、模型验证 | [references/ubiquitous-language.md](references/ubiquitous-language.md) |
| **集成模式** | ACL防腐层、开放主机服务、发布语言 | [references/integration-patterns.md](references/integration-patterns.md) |

---

## 模板与工具

| 模板 | 用途 | 文件 |
|------|------|------|
| C4 模型模板 | 系统架构可视化（4层） | [assets/c4-model-template.md](assets/c4-model-template.md) |
| 事件风暴模板 | 引导式事件风暴工作坊 | [assets/event-storming-template.md](assets/event-storming-template.md) |
| 聚合设计画布 | 聚合根边界与不变量设计 | [assets/aggregate-design-canvas.md](assets/aggregate-design-canvas.md) |
| 上下文映射模板 | 限界上下文关系可视化 | [assets/context-map-template.md](assets/context-map-template.md) |

| 脚本 | 用途 | 文件 |
|------|------|------|
| 领域分析 | 从代码中提取领域概念 | [scripts/analyze-domain.py](scripts/analyze-domain.py) |
| 模型验证 | 检查模型一致性和规范 | [scripts/validate-model.py](scripts/validate-model.py) |
| 上下文映射生成 | 生成 Mermaid 上下文映射图 | [scripts/gen-context-map.py](scripts/gen-context-map.py) |

---

## 应用场景示例

### 场景1: 新项目领域建模

**背景**: 启动一个新的财务共享服务模块，需要从零开始设计领域模型。

```bash
# 第一步：事件风暴，发现领域事件
/skill ddd event-storm 费用报销流程

# 第二步：基于事件识别聚合根和实体
/skill ddd model 费用报销 --desc "员工费用报销单据的创建、审批、支付全流程"

# 第三步：生成上下文映射图
/skill ddd context-map --from 报账 --to 审批
```

**产出**: 领域模型类图、聚合根边界图、上下文映射关系图

### 场景2: 遗留系统DDD重构

**背景**: 现有系统代码耦合严重，需要按DDD原则重构。

```bash
# 分析现有代码结构
/skill ddd analyze ./src/com/yili/fssc/claim

# 识别限界上下文边界
/skill ddd context-map ./fssc-claim-service

# 生成重构建议
/skill ddd refactor ./fssc-claim-service --target aggregate
```

**产出**: 问题诊断报告、重构路线图、目标架构设计

### 场景3: 微服务边界划分

**背景**: 单体应用拆分为微服务，需要确定服务边界。

```bash
# 基于限界上下文分析服务边界
/skill ddd context-map ./monolith-app

# 分析上下文间的集成模式
/skill ddd context-map --from 订单 --to 库存
```

**产出**: 服务边界定义、集成模式推荐、防腐层设计方案

---

## 强制约束

1. **通用语言一致性** - 所有产出（模型、代码、文档）必须使用统一的领域术语
2. **聚合边界不可跨越** - 聚合内部强一致，聚合间通过事件或ID引用
3. **值对象优先** - 能用值对象的不用实体，减少可变状态
4. **领域层无外部依赖** - 领域层不依赖框架、数据库、UI
5. **渐进式设计** - 先建核心模型，再逐步扩展，避免过度设计
