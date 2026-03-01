# 步骤1：新建报账单头 (New Claim Head)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `NewT{XXX}ClaimService.java` |
| **新代码** | `T{XXX}NewClaimServiceImpl.java` |
| **继承基类** | `BaseNewClaimService` |
| **接口** | `IT{XXX}NewClaimService extends IBaseNewClaimService` |
| **核心方法** | `newClaim(String itemId, UserObjectFullDto user)` |
| **可重写钩子** | `preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user)` |
| **模板文件** | `templates/head/interface-new-template.java`, `templates/head/impl-new-template.java` |

## 迁移策略

### 第一步：定位老代码

1. 找到老代码文件：`yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{XXX}/NewT{XXX}ClaimService.java`
2. 记录文件总行数，用于后续注释标注

### 第二步：分析老代码 execute() 方法

老代码的 `execute()` 方法通常包含以下逻辑模块（需逐一识别）：

```
execute() {
    // 模块A: 创建Claim对象、设置模板信息 → 基类已处理
    // 模块B: 设置用户信息(userId, fullName, deptId等) → 基类已处理
    // 模块C: 设置默认值(版本号、紧急程度、金额初始化等) → 基类已处理
    // 模块D: 设置员工供应商信息 → 基类已处理
    // 模块E: T{XXX}特有的初始化逻辑 → 需要迁移到 preExecute()
}
```

### 第三步：对照基类已实现能力

`BaseNewClaimService.newClaim()` 已实现的完整流程：

```
newClaim(itemId, user)
  ├── setUserInformation(claim, user)    // 设置用户信息
  ├── preResult(claim, user)             // 内部调用:
  │   ├── template(claim, user)          //   模板信息加载
  │   ├── setDefaultValues(claim, user)  //   默认值（版本号、紧急程度、金额等）
  │   └── setDefaultBu(claim, user)      //   默认事业部
  ├── preExecute(claim, user)            // ★ 空钩子 → 子类重写点
  └── return claim
```

**基类已覆盖的逻辑（不需要迁移）**：
- 创建报账单对象
- 设置用户信息（userId、fullName、deptId、username）
- 加载模板信息
- 设置默认值（版本号=1、紧急程度=ordinary、金额=0等）
- 设置默认事业部
- 员工供应商赋值（setVendorInfo / setVendorInfoOfEMployeeVendor）

### 第四步：提取需迁移的逻辑

将老代码中**不属于基类已实现**的逻辑，全部迁移到 `preExecute()` 中。

常见需要迁移的逻辑：
- 报销人信息（如果基类的用户信息不够用）
- 退款标识（isRefund）
- 单位全称和税号（ouTax）
- 特殊的默认值设置
- 特定业务字段初始化

### 第五步：编写新代码

1. 创建接口文件（基于 `interface-new-template.java`）
2. 创建实现文件（基于 `impl-new-template.java`）
3. 在 `preExecute()` 中填入迁移逻辑
4. 每段逻辑标注原代码行数

## 检查清单

### 分析阶段
- [ ] 找到老代码文件并记录总行数
- [ ] 逐行阅读老代码 `execute()` 方法
- [ ] 标记哪些逻辑基类已实现（无需迁移）
- [ ] 标记哪些逻辑需要迁移到 `preExecute()`
- [ ] 确认是否有调用其他Service的逻辑

### 编码阶段
- [ ] 创建接口 `IT{XXX}NewClaimService extends IBaseNewClaimService`
- [ ] 创建实现类 `T{XXX}NewClaimServiceImpl extends BaseNewClaimService`
- [ ] 类上添加 `@Slf4j` 和 `@Service` 注解
- [ ] 重写 `preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user)` 方法
- [ ] 迁移的每段逻辑都标注了原代码行数注释
- [ ] 需要注入的Service都用 `@Resource` 声明
- [ ] 不存在的字段创建在DTO中而非DO中

### 验证阶段
- [ ] 无编译错误
- [ ] 老代码每一行都有对应处理（迁移或标注为基类已实现）
- [ ] 没有重复基类已实现的逻辑
- [ ] import语句完整（不写在代码里面）
- [ ] 没有对传入变量重新赋值（对象set可以）

## 常见坑点

1. **重复实现基类逻辑**：最常见错误。老代码中设置用户信息、默认值的代码，基类已全部实现，不需要再写
2. **遗漏特有逻辑**：有些老代码在 `execute()` 末尾有特殊赋值，容易被忽略
3. **preExecute 返回值**：必须返回 `claim` 对象
4. **方法签名不匹配**：注意 `preExecute` 参数是 `(TRmbsClaimPageDto, UserObjectFullDto)`，不是老代码的 `(Map, UserObject)`

## 参考实现

- T047: `claim-otc/.../t047/head/impl/T047NewClaimServiceImpl.java` (45行) - preExecute设置报销人信息+退款标识+ouTax
- T010: `claim-eer/.../t010/head/impl/T010NewClaimServiceImpl.java` - 空实现（基类已满足）

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训，请在每次迁移后补充。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
<!--
格式：
- [T{XXX}] {日期} {经验描述}
示例：
- [T044] 2025-12-24 老代码中ouTax方法需要单独抽出，因为多个步骤都用到
-->
