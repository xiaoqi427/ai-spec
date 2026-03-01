---
name: transform-claim
description: 报账单老代码迁移转换器，提供将老代码迁移到新框架的Service中。
---
# Transform Claim Service (报账单老代码迁移转换器)
@author: sevenxiao
## 概述

此skill用于将财务共享服务中心各类报账单模块的**老代码**迁移转换到**新框架**的Service中。
与 `claim-generator`（生成全新空架子）不同，本skill专注于**老逻辑的分析与迁移**。

支持的迁移模块：
- **TR模块** (claim-tr) - 资金类报账单
- **OTC模块** (claim-otc) - 订单到现金报账单
- **PTP模块** (claim-ptp) - 采购到付款报账单
- **EER模块** (claim-eer) - 费用报账单
- **FA模块** (claim-fa) - 固定资产报账单
- **RTR模块** (claim-rtr) - 记录到报告报账单
- **其他模块** - 可扩展支持

## 适用场景

当用户需要将老代码迁移到新框架时使用，例如：
- "迁移T044的所有Service到新框架"
- "分析T047的老代码并转换到新Service"
- "将OTC模块的T051老逻辑迁移到新框架"

## 迁移步骤总览

每个报账单模板（如T044）的完整迁移包含以下10个步骤，**必须按顺序逐步执行**：

### 步骤1：更新New接口报账单头对应Service
- **老逻辑**: `NewT{XXX}ClaimService`
- **新框架**: `T{XXX}NewClaimServiceImpl`
- **继承基类**: `BaseNewClaimService`

### 步骤2：更新New接口报账单行对应Service
- **老逻辑**: `NewT{XXX}ClaimLineService`
- **新框架**: `T{XXX}NewClaimLineServiceImpl`
- **继承基类**: `BaseNewClaimLineService`

### 步骤3：更新Save接口报账单头对应Service
- **老逻辑**: `InsertT{XXX}ClaimService` + `UpdateT{XXX}ClaimService` (合并)
- **新框架**: `T{XXX}SaveClaimServiceImpl`
- **继承基类**: `BaseSaveClaimService`

### 步骤4：更新Save接口报账单行对应Service
- **老逻辑**: `InsertT{XXX}ClaimLineService` + `UpdateT{XXX}ClaimLineService` (合并)
- **新框架**: `T{XXX}SaveClaimLineServiceImpl`
- **继承基类**: `BaseSaveClaimLineService`

### 步骤5：更新Delete报账单头对应Service
- **老逻辑**: `DeleteT{XXX}ClaimService`
- **新框架**: `T{XXX}DeleteClaimServiceImpl`
- **继承基类**: `BaseDeleteClaimService`

### 步骤6：更新Delete报账单行对应Service
- **老逻辑**: `DeleteT{XXX}ClaimLinesService`
- **新框架**: `T{XXX}DeleteClaimLineServiceImpl`
- **继承基类**: `BaseDeleteClaimLineService`

### 步骤7：更新Load报账单对应Service（头+行合并）
- **老逻辑**: `LoadAllT{XXX}Service`, `ViewT{XXX}ClaimService`, `ViewT{XXX}ClaimLineService`, `ViewT{XXX}ClaimBankReceiptOneVendorService`, `ViewT{XXX}ClaimBankReceiptService`, `ViewT{XXX}ClaimBankReceiptVendorService` (多个合并为一个)
- **新框架**: `T{XXX}LoadClaimServiceImpl`
- **继承基类**: `BaseLoadClaimService`

### 步骤8：更新CallBack报账单对应Service
- **老逻辑**: `CallBackT{XXX}Service`
- **新框架**: `T{XXX}CallBackClaimServiceImpl`
- **继承基类**: `BaseCallBackClaimService`

### 步骤9：更新Submit报账单对应Service
- **老逻辑**: `SubmitT{XXX}Service`
- **新框架**: `T{XXX}SubmitClaimServiceImpl`
- **继承基类**: `BaseSubmitClaimService`

### 步骤10：新加行的Load Service
- **老逻辑**: `ListAllT{XXX}ClaimLinesService`
- **新框架**: `T{XXX}LoadClaimLineService`
- **Bean名称**: `@Service(value = "listAllT{XXX}ClaimLinesService")`

## 老代码到新代码映射关系总表

| 序号 | 功能 | 老代码类名 | 新代码类名 | 继承基类 |
|------|------|-----------|-----------|---------|
| 1 | 新建报账单头 | `NewT{XXX}ClaimService` | `T{XXX}NewClaimServiceImpl` | `BaseNewClaimService` |
| 2 | 新建报账单行 | `NewT{XXX}ClaimLineService` | `T{XXX}NewClaimLineServiceImpl` | `BaseNewClaimLineService` |
| 3 | 保存报账单头 | `InsertT{XXX}ClaimService` + `UpdateT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` | `BaseSaveClaimService` |
| 4 | 保存报账单行 | `InsertT{XXX}ClaimLineService` + `UpdateT{XXX}ClaimLineService` | `T{XXX}SaveClaimLineServiceImpl` | `BaseSaveClaimLineService` |
| 5 | 删除报账单头 | `DeleteT{XXX}ClaimService` | `T{XXX}DeleteClaimServiceImpl` | `BaseDeleteClaimService` |
| 6 | 删除报账单行 | `DeleteT{XXX}ClaimLinesService` | `T{XXX}DeleteClaimLineServiceImpl` | `BaseDeleteClaimLineService` |
| 7 | 加载报账单 | `LoadAllT{XXX}Service` + `ViewT{XXX}Claim*Service` (多个) | `T{XXX}LoadClaimServiceImpl` | `BaseLoadClaimService` |
| 8 | BPM回调 | `CallBackT{XXX}Service` | `T{XXX}CallBackClaimServiceImpl` | `BaseCallBackClaimService` |
| 9 | 提交校验 | `SubmitT{XXX}Service` | `T{XXX}SubmitClaimServiceImpl` | `BaseSubmitClaimService` |
| 10 | 加载报账单行 | `ListAllT{XXX}ClaimLinesService` | `T{XXX}LoadClaimLineService` | - |

## 强制约束（每一步必须遵守）

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

## 使用方式

### 整体迁移（推荐）

```bash
# 迁移整个模板的所有Service
/skill transform-claim <模块名> <模板编号> --md <需求文档路径>
```

**示例**:
```bash
# 迁移OTC模块T044的所有Service
/skill transform-claim otc T044 --md ./quests/T044-需求分析.md

# 迁移TR模块T065的所有Service
/skill transform-claim tr T065 --md ./quests/T065-需求分析.md
```

### 单步迁移

```bash
# 只迁移某个步骤
/skill transform-claim <模块名> <模板编号> --step <步骤号>
```

**示例**:
```bash
# 只迁移T044的Save报账单头（步骤3）
/skill transform-claim otc T044 --step 3

# 只迁移T044的Load（步骤7）
/skill transform-claim otc T044 --step 7
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 模块名 | ✅ | claim模块名 | tr, otc, ptp, eer, fa, rtr |
| 模板编号 | ✅ | 报账单编号 | T044, T047, T051 |
| --md | ❌ | 需求分析文档路径 | ./quests/T044-需求分析.md |
| --step | ❌ | 指定执行步骤(1-10) | 3 |

## 每步执行流程

对于每一步迁移，AI必须按以下流程执行：

### 1. 分析老逻辑
- 定位老代码文件（通过md文档提供路径或搜索代码库）
- 逐行分析老代码的业务逻辑
- 列出所有关键方法和调用链

### 2. 对比新框架
- 检查父类（Base*Service）是否已有对应实现
- 标注哪些逻辑在新框架中已实现（注明类名和方法名）
- 标注哪些逻辑需要在子类中重写

### 3. 陈述设计方案
- 输出设计方案和处理步骤
- 明确哪些方法需要重写
- 明确哪些方法直接调用父类
- **等待用户确认后才能修改代码**

### 4. 编写新代码
- 用户确认后，按设计方案编写代码
- 保持方法签名尽量和老代码一致
- 在方法注释中标注老代码行数
- 确保无编译错误

### 5. 验证完整性
- 检查是否有遗漏的老代码逻辑
- 确认所有字段映射正确
- 确认DTO中新增字段已创建

## 新代码存放路径

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

## 老代码典型路径

老代码通常位于：
```
yldc-caiwugongxiangpingtai-fsscYR-master/src/com/yili/fssc/claim/service/
├── NewT{XXX}ClaimService.java
├── NewT{XXX}ClaimLineService.java
├── InsertT{XXX}ClaimService.java
├── UpdateT{XXX}ClaimService.java
├── InsertT{XXX}ClaimLineService.java
├── UpdateT{XXX}ClaimLineService.java
├── DeleteT{XXX}ClaimService.java
├── DeleteT{XXX}ClaimLinesService.java
├── LoadAllT{XXX}Service.java
├── ViewT{XXX}ClaimService.java
├── ViewT{XXX}ClaimLineService.java
├── ListAllT{XXX}ClaimLinesService.java
├── CallBackT{XXX}Service.java
└── SubmitT{XXX}Service.java
```

## 与 claim-generator 的区别

| 维度 | claim-generator | transform-claim |
|------|----------------|-----------------|
| 目的 | 生成全新的空架子代码 | 迁移老代码逻辑到新框架 |
| 输入 | 模板编号+业务描述 | 老代码+需求文档 |
| 输出 | 空的接口和实现类 | 包含完整业务逻辑的实现类 |
| 流程 | 一键生成 | 逐步分析、确认、迁移 |
| 适用 | 全新报账单模块 | 老系统重构升级 |

## 模板文件清单

本 skill 提供了完整的代码模板，位于 `templates/` 目录下。使用时将模板变量替换为实际值。

### 模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{module}}` | 模块名(小写) | otc, ptp, tr, eer, fa, rtr |
| `{{moduleUpper}}` | 模块名(首字母大写) | Otc, Ptp, Tr |
| `{{templateNum}}` | 模板编号 | 047, 044, 051 |
| `{{templateNumLower}}` | 模板编号(小写包路径) | 047, 044, 051 |
| `{{businessDesc}}` | 业务描述 | 手工发票报账单, 退款报账单 |
| `{{author}}` | 作者 | sevenxiao |
| `{{date}}` | 日期 | 2025-12-24 |

### Head 层模板 (8个文件)

| 文件 | 对应步骤 | 基类 | 钩子方法 |
|------|---------|------|----------|
| `head/interface-new-template.java` | 步骤1 | IBaseNewClaimService | - |
| `head/impl-new-template.java` | 步骤1 | BaseNewClaimService | `preExecute(claim, user)` |
| `head/interface-save-template.java` | 步骤3 | IBaseSaveClaimService | - |
| `head/impl-save-template.java` | 步骤3 | BaseSaveOrUpdateClaimService | `preExecute(full,claim,old,params,user)`, `insertClaimLineFromClaim()`, `updateClaimLineFromClaim()` |
| `head/interface-delete-template.java` | 步骤5 | IBaseDeleteClaimService | - |
| `head/impl-delete-template.java` | 步骤5 | BaseDeleteClaimService | `preExecute(claimDto, user)` |
| `head/interface-load-template.java` | 步骤7 | IBaseLoadClaimService | - |
| `head/impl-load-template.java` | 步骤7 | BaseLoadClaimService | `preResult(claimPageFull, user)` |

### Line 层模板 (8个文件)

| 文件 | 对应步骤 | 基类 | 钩子方法 |
|------|---------|------|----------|
| `line/interface-new-template.java` | 步骤2 | IBaseNewClaimLineService | - |
| `line/impl-new-template.java` | 步骤2 | BaseNewClaimLineService | `preExecute(claimLineDto, claim)` |
| `line/interface-save-template.java` | 步骤4(新增) | IBaseSaveClaimLineService | - |
| `line/impl-save-template.java` | 步骤4(新增) | BaseSaveClaimLineService | `preExecute(claim, claimLineDto)`, `after(claim, claimLineDto)` |
| `line/interface-update-template.java` | 步骤4(修改) | IBaseUpdateClaimLineService | - |
| `line/impl-update-template.java` | 步骤4(修改) | BaseUpdateClaimLineService | `preExecute(claim, claimLineDto)`, `after(claim, claimLineDto)` |
| `line/interface-delete-template.java` | 步骤6 | IBaseDeleteClaimLineService | - |
| `line/impl-delete-template.java` | 步骤6 | BaseDeleteClaimLineService | `deleteClaimLine(claimLineDto)`, `after(claimLineDto)` |

### Line 加载模板 (1个文件)

| 文件 | 对应步骤 | 基类 | 钩子方法 |
|------|---------|------|----------|
| `line/impl-load-line-template.java` | 步骤10 | BaseLoadClaimLineService | `preResult(pageLine, full)`, `addPreLine(pageLine, full, loadParams)` |

> 注意: LoadClaimLine 使用特殊 Bean 名称: `@Service(value = "listAllT{XXX}ClaimLinesService")`

### BPM 层模板 (4个文件)

| 文件 | 对应步骤 | 基类 | 钩子方法 |
|------|---------|------|----------|
| `bpm/interface-callback-template.java` | 步骤8 | IBaseCallBackClaimService | - |
| `bpm/impl-callback-template.java` | 步骤8 | BaseCallBackClaimService | `executeExecute()`, `executeEnd()`, `executeDrawBack()`, `executeUndo()` 等 |
| `bpm/interface-submit-template.java` | 步骤9 | IBaseSubmitClaimService | - |
| `bpm/impl-submit-template.java` | 步骤9 | BaseSubmitClaimService | `preResult(full)`, `validate(full, params)`, `loadAll(fullDto, params)` |

### 基类已实现的公共能力速查

#### BaseNewClaimService
- `newClaim()`: 用户信息 → 模板 → 默认值 → preExecute
- `setUserInformation()`, `preResult()`, `setDefaultValues()`, `setVendorInfo()`

#### BaseSaveOrUpdateClaimService (替代已废弃的 BaseSaveClaimService)
- `save()`: 根据claimId判断新增/修改
- `update()`: 查老数据 → 标记修改 → 校验 → before → 保存 → updateClaimLine → after
- `validation()`, `before()→preResult()→preExecute()`, `after()`

#### BaseDeleteClaimService
- `delete()`: 删除主流程（关联删除明细行、附件、影像、付款行等）

#### BaseLoadClaimService
- `load()`: 加载主流程 → loadCommonInfo → loadAllLine → preResult
- 已包含公共信息加载、明细行、附件、影像等

#### BaseSaveClaimLineService
- `saveClaimLine()`: 查报账单 → 币种/汇率 → preExecute → 金额拆分 → 校验 → save → after

#### BaseUpdateClaimLineService
- `updateClaimLine()`: 查报账单 → 查旧行 → 校验 → preExecute → 金额拆分 → save → after
- `clearCrDrSegCode()`: 清除借贷科目段

#### BaseDeleteClaimLineService
- `deleteClaimLine()`: 循环删除（关联数据 → 金额回写 → 批量删除） → after

#### BaseLoadClaimLineService
- `load()`: loadData → processClaimLines(事件链) → preResult
- 事件链: amount → adjustAmount → loanAmount → foreignApplyAmount → dcType → addPreLine

#### BaseCallBackClaimService
- 统一回调框架: execute → integrateBusinessData → 个性方法
- 已实现: executeExecuteRoot, executeExecute, executeDrawBack, executeUndo, executeEnd, executeDelete 等

#### BaseSubmitClaimService
- `submit()` → `before()` → `preResult()` + `validate()`
- `validate()` → validateCommon → loadAll → buildValidationContext → claimValidationOrchestrator

## 迁移步骤详细文档

每个步骤都有独立的详细文档，包含完整的迁移策略、基类能力分析、检查清单和常见坑点，位于 `steps/` 目录下：

| 步骤 | 文件 | 内容 | 核心基类 |
|------|------|------|----------|
| 步骤1 | `steps/step-01-new-head.md` | 新建报账单头迁移策略 | BaseNewClaimService |
| 步骤2 | `steps/step-02-new-line.md` | 新建报账单行迁移策略 | BaseNewClaimLineService |
| 步骤3 | `steps/step-03-save-head.md` | 保存报账单头迁移策略 (Insert+Update合并) | BaseSaveOrUpdateClaimService |
| 步骤4 | `steps/step-04-save-line.md` | 保存/更新报账单行迁移策略 (Save+Update分离) | BaseSaveClaimLineService + BaseUpdateClaimLineService |
| 步骤5 | `steps/step-05-delete-head.md` | 删除报账单头迁移策略 | BaseDeleteClaimService |
| 步骤6 | `steps/step-06-delete-line.md` | 删除报账单行迁移策略 | BaseDeleteClaimLineService |
| 步骤7 | `steps/step-07-load.md` | 加载报账单迁移策略 (多LoadAll合并) | BaseLoadClaimService |
| 步骤8 | `steps/step-08-callback.md` | BPM回调迁移策略 | BaseCallBackClaimService |
| 步骤9 | `steps/step-09-submit.md` | 提交校验迁移策略 | BaseSubmitClaimService |
| 步骤10 | `steps/step-10-load-line.md` | 加载明细行迁移策略 | BaseLoadClaimLineService |

每个文档包含：
- **概述表**: 老代码→新代码映射、基类、钩子方法、模板文件
- **迁移策略**: 分步骤的详细操作指南，含基类流程树
- **检查清单**: 分析阶段→编码阶段→验证阶段的完整checklist
- **常见坑点**: 实际迁移中容易出错的地方
- **参考实现**: 已迁移的T047等参考代码
- **经验记录区**: 预留区域，用于积累每次迁移的实战经验

## 相关参考

- 项目规范：`/ai-spec/rules/agents.md`
- 代码生成器：`/ai-spec/skills/code/claim-generator/`
- 现有模板参考：claim-ptp、claim-eer、claim-otc、claim-base 中的已迁移代码
- 基类实现：`claim-common/src/main/java/com/yili/claim/common/service/claim/service/impl/`
- 行基类实现：`claim-common/src/main/java/com/yili/claim/common/service/line/service/impl/`
- 老代码位置：`yldc-caiwugongxiangpingtai-fsscYR-master/src/`
