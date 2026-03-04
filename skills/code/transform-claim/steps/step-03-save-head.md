# 步骤3：保存报账单头 (Save/Update Claim Head)

## 📋 概述

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

---

## 🔄 迁移策略（5步）

### 关键变更：Insert + Update 合并为一个

**老框架**: 分离
- `InsertT{XXX}ClaimService` - 新增逻辑
- `UpdateT{XXX}ClaimService` - 更新逻辑

**新框架**: 统一处理
```
save(params, user)
  ├── claimId != null → update(params, user)    // 更新流程
  └── claimId == null → super.save(params, user) // 新增流程
```

### 1. 定位老代码

- `InsertT{XXX}ClaimService.java` (新增逻辑)
- `UpdateT{XXX}ClaimService.java` (更新逻辑)
- 分别记录行数

### 2. 分析老代码逻辑模块

**老代码逻辑分类**:

| 模块 | Insert逻辑 | Update逻辑 | 迁移方式 |
|------|-----------|-----------|----------|
| A | 基础数据设置 | 查旧数据、版本校验 | ✅ 基类已处理 |
| B | 模板信息校验 | 流程状态校验 | ✅ 基类已处理 |
| C | 版本号设置 | 核减金额变化检测 | ✅ 基类已处理 |
| D | 流程状态、单号 | 不核销说明 | ✅ 基类已处理 |
| E | 付款计划级联 | 进项税转出信息 | ✅ 基类已处理 |
| F | T{XXX}特有逻辑 | T{XXX}特有逻辑 | 🔧 迁移到钩子方法 |

### 3. 基类能力速查

`BaseSaveOrUpdateClaimService` 流程 (371行)：

```
save(params, user)
  ├── [Insert] super.save():
  │   ├── validation → before → preResult → fillValue/preExecute
  │   ├── claimDoService.save(claim)
  │   └── after → insertClaimLineFromClaim → 级联更新
  │
  └── [Update] update():
      ├── 查旧数据 → validation → before
      ├── claimDoService.save(claim)
      └── updateClaimLineFromClaim → after → processClaimAmount
```

**基类已覆盖**（无需迁移）：
- Insert/Update路由、基础校验、流程校验
- 核减金额检测、不核销说明、进项税转出
- 付款计划级联、单号生成、版本管理

### 4. 提取需迁移的逻辑

**常见需迁移逻辑**:
- `fillValue()`: T{XXX}特有字段赋值（Insert/Update通用）
- `preExecute()`: T{XXX}特有的前置处理
- `insertClaimLineFromClaim()`: Insert时插入特殊行
- `updateClaimLineFromClaim()`: Update时更新特殊行
- `processClaimAmount()`: T015专用金额处理

### 5. 编写新代码

1. 基于模板创建接口和实现类
2. 根据需要重写钩子方法
3. Insert和Update逻辑合并，通过参数区分

---

## ✅ 关键检查点

### 分析阶段
- [ ] Insert和Update老代码都已定位
- [ ] 逻辑已分类（基类已有 vs 需迁移）
- [ ] 明确哪些逻辑在Insert、哪些在Update、哪些共用

### 编码阶段
- [ ] 接口和实现类已创建
- [ ] 类上有 `@Slf4j` 和 `@Service`
- [ ] 钩子方法重写正确（fillValue/preExecute等）
- [ ] Insert和Update逻辑已合理合并

### 验证阶段
- [ ] 无编译错误
- [ ] Insert和Update场景都已覆盖
- [ ] 无重复实现基类逻辑

---

## ⚠️ 常见坑点

1. **遗漏Update逻辑** - 只看Insert代码，忘记分析Update
2. **重复校验** - 基类已有完整的模板、流程、版本校验
3. **钩子方法调用顺序** - fillValue在preExecute之前
4. **级联更新** - 付款计划级联基类已处理，不要重复

---

## 📚 参考实现

- **T047**: `T047SaveClaimServiceImpl.java` - 重写fillValue和preExecute
- **基类**: `BaseSaveOrUpdateClaimService.java` (371行) - 需仔细阅读

---

## 📝 经验记录区

> 每次迁移后补充实战经验

<!-- 格式: [T{XXX}] {日期} {经验描述} -->
