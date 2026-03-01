# 步骤4：保存报账单行 (Save Claim Line) + 更新报账单行 (Update Claim Line)

## 概述

**注意**: 与头层不同，行层的 Save 和 Update 在新框架中是**分离的两个基类**。

| 操作 | 老代码 | 新代码 | 继承基类 |
|------|--------|--------|---------|
| **保存（新增行）** | `SaveT{XXX}ClaimLineService.java` | `T{XXX}SaveClaimLineServiceImpl.java` | `BaseSaveClaimLineService` |
| **更新（修改行）** | `UpdateT{XXX}ClaimLineService.java` | `T{XXX}UpdateClaimLineServiceImpl.java` | `BaseUpdateClaimLineService` |

### Save 行接口

| 项目 | 内容 |
|------|------|
| **接口** | `IT{XXX}SaveClaimLineService extends IBaseSaveClaimLineService` |
| **核心方法** | `saveClaimLine(TRmbsClaimLineDto claimLineDto)` |
| **可重写钩子** | `preExecute(claim, claimLineDto)`, `after(claim, claimLineDto)` |
| **模板文件** | `templates/line/interface-save-template.java`, `templates/line/impl-save-template.java` |

### Update 行接口

| 项目 | 内容 |
|------|------|
| **接口** | `IT{XXX}UpdateClaimLineService extends IBaseUpdateClaimLineService` |
| **核心方法** | `updateClaimLine(TRmbsClaimLineDto claimLineDto)` |
| **可重写钩子** | `preExecute(claim, claimLineDto)`, `clearCrDrSegCode(claim, claimLineDto)`, `after(claim, claimLineDto)` |
| **模板文件** | `templates/line/interface-update-template.java`, `templates/line/impl-update-template.java` |

## 迁移策略

### 第一步：定位老代码

1. 找到 `SaveT{XXX}ClaimLineService.java`
2. 找到 `UpdateT{XXX}ClaimLineService.java`
3. 分别记录行数

### 第二步：分析 Save（新增行）老代码

**SaveT{XXX}ClaimLineService.execute()** 通常包含：
```
execute() {
    // 模块A: 查报账单信息 → 基类已处理
    // 模块B: 设币种/汇率 → 基类已处理 (非T057设CNY)
    // 模块C: 八段信息处理 → 基类 preExecute 中 super.preExecute() 已处理
    // 模块D: 发票校验/银行托收 → 需要迁移到 preExecute
    // 模块E: 智能报账金额拆分 → 基类已处理
    // 模块F: T049/T069校验 → 基类已处理
    // 模块G: 科目段/子目段/承兑台账 → 基类已处理
    // 模块H: save → 基类已处理
    // 模块I: 手机费额度 → 基类已处理
    // 模块J: processAmount → 基类 after 已处理
}
```

### 第三步：对照 BaseSaveClaimLineService 已实现能力 (274行)

```
saveClaimLine(claimLineDto)
  ├── 查报账单: claimDoService.findByClaimId()
  ├── 设币种/汇率 (非T057)
  ├── preExecute(claim, claimLineDto)           // ★ 继承自 ClaimLineBaseService
  │   └── super.preExecute() → 八段信息处理
  ├── 智能报账金额拆分 (smartAccountAmount)
  ├── T049/T069校验 (updateT049T069TransFlow)
  ├── 项目段处理 (processApProjectSeg)
  ├── 科目段校验 (validateSubjectField)
  ├── T020/T035子目段 (processSubItemSeg)
  ├── T014承兑台账 (processAcptBillBiz)
  ├── claimLineDoService.save(claimLineDto)
  ├── 手机费额度 (executeSaveMobilefeeQuota)
  └── after(claim, claimLineDto)                // ★ 默认调 processAmount
```

### 第四步：对照 BaseUpdateClaimLineService 已实现能力 (507行)

```
updateClaimLine(claimLineDto)
  ├── 查报账单和旧行数据
  ├── 设币种/汇率 (非T057)
  ├── preExecute(claim, claimLineDto)           // ★ 子类重写点
  │   ├── clearCrDrSegCode(claim, claimLineDto) // 清借贷方科目段
  │   └── super.preExecute() → 八段信息处理
  ├── 智能报账金额拆分
  ├── T049/T069校验
  ├── 科目段校验
  ├── 付款计划相关 (processLedgerPayList4ClaimLine)
  ├── 保存
  ├── 发票核销更新 (updateClaimInvoiceRelationReserved2)
  ├── T049/T069交易流水 (updateT049AndT069TransFlow)
  └── after(claim, claimLineDto)                // ★ 默认调 processAmount
```

**Update 比 Save 多的能力**:
- `clearCrDrSegCode()`: 清除借贷方科目段代码
- 付款计划相关处理
- 发票核销更新
- T049/T069交易流水
- CVT记录处理

### 第五步：提取需迁移的逻辑

**Save 行常见迁移逻辑**:
- 发票校验逻辑
- 银行托收逻辑
- 金额特殊处理
- flexOu/vmilineId 等特有字段

**Update 行常见迁移逻辑**:
- 与 Save 行类似的字段处理
- 可能需要自定义 `clearCrDrSegCode` 逻辑
- 可能需要自定义 `after` 来改变金额重算行为

## 检查清单

### Save 行分析阶段
- [ ] 找到 SaveT{XXX}ClaimLineService.java
- [ ] 逐行分析 execute() 方法
- [ ] 对照 BaseSaveClaimLineService (274行)
- [ ] 标记基类已覆盖的逻辑
- [ ] 标记需要迁移到 preExecute() 的逻辑
- [ ] 确认 preExecute 中是否需要调 super.preExecute()（八段信息）

### Update 行分析阶段
- [ ] 找到 UpdateT{XXX}ClaimLineService.java
- [ ] 逐行分析 execute() 方法
- [ ] 对照 BaseUpdateClaimLineService (507行)
- [ ] 标记是否需要自定义 clearCrDrSegCode
- [ ] 标记需要迁移到 preExecute() 的逻辑
- [ ] 确认 after 是否需要自定义金额重算

### 编码阶段 - Save 行
- [ ] 创建接口 `IT{XXX}SaveClaimLineService extends IBaseSaveClaimLineService`
- [ ] 创建实现类 `T{XXX}SaveClaimLineServiceImpl extends BaseSaveClaimLineService`
- [ ] 重写 `preExecute(TRmbsClaimBaseDto claim, TRmbsClaimLineDto claimLineDto)`
- [ ] 如需八段信息处理：在 preExecute 中调 `super.preExecute(claim, claimLineDto)`
- [ ] 如需自定义金额重算：重写 `after(claim, claimLineDto)`

### 编码阶段 - Update 行
- [ ] 创建接口 `IT{XXX}UpdateClaimLineService extends IBaseUpdateClaimLineService`
- [ ] 创建实现类 `T{XXX}UpdateClaimLineServiceImpl extends BaseUpdateClaimLineService`
- [ ] 重写 `preExecute(TRmbsClaimBaseDto claim, TRmbsClaimLineDto claimLineDto)`
- [ ] 基类 preExecute 已含 clearCrDrSegCode + super.preExecute，如需自定义则重写

### 验证阶段
- [ ] Save 和 Update 分别编译无错
- [ ] 没有重复基类的八段信息处理
- [ ] processAmount 金额重算逻辑正确
- [ ] import语句完整

## 常见坑点

1. **行层 Save 和 Update 不合并**: 不同于头层，行层是分开的两个基类，必须分别创建
2. **preExecute 继承链**: `ClaimLineBaseService.preExecute()` 处理八段信息，如果子类重写了 preExecute，需要决定是否调 `super.preExecute()`
3. **after 金额重算**: 基类默认在 after 中调 `processAmount`，如果某些 T{XXX} 有自定义金额逻辑（如T047），需要重写 after
4. **T047 Save 行参考**: preExecute 中含发票校验、银行托收、金额处理、flexOu、vmilineId
5. **clearCrDrSegCode**: Update 基类的 preExecute 会先调 clearCrDrSegCode 清除借贷方代码，再调 super.preExecute 重新处理八段

## 参考实现

- T047 Save: `T047SaveClaimLineServiceImpl.java` - preExecute含发票校验+银行托收+金额+flexOu
- T047 Update: `T047UpdateClaimLineServiceImpl.java` - preExecute重写
- T047 Delete: `T047DeleteClaimLineServiceImpl.java` - 自定义金额重算
- 基类 Save: `BaseSaveClaimLineService.java` (274行)
- 基类 Update: `BaseUpdateClaimLineService.java` (507行)

## 经验记录区
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
- 
> 此区域用于记录实际迁移过程中发现的经验和教训。

<!--
格式：
- [T{XXX}] {日期} {经验描述}
-->
