# 步骤2：新建报账单行 (New Claim Line)

## 📋 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `NewT{XXX}ClaimLineService.java` |
| **新代码** | `T{XXX}NewClaimLineServiceImpl.java` |
| **继承基类** | `BaseNewClaimLineService` |
| **接口** | `IT{XXX}NewClaimLineService extends IBaseNewClaimLineService` |
| **核心方法** | `newClaimLine(Long claimId)` |
| **可重写钩子** | `preExecute(TRmbsClaimLineDto claimLineDto, TRmbsClaimBaseDto claim)` |
| **模板文件** | `templates/line/interface-new-template.java`, `templates/line/impl-new-template.java` |

---

## 🔄 迁移策略（5步）

### 1. 定位老代码

- 路径: `NewT{XXX}ClaimLineService.java`
- 记录文件总行数

### 2. 分析老代码 execute() 方法

老代码的逻辑模块分类：

| 模块 | 功能 | 迁移方式 |
|------|------|----------|
| A | 查报账单信息 | ✅ 基类已处理，跳过 |
| B | 创建ClaimLine对象、设claimId | ✅ 基类已处理，跳过 |
| C | 设币种CNY、汇率1 | ✅ 基类已处理，跳过 |
| D | 设公司ID | ✅ 基类已处理，跳过 |
| E | T{XXX}特有字段初始化 | 🔧 迁移到 preExecute() |
| F-J | 费用部门、BU段、部门属性等 | ✅ 基类已处理，跳过 |

### 3. 基类能力速查

`BaseNewClaimLineService.newClaimLine()` 流程：

```
newClaimLine(claimId)
  ├── 查报账单信息
  ├── 创建 TRmbsClaimLineDto
  ├── 设 claimId, currency, exchangeRate, compId
  ├── preExecute(claimLineDto, claim)     // ★ 子类重写点
  ├── 设费用部门、BU段、部门属性、项目段等
  ├── 设默认值、申请日期、发票类型等
  └── return claimLineDto
```

**基类已覆盖**（无需迁移）：
- 查报账单、创建对象、基础字段
- 费用部门（根据sysGroup+item2Id判断，分支极其复杂）
- BU段、部门属性、项目段、申请日期等

### 4. 提取需迁移的逻辑

**常见需迁移逻辑**：
- T{XXX}特有字段初始化
- 特殊默认值覆盖
- 从其他Service查询并赋值

**重要**: 很多单据类型的 NewClaimLine 完全被基类覆盖，实现类可为空。

### 5. 编写新代码

1. 基于模板创建接口和实现类
2. 如有特有逻辑，在 `preExecute()` 中实现
3. 如无特有逻辑，实现类保持空

---

## ✅ 关键检查点

### 分析阶段
- [ ] 老代码文件已定位，记录行数
- [ ] 逻辑已分类（基类已有 vs 需迁移）
- [ ] 确认preExecute调用时机（在费用部门等之前）

### 编码阶段
- [ ] 接口和实现类已创建
- [ ] 类上有 `@Slf4j` 和 `@Service`
- [ ] preExecute 返回 `claimLineDto`

### 验证阶段
- [ ] 无编译错误
- [ ] 无重复实现基类的itemId判断逻辑

---

## ⚠️ 常见坑点

1. **大量重复** - 基类已包含非常多itemId的特殊处理
2. **preExecute时机** - 在费用部门、BU段、部门属性**之前**调用
3. **空实现是正确的** - 老代码逻辑全被基类覆盖时（参考T047）
4. **参数类型** - claim参数类型是 `TRmbsClaimBaseDto`

---

## 📚 参考实现

- **T047**: `T047NewClaimLineServiceImpl.java` (18行) - 空实现，基类已满足
- **基类**: `BaseNewClaimLineService.java` (183行) - 需仔细阅读

---

## 📝 经验记录区

> 每次迁移后补充实战经验

- TODO需要检查是否有API可调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑

<!-- 格式: [T{XXX}] {日期} {经验描述} -->
