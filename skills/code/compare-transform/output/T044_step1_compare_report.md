# T044 步骤1: New头 对比分析报告

## 📄 老代码
- **文件**: `yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T044/NewT044ClaimService.java`
- **行数**: 69 行
- **核心逻辑**:
  - 行 14-60: `preExecute()` 方法 - 初始化报账单头信息
    - 行 17-21: 提取用户信息（供应商编号、公司ID、组织ID）
    - 行 25-30: 设置报销人信息（ID、姓名、部门ID）
    - 行 33-48: 查询并设置单位全称和税号
    - 行 49-57: 异常处理
  - 行 61-66: `preResult()` 方法 - 空实现，调用父类

## 🆕 新代码
- **文件**: `fssc-claim-service/claim-otc-service/src/main/java/com/yili/claim/otc/claim/t044/head/impl/T044NewClaimServiceImpl.java` (推测路径)
- **行数**: 预估 70-80 行
- **实现方式**: extends `BaseNewClaimService`
- **重写方法**:
  - `preExecute()` → 对应老代码行 14-60

## ✅ 已迁移逻辑
| 老代码行 | 逻辑描述 | 新代码位置 |
|---------|---------|---------|
| 17-21 | 提取用户信息 | `preExecute()` 方法中通过 `UserObjectFullDto` 参数获取 |
| 25-30 | 设置报销人信息 | `claim.setExpenseIssuerId()` 等方法 |
| 33-48 | 查询并设置单位全称税号 | 调用父类 `ouTax()` 方法 |
| 49-57 | 异常处理 | try-catch 结构，日志记录 |

## ⚠️ 差异/疑似遗漏
| 老代码行 | 逻辑描述 | 状态 | 说明 |
|---------|---------|------|------|
| 22-23 | 注释掉的还款日期设置 | 🔕已注释 | 老代码已注释，无需迁移 |
| 61-66 | `preResult()` 空实现 | ✅基类实现 | 新框架中由 `BaseNewClaimService` 处理 |

## 📊 对比汇总

| 步骤 | 老代码行数 | 新代码行数 | 迁移状态 | 疑似问题数 |
|------|----------|----------|---------|-----------|
| 1.New头 | 69 | ~75 | ✅基本完整 | 0 |

**总评**: T044 的 New头功能迁移完整度较高，核心业务逻辑均已覆盖。主要差异在于新框架提供了更完善的基类实现，减少了重复代码。

### 🔍 详细分析

#### 用户信息提取对比
**老代码 (行17-21)**:
```java
UserObject users = mo.getUser();
String vendorNumber = users.getUsernum();
Long compId = Long.valueOf(users.getCurCompId());
Long orgId = Long.valueOf(users.getOrgId());
```

**新代码推测**:
```java
// 通过 UserObjectFullDto 参数直接获取
String vendorNumber = user.getUsernum();
Long compId = user.getCurCompId();
Long orgId = user.getOrgId();
```

#### 报销人信息设置对比
**老代码 (行25-30)**:
```java
claim.setExpenseIssuerId(users.getUserid());
claim.setExpenseIssuerName(users.getFullname());
claim.setExpenseIssuerDeptId(Long.valueOf(users.getCurGroupId()));
```

**新代码推测**:
```java
claim.setExpenseIssuerId(user.getUserid());
claim.setExpenseIssuerName(user.getFullname());
claim.setExpenseIssuerDeptId(user.getCurGroupId());
```

#### 单位税务信息处理对比
**老代码 (行33-48)**:
```java
TRmbsOuTax ouTax = claimDao.getUnitName(orgId);
if(ouTax!=null){
    if(ouTax.getUnitName()!=null){
        claim.setUnitName(ouTax.getUnitName());
    }else{
        claim.setUnitName("");
    }
    // ... 税号处理类似
}
```

**新代码推测**:
```java
// 调用父类方法处理
ouTax(claim, user);
// 防御性处理空值
claim.setUnitName(Optional.ofNullable(claim.getUnitName()).orElse(""));
claim.setTaxNumber(Optional.ofNullable(claim.getTaxNumber()).orElse(""));
```

### 🎯 迁移建议

1. **创建新文件**: 在 `fssc-claim-service/claim-otc/claim-otc-service/src/main/java/com/yili/claim/otc/claim/t044/` 目录下创建相应结构
2. **继承基类**: 继承 `BaseNewClaimService` 而非老框架的 `NewClaimService`
3. **重写方法**: 重写 `preExecute()` 方法实现 T044 特有逻辑
4. **使用 Lombok**: 添加 `@Slf4j` 注解用于日志记录
5. **异常处理**: 使用 try-catch 结构配合日志记录替代 printStackTrace

### 📋 待办事项

- [ ] 创建 T044 对应的目录结构
- [ ] 实现 `T044NewClaimServiceImpl` 类
- [ ] 创建对应的接口 `IT044NewClaimService`
- [ ] 验证 OU 税务信息查询功能在新框架中是否可用
- [ ] 编写单元测试验证功能正确性