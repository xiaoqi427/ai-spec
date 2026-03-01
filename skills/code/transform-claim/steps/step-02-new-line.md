# 步骤2：新建报账单行 (New Claim Line)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `NewT{XXX}ClaimLineService.java` |
| **新代码** | `T{XXX}NewClaimLineServiceImpl.java` |
| **继承基类** | `BaseNewClaimLineService` |
| **接口** | `IT{XXX}NewClaimLineService extends IBaseNewClaimLineService` |
| **核心方法** | `newClaimLine(Long claimId)` |
| **可重写钩子** | `preExecute(TRmbsClaimLineDto claimLineDto, TRmbsClaimBaseDto claim)` |
| **模板文件** | `templates/line/interface-new-template.java`, `templates/line/impl-new-template.java` |

## 迁移策略

### 第一步：定位老代码

1. 找到 `NewT{XXX}ClaimLineService.java`
2. 记录文件总行数

### 第二步：分析老代码 execute() 方法

老代码通常包含：

```
execute() {
    // 模块A: 查报账单信息 → 基类已处理
    // 模块B: 创建ClaimLine对象、设claimId → 基类已处理
    // 模块C: 设币种CNY、汇率1 → 基类已处理
    // 模块D: 设公司ID → 基类已处理
    // 模块E: T{XXX}特有字段初始化 → 需要迁移到 preExecute()
    // 模块F: 设费用部门（根据部门属性、item2Id判断） → 基类已处理
    // 模块G: 设BU段 → 基类已处理
    // 模块H: 设部门属性（groupAttributeId） → 基类已处理
    // 模块I: 设项目段（apProjectSeg） → 基类已处理
    // 模块J: 设申请日期、发票类型、组织ID等 → 基类已处理
}
```

### 第三步：对照基类已实现能力

`BaseNewClaimLineService.newClaimLine(Long claimId)` 已实现的完整流程（183行）：

```
newClaimLine(claimId)
  ├── 查报账单信息: claimDoService.findByClaimId(claimId)
  ├── 创建 TRmbsClaimLineDto
  ├── 设 claimId, currency(CNY), exchangeRate(1), compId
  ├── preExecute(claimLineDto, claim)     // ★ 空钩子 → 子类重写点
  ├── 设费用部门段（根据 sysGroup + item2Id 各种分支判断）
  ├── 设BU段（buSegCode, buSeg）
  ├── 设部门属性（groupAttributeId，含 T020/T035、多种itemId的特殊处理）
  ├── 设项目段（apProjectSeg，含在建工程类、ConstructionProject配置）
  ├── 设默认值（T002-T032等 groupAttributeId=0, costSeg=不分明细）
  ├── 设 applyDate, invoiceType, orgId, costAssumeDepartment
  ├── 设 T020的accountedOrgId/accountedCompId等
  ├── 设 T019的crApProjectSegCode
  └── 设 T030/T057的claimCreateDate
```

**注意**: 基类已处理了大量的 itemId 判断逻辑，覆盖面很广。

### 第四步：提取需迁移的逻辑

对比老代码和基类代码，只迁移基类**未覆盖**的 T{XXX} 特有逻辑到 `preExecute()`。

常见需要迁移的逻辑：
- 特有的字段初始化（如T047的退款相关字段）
- 特殊的默认值覆盖
- 从其他Service查询并赋值的逻辑

**重要**: 很多单据类型的 NewClaimLine 完全被基类覆盖，此时实现类可以是空的（如T047）。

### 第五步：编写新代码

1. 创建接口和实现类
2. 如有特有逻辑，在 `preExecute()` 中实现
3. 如无特有逻辑，实现类保持空（仅继承基类）

## 检查清单

### 分析阶段
- [ ] 找到老代码文件并记录总行数
- [ ] 逐行对比老代码与 BaseNewClaimLineService（183行）
- [ ] 标记基类已覆盖的逻辑（通常是大部分）
- [ ] 标记 T{XXX} 特有的逻辑
- [ ] 确认 preExecute 的调用时机（在费用部门/BU段/部门属性之前）

### 编码阶段
- [ ] 创建接口 `IT{XXX}NewClaimLineService extends IBaseNewClaimLineService`
- [ ] 创建实现类 `T{XXX}NewClaimLineServiceImpl extends BaseNewClaimLineService`
- [ ] 类上添加 `@Service` 注解
- [ ] 如有特有逻辑：重写 `preExecute(TRmbsClaimLineDto claimLineDto, TRmbsClaimBaseDto claim)`
- [ ] preExecute 必须返回 `claimLineDto`
- [ ] 注释标注原代码行数

### 验证阶段
- [ ] 无编译错误
- [ ] 没有重复基类的 itemId 判断逻辑
- [ ] 基类 preExecute 调用时机正确理解（在基类其他逻辑之前）
- [ ] import语句完整

## 常见坑点

1. **大量重复**: 基类 `BaseNewClaimLineService` 已包含非常多 itemId 的特殊处理，老代码中大部分逻辑已被基类覆盖
2. **preExecute 时机**: `preExecute` 在基类中是在 **费用部门、BU段、部门属性之前** 调用的，所以子类可以在此设置后续逻辑需要的前置数据
3. **空实现是正确的**: 如果老代码的所有逻辑都被基类覆盖了，空实现就是正确答案（参考T047）
4. **参数类型注意**: `preExecute` 的 claim 参数类型是 `TRmbsClaimBaseDto`，不是 `TRmbsClaimPageDto`

## 参考实现

- T047: `T047NewClaimLineServiceImpl.java` (18行) - 空实现，基类已满足
- 基类: `BaseNewClaimLineService.java` (183行) - 需仔细阅读理解全部逻辑

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
<!--
格式：
- [T{XXX}] {日期} {经验描述}
-->
