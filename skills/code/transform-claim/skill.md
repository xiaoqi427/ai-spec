---
name: transform-claim
description: 报账单老代码迁移转换器，提供将老代码迁移到新框架的Service中。
---
# Transform Claim Service (报账单老代码迁移转换器)
@author: sevenxiao

## 📋 概述

此skill用于将财务共享服务中心各类报账单模块的**老代码**迁移转换到**新框架**的Service中。

**核心特点**:
- 与 `claim-generator`（生成空架子）不同，专注于**老逻辑的分析与迁移**
- 支持模块: TR/OTC/PTP/EER/FA/RTR
- 10步标准化迁移流程
- 保证逻辑完整性，遵循新框架分层规范

**适用场景**:
- "迁移T044的所有Service到新框架"
- "分析T047的老代码并转换到新Service"

---

## 🗺️ 迁移步骤映射表（10步）

| 步骤 | 功能 | 老代码类名 | 新代码类名 | 继承基类 | 详细文档 |
|------|------|-----------|-----------|---------|----------|
| 1 | New头 | `NewT{XXX}ClaimService` | `T{XXX}NewClaimServiceImpl` | `BaseNewClaimService` | [步骤1](steps/step-01-new-head.md) |
| 2 | New行 | `NewT{XXX}ClaimLineService` | `T{XXX}NewClaimLineServiceImpl` | `BaseNewClaimLineService` | [步骤2](steps/step-02-new-line.md) |
| 3 | Save头 | `Insert/UpdateT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` | `BaseSaveOrUpdateClaimService` | [步骤3](steps/step-03-save-head.md) |
| 4 | Save行 | `Insert/UpdateT{XXX}ClaimLineService` | `T{XXX}SaveClaimLineServiceImpl` | `BaseSave/UpdateClaimLineService` | [步骤4](steps/step-04-save-line.md) |
| 5 | Delete头 | `DeleteT{XXX}ClaimService` | `T{XXX}DeleteClaimServiceImpl` | `BaseDeleteClaimService` | [步骤5](steps/step-05-delete-head.md) |
| 6 | Delete行 | `DeleteT{XXX}ClaimLinesService` | `T{XXX}DeleteClaimLineServiceImpl` | `BaseDeleteClaimLineService` | [步骤6](steps/step-06-delete-line.md) |
| 7 | Load | `LoadAllT{XXX}Service` + 多个View | `T{XXX}LoadClaimServiceImpl` | `BaseLoadClaimService` | [步骤7](steps/step-07-load.md) |
| 8 | Callback | `CallBackT{XXX}Service` | `T{XXX}CallBackClaimServiceImpl` | `BaseCallBackClaimService` | [步骤8](steps/step-08-callback.md) |
| 9 | Submit | `SubmitT{XXX}Service` | `T{XXX}SubmitClaimServiceImpl` | `BaseSubmitClaimService` | [步骤9](steps/step-09-submit.md) |
| 10 | Load行 | `ListAllT{XXX}ClaimLinesService` | `T{XXX}LoadClaimLineService` | `BaseLoadClaimLineService` | [步骤10](steps/step-10-load-line.md) |

**说明**:
- `{XXX}` 为模板编号，如 `044`, `047`, `051`
- 步骤3-4: Insert和Update合并为Save
- 步骤7: 多个Load/View Service合并为一个
- 点击"详细文档"查看每步的完整迁移策略

---

## 💻 使用方式

### 方式1: 整体迁移（推荐）

```bash
/skill transform-claim <模块名> <模板编号> --md <需求文档路径>
```

**示例**:
```bash
# 迁移OTC模块T044的全部10个步骤
/skill transform-claim otc T044 --md ./quests/T044-需求分析.md

# 迁移TR模块T065
/skill transform-claim tr T065
```

### 方式2: 单步迁移

```bash
/skill transform-claim <模块名> <模板编号> --step <步骤号>
```

**示例**:
```bash
# 只迁移T044的步骤3（Save报账单头）
/skill transform-claim otc T044 --step 3
```

**参数说明**:
- `模块名`: tr/otc/ptp/eer/fa/rtr
- `模板编号`: T044/T047/T051 等
- `--md`: (可选) 需求分析文档路径
- `--step`: (可选) 指定执行步骤(1-10)

---

## 🔄 执行流程

**AI将按以下4个阶段执行每个步骤**（详见 [WORKFLOW.md](WORKFLOW.md)）：

1. **分析老代码** → 定位文件、逐行分析、对照基类
2. **输出设计方案** → 陈述方案（最多500字）
3. **等待确认** → 用户回复"确认"后才写代码
4. **编写+验证** → 创建新代码、检查完整性

**重要**: 每步都会先给出设计方案并等待确认，不会直接写代码。

---

## ⚠️ 强制约束（每一步必须遵守）

### 迁移原则
1. **不修改继承类的代码，需要变更请重写** - 老逻辑如果与父类方法冲突，必须在子类重写，绝不修改基类
2. **存在父类逻辑直接调用** - 如果父类已有实现且满足需求，直接调用不用重写
3. **逻辑要完整** - 不能遗漏任何老代码中的业务逻辑
4. **不要遗漏代码** - 每一行老代码都要有对应的新代码处理
5. **代码先迁移过来，再看情况是否需要重构** - 方法尽量和之前保持一致

### 注释规范
- 抽离出的方法，方法注释上要写出**原来代码对应行数**
- 迁移老代码到新代码，在新代码中要**写好老代码的行数**

### 字段处理
- **不存在的字段创建在对应的DTO中，不要创建在DO中**
- 导入包，别直接写在代码里面

### 代码质量
- 迁移之后的代码**不要有编译错误**
- 不能对传入的变量重新赋值，对象set可以
- MyBatis Plus就能实现的不要创建SQL
- 单表尽量用 `LambdaQueryWrapperX`

### 工具类
- `NumberToCNUtil` 方法是存在的，可以直接使用
- 有些方法可以在 `claim-ptp`, `claim-eer`, `claim-otc`, `claim-base` 中寻找复用逻辑

### 特殊注意
- 调用 `isImagePool` 初始化影像状态是 `t_process_wi_record` 表，和 `findImage` 的 `EIM_IMAGE` 不是同一个东西
- 老逻辑中 `Insert` 和 `Update` 在新框架中合并为一个 `Save`
- Load 步骤中老逻辑分头行多个Service，新框架合并为一个

---

## 📁 代码路径约定

```
claim-{module}-service/
  └── src/main/java/com/yili/claim/{module}/claim/t{xxx}/
      ├── head/
      │   ├── IT{XXX}NewClaimService.java
      │   ├── IT{XXX}LoadClaimService.java
      │   ├── IT{XXX}SaveClaimService.java
      │   ├── IT{XXX}DeleteClaimService.java
      │   └── impl/
      │       ├── T{XXX}NewClaimServiceImpl.java
      │       ├── T{XXX}LoadClaimServiceImpl.java
      │       ├── T{XXX}SaveClaimServiceImpl.java
      │       └── T{XXX}DeleteClaimServiceImpl.java
      ├── line/
      │   ├── IT{XXX}NewClaimLineService.java
      │   ├── IT{XXX}SaveClaimLineService.java
      │   ├── IT{XXX}UpdateClaimLineService.java
      │   ├── IT{XXX}DeleteClaimLineService.java
      │   ├── T{XXX}LoadClaimLineService.java
      │   └── impl/
      │       ├── T{XXX}NewClaimLineServiceImpl.java
      │       ├── T{XXX}SaveClaimLineServiceImpl.java
      │       ├── T{XXX}UpdateClaimLineServiceImpl.java
      │       └── T{XXX}DeleteClaimLineServiceImpl.java
      └── bpm/ (或 workflow/)
          ├── IT{XXX}CallBackClaimService.java
          ├── IT{XXX}SubmitClaimService.java
          └── impl/
              ├── T{XXX}CallBackClaimServiceImpl.java
              └── T{XXX}SubmitClaimServiceImpl.java
```

**老代码典型路径**:
```
yldc-caiwugongxiangpingtai-fsscYR-master/src/com/yili/fssc/claim/service/
├── NewT{XXX}ClaimService.java
├── InsertT{XXX}ClaimService.java / UpdateT{XXX}ClaimService.java
├── DeleteT{XXX}ClaimService.java
├── LoadAllT{XXX}Service.java / ViewT{XXX}*Service.java
├── CallBackT{XXX}Service.java
└── SubmitT{XXX}Service.java
```

---

## 📦 模板文件清单

本 skill 提供了完整的代码模板，位于 `templates/` 目录下。

### 模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{module}}` | 模块名(小写) | otc, ptp, tr |
| `{{moduleUpper}}` | 模块名(首字母大写) | Otc, Ptp, Tr |
| `{{templateNum}}` | 模板编号 | 047, 044 |
| `{{businessDesc}}` | 业务描述 | 手工发票报账单 |
| `{{author}}` | 作者 | sevenxiao |
| `{{date}}` | 日期 | 2025-12-24 |

### 模板目录结构

```
templates/
├── head/          # 报账单头相关（8个文件）
│   ├── interface-new-template.java
│   ├── impl-new-template.java
│   ├── interface-save-template.java
│   ├── impl-save-template.java
│   ├── interface-delete-template.java
│   ├── impl-delete-template.java
│   ├── interface-load-template.java
│   └── impl-load-template.java
├── line/          # 报账单行相关（9个文件）
│   ├── interface-new-template.java
│   ├── impl-new-template.java
│   ├── interface-save-template.java
│   ├── impl-save-template.java
│   ├── interface-update-template.java
│   ├── impl-update-template.java
│   ├── interface-delete-template.java
│   ├── impl-delete-template.java
│   └── impl-load-line-template.java
└── bpm/           # BPM相关（4个文件）
    ├── interface-callback-template.java
    ├── impl-callback-template.java
    ├── interface-submit-template.java
    └── impl-submit-template.java
```

---

## 🔗 参考资料

- **执行工作流**: [WORKFLOW.md](WORKFLOW.md) - AI标准执行流程
- **步骤详细文档**: [steps/](steps/) - 每个步骤的完整迁移策略
- **项目规范**: `/ai-spec/rules/agents.md` - 项目开发规范
- **代码生成器**: `/ai-spec/skills/code/claim-generator/` - 生成空架子
- **现有参考**: claim-ptp、claim-eer、claim-otc、claim-base 中的已迁移代码
- **基类实现**:
  - 报账单头: `claim-common/.../claim/service/impl/Base*ClaimService`
  - 报账单行: `claim-common/.../line/service/impl/Base*ClaimLineService`
- **老代码**: `yldc-caiwugongxiangpingtai-fsscYR-master/src/`

---

## 📝 与 claim-generator 的区别

| 维度 | claim-generator | transform-claim |
|------|----------------|-----------------|
| 目的 | 生成全新的空架子代码 | 迁移老代码逻辑到新框架 |
| 输入 | 模板编号+业务描述 | 老代码+需求文档 |
| 输出 | 空的接口和实现类 | 包含完整业务逻辑的实现类 |
| 流程 | 一键生成 | 逐步分析、确认、迁移 |
| 适用 | 全新报账单模块 | 老系统重构升级 |
