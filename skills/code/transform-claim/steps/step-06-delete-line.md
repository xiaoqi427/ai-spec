# 步骤6：删除报账单行 (Delete Claim Line)

## 📋 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `DeleteT{XXX}ClaimLineService.java` |
| **新代码** | `T{XXX}DeleteClaimLineServiceImpl.java` |
| **继承基类** | `BaseDeleteClaimLineService` |
| **接口** | `IT{XXX}DeleteClaimLineService extends IBaseDeleteClaimLineService` |
| **核心方法** | `deleteClaimLine(TRmbsClaimLineDto claimLineDto)` |
| **可重写钩子** | `deleteClaimLine()` 整体重写 或 `after(claimLineDto)` |
| **模板文件** | `templates/line/interface-delete-template.java`, `templates/line/impl-delete-template.java` |

---

## 🔄 迁移策略

### 1. 定位老代码

- 路径: `DeleteT{XXX}ClaimLineService.java`
- 记录文件总行数

### 2. 分析老代码

老代码逻辑分类：

| 模块 | 功能 | 迁移方式 |
|------|------|----------|
| A-H | 查行、删附件、CVT、差额、税金、手机费、发票、行数据 | ✅ 基类已处理 |
| I | processAmount 金额重算 | ✅ 基类 after 已处理 |
| J | T{XXX}特有删除逻辑 | 🔧 需要迁移 |

### 3. 基类能力速查

`BaseDeleteClaimLineService` (228行):

```
deleteClaimLine(claimLineDto)  [@Transactional]
  ├── 查报账单 → 附件挂载模式处理
  ├── 删除附件、CVT、差额、税金、手机费、发票核销
  ├── 删除行本身
  └── after(claimLineDto)                        // ★ 默认调 processAmount
```

**基类已覆盖**（无需迁移）：
- 所有关联表清理、金额重算

### 4. 提取需迁移的逻辑

**大多数情况下无需迁移**，基类已包含所有通用逻辑。

### 5. 编写新代码

1. 基于模板创建接口和实现类
2. 通常只需继承，不需重写
3. 极少情况需要重写 after()

---

## ✅ 关键检查点

### 分析阶段
- [ ] 老代码已定位，记录行数
- [ ] 确认无特殊删除逻辑

### 编码阶段
- [ ] 接口和实现类已创建
- [ ] 类上有 `@Slf4j` 和 `@Service`
- [ ] 大多数情况下无需重写

### 验证阶段
- [ ] 无编译错误
- [ ] 删除功能正常

---

## ⚠️ 常见坑点

1. **重复实现金额重算** - after中的processAmount基类已调用
2. **空实现是正常的** - 大多数DeleteLineService都是空实现

---

## 📚 参考实现

- **T047**: `T047DeleteClaimLineServiceImpl.java` - 空实现
- **基类**: `BaseDeleteClaimLineService.java` (228行)

---

## 📝 经验记录区

> 每次迁移后补充实战经验

<!-- 格式: [T{XXX}] {日期} {经验描述} -->

1. **自定义金额重算**: 某些 T{XXX} 的 processAmount 逻辑不同（如T047需要额外的 preProcess/afterProcess）
2. **额外的关联数据清理**: 基类未覆盖的 T{XXX} 特有关联表
3. **状态回写**: 删除行后需要更新其他表的状态

### 第五步：选择重写策略

**方案A**: 只重写 `after()` → 适用于只需自定义金额重算的场景
```java
@Override
protected void after(TRmbsClaimLineDto claimLineDto) {
    // 自定义金额重算逻辑
    this.processAmount(claimLineDto, preProcess, afterProcess);
}
```

**方案B**: 完全重写 `deleteClaimLine()` → 适用于需要在删除流程中插入额外逻辑的场景（不推荐，除非必要）

## 检查清单

### 分析阶段
- [ ] 找到老代码文件
- [ ] 逐行分析 execute() 方法
- [ ] 对照 BaseDeleteClaimLineService (228行)
- [ ] 标记基类已覆盖的关联表删除
- [ ] 标记 T{XXX} 特有的额外清理逻辑
- [ ] 确认 processAmount 是否需要自定义

### 编码阶段
- [ ] 创建接口 `IT{XXX}DeleteClaimLineService extends IBaseDeleteClaimLineService`
- [ ] 创建实现类 `T{XXX}DeleteClaimLineServiceImpl extends BaseDeleteClaimLineService`
- [ ] 类上添加 `@Slf4j` 和 `@Service`
- [ ] 如需自定义金额：重写 `after(TRmbsClaimLineDto claimLineDto)`
- [ ] 注释标注原代码行数

### 验证阶段
- [ ] 无编译错误
- [ ] 基类已覆盖的关联表删除没有重复
- [ ] processAmount 金额重算逻辑正确
- [ ] import语句完整

## 常见坑点

1. **@Transactional 已在基类**: 基类的 `deleteClaimLine` 方法带有 `@Transactional(rollbackFor = Exception.class)`，子类不需要重复加
2. **after 默认行为**: 基类 after 默认调 `processAmount(claimLineDto, null, null)`，如果需要自定义 preProcess/afterProcess 就重写 after
3. **T047 参考**: T047 重写了 after，添加了自定义的 preProcess 和 afterProcess 来处理金额重算
4. **不要重复删除关联**: 基类已删除 CVT记录、差额记录、税金行、手机费额度、发票核销关联，不要在子类中重复

## 参考实现

- T047: `T047DeleteClaimLineServiceImpl.java` - 重写 after 自定义金额重算
- 基类: `BaseDeleteClaimLineService.java` (228行)

## 经验记录区
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
> 此区域用于记录实际迁移过程中发现的经验和教训。

<!--
格式：
- [T{XXX}] {日期} {经验描述}
-->
