# 步骤9：提交校验 (Submit)

## 📋 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `SubmitT{XXX}ClaimService.java` / `SubmitClaimService.java` 中的 T{XXX} 分支 |
| **新代码** | `T{XXX}SubmitClaimServiceImpl.java` |
| **继承基类** | `BaseSubmitClaimService` |
| **接口** | `IT{XXX}SubmitClaimService extends IBaseSubmitClaimService` |
| **核心方法** | `submit(P params)` |
| **可重写钩子** | `preResult(full)`, `validate(full, params)`, `loadAll(fullDto, params)` |
| **模板文件** | `templates/bpm/interface-submit-template.java`, `templates/bpm/impl-submit-template.java` |

---

## 🔄 迁移策略

### 核心概念：提交三阶段

新框架的提交流程分为三个阶段：

```
submit(params)
  └── before(full, params)
      ├── preResult(full)              // 阶段1: 数据预处理
      ├── validate(full, params)       // 阶段2: 链式校验
      │   ├── validateCommon()         //   通用校验
      │   ├── loadAll(fullDto, params) //   加载完整数据
      │   └── claimValidationOrchestrator.validate() // 编排器
      └── return chainValidator        // 返回校验结果
```

**三个阶段的区别**:

| 阶段 | 方法 | 错误处理 | 适用场景 |
|------|------|---------|---------|
| 预处理 | `preResult()` | 抛异常直接中断 | 致命错误、数据修正 |
| 校验 | `validate()` | ChainValidator 收集 | 业务规则校验 |
| 数据加载 | `loadAll()` | 在 validate 内调用 | 校验前加载必要数据 |

### 1. 定位老代码

- `SubmitT{XXX}ClaimService.java`（如果存在）
- 或在通用 `SubmitClaimService.java` 中搜索 T{XXX} 相关分支
- 记录行数和逻辑模块

### 2. 分析老代码

老代码通常包含两类校验：

| 类型 | 内容 | 迁移方式 |
|------|------|----------|
| **前置校验** | 数据完整性、数据修正、致命错误 | 🔧 迁移到 preResult |
| **业务校验** | 金额、发票、预算、承兑、资产等 | 🔧 创建 Validator (在 `validator/` 包) |

### 3. 基类能力速查

`BaseSubmitClaimService` (178行):

```
submit(params)
  ├── 查报账单完整信息
  └── before(full, params):
      ├── preResult(full)                    // ★ 空钩子
      └── validate(full, params):
          ├── validateCommon(full, params)    // 通用校验
          ├── loadAll(fullDto, params)        // ★ 加载数据
          ├── buildValidationContext()        // 构建上下文
          └── claimValidationOrchestrator.validate(context)  // 编排器
```

**基类已注入**:
- `claimService`, `claimValidationOrchestrator`

### 4. 提取需迁移的逻辑

**常见迁移点**:

1. **preResult** - 前置处理:
   - 必填字段检查
   - 默认值填充
   - 致命错误判断

2. **Validator** - 业务校验:
   - 每个业务规则创建一个 `AbstractClaimValidator`
   - 注入到 Spring 容器
   - 编排器自动收集并执行

**Validator 示例**:
```java
@Component
public class T{XXX}AmountValidator extends AbstractClaimValidator {
    @Override
    protected void doValidate(ClaimValidationContext context) {
        // 校验逻辑
        if (条件不满足) {
            addError("错误信息");
        }
    }
}
```

### 5. 编写新代码

1. 基于模板创建接口和实现类
2. 在 preResult() 中实现前置处理
3. 为每个业务规则创建 Validator
4. 通常不需要重写 validate()

---

## ✅ 关键检查点

### 分析阶段
- [ ] 老代码已定位，记录行数
- [ ] 区分前置校验 vs 业务校验
- [ ] 识别所有校验规则

### 编码阶段
- [ ] 接口和实现类已创建
- [ ] preResult 实现前置处理
- [ ] 每个业务规则创建了 Validator
- [ ] Validator 都标注了 `@Component`

### 验证阶段
- [ ] 无编译错误
- [ ] 所有校验规则都能触发
- [ ] 错误信息正确收集和返回

---

## ⚠️ 常见坑点

1. **在 preResult 中写业务校验** - 应该创建 Validator
2. **忘记 @Component** - Validator 必须注入到容器
3. **重写 validate()** - 通常不需要，编排器已处理
4. **混淆错误处理** - preResult 抛异常，Validator 用 addError

---

## 📚 参考实现

- **T047**: `T047SubmitClaimServiceImpl.java`
- **Validator示例**: `T047AmountValidator.java`
- **基类**: `BaseSubmitClaimService.java` (178行)
- **编排器**: `ClaimValidationOrchestrator.java`

---

## 📝 经验记录区

> 每次迁移后补充实战经验

<!-- 格式: [T{XXX}] {日期} {经验描述} -->
- `claimValidationOrchestrator` - 校验编排器（自动发现和执行所有注册的 Validator）

**loadAll 默认实现**:
```java
protected void loadAll(TRmbsClaimPageFullDto fullDto, P params) {
    String itemId = params.getItemId();
    IBaseLoadClaimService loadService = SpringUtil.bean("loadAll", itemId, "ClaimService");
    if (loadService != null) {
        TRmbsClaimPageFullDto pageFullDto = loadService.load(params, user);
        BeanUtil.copyProperties(pageFullDto, fullDto);
    }
}
```

### 第四步：校验器架构

新框架使用 **校验编排器** 模式，每个校验规则是一个独立的 Validator：

```
ClaimValidationOrchestrator
  ├── 通用校验器 (basic/bank/contract/...)
  ├── 领域校验器 (asset/invoice/payment/...)
  ├── 规则引擎校验器 (rule/)
  ├── 单据特有校验器 (specific/)
  └── T{XXX}SpecificValidator     // 待新增的T{XXX}特有校验
```

**如果需要新增 T{XXX} 特有的校验规则**:
1. 创建新的 Validator 类，继承 `AbstractClaimValidator`
2. 通过注解注册到编排器
3. 编排器会自动发现并执行

### 已有校验器完整清单

> **路径**: `claim-common/claim-common-service/src/main/java/com/yili/claim/common/service/claim/external/submit/validation/validators/`
> 
> 迁移时**必须先对照此清单**，确认老代码校验逻辑是否已被覆盖，避免重复实现。

#### accounting/ （会计科目，1个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `LedgerAccountCrossValidator` | 1350 | 特殊会计科目交叉验证 | 会计科目交叉校验 |

#### asset/ （资产相关，11个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `LineAndAssetAmountMatchValidator` | 205 | 资产页签与明细行金额匹配 | 明细行与资产页签金额一致性 |
| `AssetLineAmountValidator` | 210 | 资产页签与明细行金额校验 | 资产金额相关校验 |
| `AssetDataFreshnessValidator` | 230 | 资产数据最新性校验 | 资产数据是否为最新 |
| `AssetDataTimeValidator` | 235 | 资产更新时间校验 | 资产更新时间校验 |
| `AssetOaRelationValidator` | 235 | 资产OA购置验收流程关联校验 | OA流程关联 |
| `AssetDataNewestValidator` | 240 | 资产原值最新性校验 | 资产原值是否为最新 |
| `AssetReduceValidator` | 240 | 资产减少页签互斥校验 | 资产减少互斥 |
| `AssetValidityValidator` | 250 | 资产有效性校验 | 资产是否有效 |
| `AssetChangeDuplicateValidator` | 260 | 资产变更分配行重复数据校验 | 变更行去重 |
| `AssetDisplayFlagValidator` | 1111 | 资产显示标识变更校验 | 显示标识变更 |
| `AssetSegmentValidator` | 3210 | 资产费用八段值状态校验 | 八段码状态 |

#### bank/ （银行相关，2个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `BankInternalCompanySegmentValidator` | 146 | 银行内部/关联现金流量公司间段校验 | 公司间段校验 |
| `BankOuAccountConsistencyValidator` | 147 | 银行OU与账户对应关系一致性校验 | 银行OU一致性 |

#### basic/ （基础通用，8个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `OuConsistencyValidator` | 5 | OU信息一致性校验 | OU基础信息、银行/部门/供应商/合同/核销OU一致性 |
| `InvoiceTaxValidator` | 55 | 税率与税金校验 | 税率格式、T009进项税转出、税额非空等 |
| `ClaimStatusValidator` | 100 | 报账单状态与删除标识校验 | 状态/删除标识 |
| `BusinessClassValidator` | 120 | 业务小类必填校验 | 明细行业务小类(ITEM3_ID)非空 |
| `SegmentCodeValidator` | 140 | 段值有效性校验 | 费用承担部门段/子目段/产品段/T040税率段 |
| `DepartmentAttributeAndBusinessClassMatchValidator` | 145 | 部门属性与业务小类匹配校验 | groupAttributeId与item3Id匹配 |
| `GlDateValidator` | 190 | GL日期校验 | GL日期（老代码为空方法） |
| `ClaimAmountValidator` | 195 | 报账单金额校验 | 金额非负、T007付款金额公式校验 |

#### contract/ （合同相关，2个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `LoanContractDeletedValidator` | 49 | 借款合同删除校验 | 借款合同是否已删除 |
| `ContractValidator` | 185 | 合同校验 | 合同信息校验 |

#### dashboard/ （驾驶舱规则，5个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `DashboardRule1And2Validator` | - | 驾驶舱规则1和2 | 关账驾驶舱期间控制 |
| `DashboardRule3Validator` | - | 驾驶舱规则3校验 | 关账驾驶舱到单时间控制 |
| `DashboardRule6Validator` | - | 驾驶舱规则6 | 工作项完成时间控制 |
| `DashboardRule7Validator` | - | 驾驶舱规则7 | 单据截止时间控制 |
| `DashboardTaskRuleValidator` | - | 驾驶舱任务规则校验器 | 编排调用Rule1-7 |

#### document/ （文档相关，3个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `OfdDocumentValidator` | 1300 | OFD文档校验 | OFD格式文档校验 |
| `PdfPageCountValidator` | 1310 | PDF页数校验 | PDF页数限制校验 |
| `PdfPageValidator` | 1311 | PDF页码校验 | PDF页码校验 |

#### image/ （影像相关，4个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `OcrImageInvoicePoolValidator` | 27 | OCR影像发票池查询校验 | OCR识别结果与发票池匹配 |
| `EimImageValidator` | 118 | EIM影像校验 | EIM影像验真状态校验 |
| `ImageUserBlacklistValidator` | 119 | 影像用户黑名单校验 | 影像用户黑名单 |
| `OcrImageValidator` | 130 | OCR与影像完整性校验 | OCR识别与影像完整性 |

#### invoice/ （发票相关，7个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `InvoiceRedBlueValidator` | 23 | 红票蓝票校验 | 红票蓝票配对校验 |
| `InvoiceRedMixedValidator` | 24 | 红字发票混合报账校验 | 红字发票混合报账限制 |
| `InvoiceOtherPureAmountValidator` | 25 | 税金页签其他发票金额非空校验 | 其他发票金额非空 |
| `InvoiceDuplicateValidator` | 50 | APP发票防重校验（税金页签内部防重） | 税金页签发票防重 |
| `ElectronicInvoiceValidator` | 165 | 电子发票校验 | 电子发票校验 |
| `VatInvoiceValidator` | 166 | 增值税发票校验 | 增值税发票校验 |
| `InputTaxTransferValidator` | 6 | 进项税转出金额校验 | 进项税转出金额 |

#### invoicepool/ （发票池，2个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `InvoiceLibraryValidator` | 26 | 发票池校验 | 发票池信息校验 |
| `TaxInvoiceLibraryOccupationValidator` | 27 | 税票发票池占用校验器 | 税票发票池占用 |

#### payment/ （付款计划，14个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `PaymentPlanAmountValidator` | 180 | 付款计划校验 | 付款计划金额综合校验 |
| `BondFundPaymentPlanValidator` | 210 | 质保金付款计划校验 | 质保金专用 |
| `PaymentPlanAndInvoiceWriteOffAmountMatchValidator` | 420 | 付款计划与发票核销金额校验 | 付款计划与发票核销匹配 |
| `PaymentPlanAndTaxAmountMatchValidator` | 420 | 付款计划与税金页签金额匹配校验（T059） | T059支付租金专用 |
| `LineAndPaymentPlanAmountMatchValidator` | 430 | 明细行与付款计划金额匹配校验 | 仅 T059（初始直接费用/台账未生效前支付租金且预付款）与 T064 |
| `PaymentPlanCalculationValidator` | 1256 | 付款计划-计算校验 | 付款计划计算校验 |
| `PayChangeLineAmountValidator` | - | 付款变更行金额校验 | 付款变更行金额 |
| `PaymentPlanConsistencyValidator` | - | 付款计划一致性校验 | 付款计划一致性 |
| `PaymentPlanCreditNoteValidator` | - | 付款计划-贷项通知单校验 | 贷项通知单 |
| `PaymentPlanDateValidator` | - | 付款计划-日期校验 | 付款日期 |
| `PaymentPlanExclusionValidator` | - | 付款计划互斥校验 | T034/T039/T049/T069/T044/T033/T023/T050互斥 |
| `PaymentPlanMilkVendorValidator` | - | 付款计划-奶户付款校验 | 奶户专用 |
| `PaymentPlanPayTypeValidator` | - | 付款计划-支付方式校验 | 支付方式 |
| `VendorControlRangeValidator` | - | 供应商控制范围校验 | 供应商控制范围 |

#### rule/ （规则引擎，5个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `VendorRuleEngineValidator` | 1100 | 供应商规则引擎校验 | 供应商规则引擎 |
| `ReceiptRuleEngineValidator` | 1120 | 收款规则引擎校验 | 收款规则引擎 |
| `VendorSiteRuleEngineValidator` | 1120 | 供应商地点规则引擎校验 | 供应商地点规则引擎 |
| `ProjectRuleEngineValidator` | 1140 | 项目规则引擎校验 | 项目规则引擎 |
| `ClaimLineRuleEngineValidator` | 1160 | 明细行规则引擎校验 | 明细行规则引擎 |

#### specific/ （单据特有，13个）

| 类名 | Order | 校验名称 | 适用单据 |
|------|-------|---------|----------|
| `T001TravelLineValidator` | 700 | T001差旅行信息校验器 | T001 |
| `T001TravelAmountValidator` | 705 | T001差旅明组金额校验器 | T001 |
| `T007InvoiceDuplicateValidator` | 500 | T007发票重复校验 | T007 |
| `T007VendorSiteMatchValidator` | 501 | T007供应商地点匹配校验 | T007 |
| `T027T012LineAmountValidator` | 520 | T027/T012明细行金额校验 | T027/T012 |
| `T032T031T019T028T900LinkClaimValidator` | 530 | T032/T031/T019/T028/T900关联报账单校验 | T032/T031/T019/T028/T900 |
| `T035VendorValidator` | - | T035供应商信息校验 | T035 |
| `T003VendorInfoValidator` | 1210 | T003借款单供应商信息完整性校验 | T003 |
| `T044AcceptanceDetailValidator` | - | T044承兑汇票明细完整性校验器 | T044 |
| `T044BillUniquenessValidator` | - | T044票据占用唯一性校验器 | T044 |
| `T044EndorsementValidator` | - | T044背书申请状态校验器 | T044 |
| `T044PaymentMethodValidator` | - | T044统筹支付方式校验器 | T044 |
| `T049T069NoTicketToTicketValidator` | - | T049/T069无票转有票校验 | T049/T069 |

#### tax/ （税金相关，2个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `TaxSubtractionAmountChangeValidator` | 22 | 税金核减金额变更校验 | 税金核减变更 |
| `LineAndTaxAmountMatchValidator` | 410 | 明细行与税金页签金额匹配校验 | 明细行与税金匹配 |

#### tpm/ （TPM，1个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `TpmAmountValidator` | 31 | TPM综合校验 | T009/T011/T007等TPM金额校验 |

#### writeoff/ （核销相关，6个）

| 类名 | Order | 校验名称 | 说明 |
|------|-------|---------|------|
| `InvoiceWriteOffSingleInProgressValidator` | 29 | 发票核销只有一单在途校验 | 发票核销在途唯一性 |
| `MandatoryWriteOffPrePayDraftValidator` | 300 | 预付款强制核销校验（起草环节） | 起草环节预付款核销 |
| `MandatoryWriteOffPrePayProcessValidator` | 310 | 预付款强制核销校验（流程环节） | 流程环节预付款核销 |
| `MandatoryWriteOffInvoiceDraftValidator` | 320 | 发票强制核销校验（起草环节） | 起草环节发票核销 |
| `MandatoryWriteOffInvoiceProcessValidator` | 330 | 发票强制核销校验（流程环节） | 流程环节发票核销 |
| `ClaimVendorConsistencyValidator` | 1000 | 报账单与核销报账单供应商一致性校验 | 核销供应商一致性 |

> **合计: 86 个校验器** (按 Order 值从小到大执行)

### 第五步：选择正确的重写方式

**场景1**: 只需要数据预处理（无特殊校验）
```java
@Override
protected void preResult(TRmbsClaimPageFullDto full) {
    // 数据修正或前置检查
}
```

**场景2**: 需要额外校验规则
```java
@Override
public <P extends TRmbsClaimPageDto> ChainValidator validate(TRmbsClaimPageFullDto full, P params) {
    // 调用基类校验
    ChainValidator validator = super.validate(full, params);
    // 追加 T{XXX} 特有校验
    // ...
    return validator;
}
```

**场景3**: 需要自定义数据加载（性能优化）
```java
@Override
protected <P extends TRmbsClaimPageDto> void loadAll(TRmbsClaimPageFullDto fullDto, P params) {
    // 自定义加载逻辑（如提前加载某些数据避免N+1查询）
    super.loadAll(fullDto, params);
}
```

## 检查清单

### 分析阶段
- [ ] 找到老代码中 T{XXX} 的提交校验逻辑
- [ ] 区分"前置校验"和"业务校验"
- [ ] 标记哪些校验已被通用 Validator 覆盖
- [ ] 标记需要新增的 T{XXX} 特有校验
- [ ] 确认 loadAll 是否需要自定义（性能问题）

### 编码阶段
- [ ] 创建接口 `IT{XXX}SubmitClaimService extends IBaseSubmitClaimService`
- [ ] 创建实现类 `T{XXX}SubmitClaimServiceImpl extends BaseSubmitClaimService`
- [ ] 类上添加 `@Slf4j` 和 `@Service`
- [ ] 如有前置处理：重写 `preResult(TRmbsClaimPageFullDto full)`
- [ ] 如有额外校验：重写 `validate()` 或创建新的 Validator
- [ ] 如需性能优化：重写 `loadAll()`
- [ ] 注释标注原代码行数

### 验证阶段
- [ ] 无编译错误
- [ ] 所有老代码的校验规则都有对应处理
- [ ] preResult 中的错误抛异常（直接中断）
- [ ] validate 中的错误走 ChainValidator（收集所有错误）
- [ ] 没有重复已有 Validator 的校验逻辑
- [ ] import语句完整

## 常见坑点

1. **preResult vs validate 区分**: `preResult` 中抛异常会直接中断提交；`validate` 中通过 `ChainValidator` 收集所有错误后统一返回
2. **校验编排器**: 新框架通过 `ClaimValidationOrchestrator` 自动发现所有注册的 Validator，不需要在 Submit 中手动调用每个校验
3. **loadAll 性能**: 默认的 loadAll 会通过 SpringUtil.bean 找到 Load 服务加载全量数据，如果数据量大需要优化
4. **ChainValidator**: 使用 `ChainValidator` 而不是直接抛异常，这样前端可以一次看到所有校验错误
5. **不要在 preResult 中做业务校验**: preResult 适合数据修正和致命检查，业务规则校验应该走 Validator

## 参考实现

- T047: `claim-otc/.../t047/bpm/impl/T047SubmitClaimServiceImpl.java` - 含 preResult + validate 重写
- 基类: `BaseSubmitClaimService.java` (178行)

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
- 工作流常用枚举类型ClaimProcessEnum
- validate开头的方法以前是在老代码SubmitClaimService里面存在的方法，帮忙增加组件到txxx/validator目录下
- 等待父类方法迁移的方法按照父类方法名，在父类中创建空方法，写上//TODO，后面统一迁移，保持和以前方法名一样
- 分步进行，每步立即生成代码，以免浪费Credits
<!--
格式：
- [T{XXX}] {日期} {经验描述}
示例：
- [T047] 2025-12-28 T047的承兑汇票校验需要新建独立的Validator
- [T014] 2025-12-28 T014的preResult中需要修正isTransMode字段
-->
