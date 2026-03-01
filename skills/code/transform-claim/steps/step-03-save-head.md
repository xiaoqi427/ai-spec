# 步骤3：保存报账单头 (Save/Update Claim Head)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码 (Insert)** | `InsertT{XXX}ClaimService.java` |
| **老代码 (Update)** | `UpdateT{XXX}ClaimService.java` |
| **新代码** | `T{XXX}SaveClaimServiceImpl.java` (合并Insert+Update) |
| **继承基类** | `BaseSaveOrUpdateClaimService` (注意: `BaseSaveClaimService` 已废弃) |
| **接口** | `IT{XXX}SaveClaimService extends IBaseSaveClaimService` |
| **核心方法** | `save(P params, UserObjectFullDto user)` |
| **可重写钩子** | `preExecute`, `fillValue`, `after`, `insertClaimLineFromClaim`, `updateClaimLineFromClaim`, `processClaimAmount` |
| **模板文件** | `templates/head/interface-save-template.java`, `templates/head/impl-save-template.java` |

## 迁移策略

### 关键变更：两个Service合并为一个

**老框架**: `InsertT{XXX}ClaimService` + `UpdateT{XXX}ClaimService` 分离
**新框架**: `BaseSaveOrUpdateClaimService` 统一处理，通过 `claimId == null` 判断是新增还是更新

```
save(params, user)
  ├── claimId != null → update(params, user)    // 更新流程
  └── claimId == null → super.save(params, user) // 新增流程
```

### 第一步：定位老代码

1. 找到 `InsertT{XXX}ClaimService.java`（新增逻辑）
2. 找到 `UpdateT{XXX}ClaimService.java`（更新逻辑）
3. 分别记录行数

### 第二步：分析老代码逻辑模块

**InsertT{XXX}ClaimService.execute()** 通常包含：
```
execute() {
    // 模块A: 基础数据设置 (createUser, date等) → 基类已处理
    // 模块B: 模板信息、大类小类校验 → 基类已处理
    // 模块C: 版本号设置 → 基类已处理
    // 模块D: 流程状态、单号生成 → 基类已处理
    // 模块E: 付款计划级联 → 基类 after (claimCascadeUpdateService) 已处理
    // 模块F: T{XXX}特有的Insert逻辑 → 需要迁移到 preExecute/fillValue
}
```

**UpdateT{XXX}ClaimService.execute()** 通常包含：
```
execute() {
    // 模块A: 查旧数据、版本校验 → 基类已处理
    // 模块B: 流程状态校验 → 基类已处理
    // 模块C: 核减金额变化检测 → 基类 checkChange 已处理
    // 模块D: 不核销说明 → 基类 fillVerifInstructions 已处理
    // 模块E: 进项税转出信息 → 基类 fillVerifRatioAndIsArcAndIsTaxAndIsRefund 已处理
    // 模块F: T{XXX}特有的Update逻辑 → 需要迁移到 preExecute/fillValue
}
```

### 第三步：对照基类继承链已实现能力

继承链: `BaseSaveOrUpdateClaimService` → `BaseSaveClaimService` → `ClaimBaseService`

**BaseSaveOrUpdateClaimService** 已实现 (371行)：

```
save(params, user)
  ├── [Insert流程] super.save():
  │   ├── validation(full, claim, null, user)  // 模板+版本+流程校验
  │   ├── before(full, claim, null, params, user):
  │   │   ├── checkChange()                     // 核减金额变化检测
  │   │   └── preResult():
  │   │       ├── updateByUi()                  // 前端数据同步
  │   │       ├── fillValue()                   // ★ 子类可重写
  │   │       └── preExecute()                  // ★ 子类可重写
  │   ├── claimDoService.save(claim)
  │   └── after():
  │       ├── insertClaimLineFromClaim()        // ★ 子类可重写(新增时插入行)
  │       └── claimCascadeUpdateService.cascadeUpdate() // 级联更新
  │
  └── [Update流程] update():
      ├── 查旧数据 oldClaim
      ├── validation(full, claim, oldClaim, user) // 含流程校验
      ├── before(full, claim, oldClaim, params, user)
      ├── claimDoService.save(claim)
      ├── updateClaimLineFromClaim()             // ★ 子类可重写
      ├── after()
      └── processClaimAmount()                   // ★ 子类可重写(T015专用)
```

**基类已覆盖的逻辑（不需要迁移）**：
- 创建/更新的路由判断
- 基础数据校验（模板、版本号）
- 流程校验（环节、处理人）
- 核减金额变化检测
- 不核销说明填充
- 进项税转出信息
- 付款计划级联
- 单号生成、版本号管理
- 锁报账单

### 第四步：选择正确的钩子方法

| 钩子方法 | 适用场景 | 参数 |
|----------|---------|------|
| `preExecute()` | T{XXX}特有的字段赋值（Insert和Update都执行） | `(full, claim, oldClaim, params, user)` |
| `fillValue()` | 重写默认值填充逻辑（需先调 `super.fillValue()`） | `(claim, oldClaim, params, full, user)` |
| `after()` | 保存后的额外操作 | `(full, claim, oldClaim, params, user)` |
| `insertClaimLineFromClaim()` | 新增保存时自动插入明细行 | `(full, claim, user)` |
| `updateClaimLineFromClaim()` | 更新保存时更新明细行 | `(full, claim, user)` |
| `processClaimAmount()` | 特殊金额处理（如T015） | `(claim)` |

### 第五步：合并 Insert + Update 逻辑

1. 两者共有的逻辑 → 放 `preExecute()` 或 `fillValue()`
2. 仅 Insert 有的逻辑 → 在 `preExecute()` 中判断 `params.getNewClaim()` 或放 `insertClaimLineFromClaim()`
3. 仅 Update 有的逻辑 → 在 `preExecute()` 中判断 `!params.getNewClaim()` 或放 `updateClaimLineFromClaim()`

## 检查清单

### 分析阶段
- [ ] 找到 Insert 和 Update 两个老代码文件
- [ ] 逐行分析 Insert 的 execute() 方法
- [ ] 逐行分析 Update 的 execute() 方法
- [ ] 对比两者，标记共有逻辑和独有逻辑
- [ ] 对照基类继承链（BaseSaveOrUpdateClaimService → BaseSaveClaimService → ClaimBaseService）
- [ ] 确认哪些老逻辑已被基类覆盖
- [ ] 确认是否需要 fillValue 还是 preExecute

### 编码阶段
- [ ] 创建接口 `IT{XXX}SaveClaimService extends IBaseSaveClaimService`
- [ ] 创建实现类 `T{XXX}SaveClaimServiceImpl extends BaseSaveOrUpdateClaimService`
- [ ] 类上添加 `@Slf4j` 和 `@Service`
- [ ] 选择正确的钩子方法重写
- [ ] 如果重写 `fillValue()`，必须先调 `super.fillValue()`
- [ ] Insert独有逻辑判断 `params.getNewClaim()` 或放 `insertClaimLineFromClaim`
- [ ] Update独有逻辑判断 `!params.getNewClaim()` 或放 `updateClaimLineFromClaim`
- [ ] 每段逻辑标注原代码行数（两个文件分别标注）
- [ ] 需要注入的Service都用 `@Resource` 声明

### 验证阶段
- [ ] 无编译错误
- [ ] Insert老代码每一行都有对应处理
- [ ] Update老代码每一行都有对应处理
- [ ] 继承 `BaseSaveOrUpdateClaimService` 而不是已废弃的 `BaseSaveClaimService`
- [ ] 没有重复基类已实现的逻辑
- [ ] import语句完整

## 常见坑点

1. **继承错误的基类**: 必须用 `BaseSaveOrUpdateClaimService`，`BaseSaveClaimService` 已标记 `@Deprecated`
2. **忽略合并**: Insert和Update的共有逻辑只需写一次，放在 `preExecute()` 中
3. **fillValue vs preExecute**: `fillValue` 在 `preExecute` 之前执行，如果需要覆盖基类的值填充用 `fillValue`，如果是额外赋值用 `preExecute`
4. **忘记调 super**: 重写 `fillValue()` 时必须先调 `super.fillValue()`，否则会丢失基类的默认值设置
5. **老代码中的付款计划**: 老代码经常有 cascadePayList 逻辑，基类 after 中已经通过 `claimCascadeUpdateService.cascadeUpdate()` 处理
6. **isTransMode/银行现金流**: 这类 T{XXX} 特有的字段填充是需要迁移的典型代码（参考T014迁移经验）

## 参考实现

- T047: `claim-otc/.../t047/head/impl/T047SaveClaimServiceImpl.java`
- T014: `claim-ptp/.../t014/head/impl/T014SaveClaimServiceImpl.java` - 含 isTransMode 和银行现金流迁移
- 基类: `BaseSaveOrUpdateClaimService.java` (371行)

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
<!--
格式：
- [T{XXX}] {日期} {经验描述}
示例：
- [T014] 2025-12-20 isTransMode填充逻辑需要查TCoItemLevel2获取isCredit，放在fillValue中
- [T014] 2025-12-20 014302公司间业务硬编码flexOuCode='130017'，放在after中
-->
