# 步骤1：新建报账单头 (New Claim Head)

## 📋 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `NewT{XXX}ClaimService.java` |
| **新代码** | `T{XXX}NewClaimServiceImpl.java` |
| **继承基类** | `BaseNewClaimService` |
| **接口** | `IT{XXX}NewClaimService extends IBaseNewClaimService` |
| **核心方法** | `newClaim(String itemId, UserObjectFullDto user)` |
| **可重写钩子** | `preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user)` |
| **模板文件** | `templates/head/interface-new-template.java`, `templates/head/impl-new-template.java` |

---

## 🔄 迁移策略（5步）

### 1. 定位老代码

- 路径: `yldc-.../claim/T{XXX}/NewT{XXX}ClaimService.java`
- 记录文件总行数

### 2. 分析老代码 execute() 方法

老代码的逻辑模块分类：

| 模块 | 功能 | 迁移方式 |
|------|------|----------|
| A | 创建Claim对象、设置模板 | ✅ 基类已处理，跳过 |
| B | 设置用户信息 | ✅ 基类已处理，跳过 |
| C | 设置默认值 | ✅ 基类已处理，跳过 |
| D | 员工供应商信息 | ✅ 基类已处理，跳过 |
| E | T{XXX}特有逻辑 | 🔧 迁移到 preExecute() |

### 3. 基类能力速查

`BaseNewClaimService.newClaim()` 流程：

```
newClaim(itemId, user)
  ├── setUserInformation(claim, user)    // 用户信息
  ├── preResult(claim, user)             // 模板+默认值+事业部
  ├── preExecute(claim, user)            // ★ 子类重写点
  └── return claim
```

**基类已覆盖**（无需迁移）：
- 创建对象、用户信息、模板信息
- 默认值（版本号、紧急程度、金额等）
- 默认事业部、员工供应商

### 4. 提取需迁移的逻辑

**常见需迁移逻辑**：
- 报销人信息（基类的用户信息不够时）
- 退款标识（isRefund）
- 单位全称和税号（ouTax）
- 特殊默认值
- 特定业务字段

### 5. 编写新代码

1. 基于模板创建接口和实现类
2. 在 `preExecute()` 填入迁移逻辑
3. 标注原代码行数

---

## ✅ 关键检查点

### 分析阶段
- [ ] 老代码文件已定位，记录行数
- [ ] 逻辑已分类（基类已有 vs 需迁移）

### 编码阶段
- [ ] 接口和实现类已创建
- [ ] 类上有 `@Slf4j` 和 `@Service`
- [ ] 迁移逻辑标注了原代码行数
- [ ] 依赖用 `@Resource` 注入

### 验证阶段
- [ ] 无编译错误
- [ ] 老代码100%覆盖（迁移或标记为基类已有）
- [ ] 无重复实现基类逻辑

---

## ⚠️ 常见坑点

1. **重复实现基类逻辑** - 用户信息、默认值基类已全部实现
2. **遗漏特有逻辑** - 老代码末尾的特殊赋值容易被忽略
3. **方法签名不匹配** - `preExecute` 参数是 `(TRmbsClaimPageDto, UserObjectFullDto)`
4. **忘记返回claim** - `preExecute` 必须返回 `claim` 对象

---

## 📚 参考实现

- **T047**: `claim-otc/.../t047/head/impl/T047NewClaimServiceImpl.java` (45行)
  - preExecute设置报销人信息+退款标识+ouTax
- **T010**: `claim-eer/.../t010/head/impl/T010NewClaimServiceImpl.java`
  - 空实现（基类已满足）

---

## 📝 经验记录区

> 每次迁移后补充实战经验

- TODO需要检查是否有API可调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑

<!-- 格式: [T{XXX}] {日期} {经验描述} -->
