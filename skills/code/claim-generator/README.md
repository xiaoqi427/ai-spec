# TR Claim Generator - 使用指南

## 快速开始

### 生成T014资产采购报账单（不含付款行）

运行以下命令即可生成完整的T014模块代码：

```bash
/skill tr-claim-generator T014 "资产采购报账单" "资金类报账" --author sevenxiao
```

生成后的文件结构：
```
claim-tr-web/
  └── controller/claim/
      └── T014ClaimController.java

claim-tr-service/
  └── claim/t014/
      ├── head/
      │   ├── IT014NewClaimService.java
      │   ├── IT014LoadClaimService.java
      │   ├── IT014SaveClaimService.java
      │   ├── IT014DeleteClaimService.java
      │   └── impl/
      │       ├── T014NewClaimServiceImpl.java
      │       ├── T014LoadClaimServiceImpl.java
      │       ├── T014SaveClaimServiceImpl.java
      │       └── T014DeleteClaimServiceImpl.java
      └── line/
          ├── IT014NewClaimLineService.java
          ├── IT014SaveClaimLineService.java
          ├── IT014UpdateClaimLineService.java
          ├── IT014DeleteClaimLineService.java
          └── impl/
              ├── T014NewClaimLineServiceImpl.java
              ├── T014SaveClaimLineServiceImpl.java
              ├── T014UpdateClaimLineServiceImpl.java
              └── T014DeleteClaimLineServiceImpl.java
```

### 生成T065收入成本报账单（含付款行）

```bash
/skill tr-claim-generator T065 "收入成本报账单" "订单到收款总账记账业务" --with-pay --author sevenxiao
```

额外生成的pay目录：
```
claim-tr-service/
  └── claim/t065/
      └── pay/
          ├── IT065NewClaimPayLineService.java
          ├── IT065SaveClaimPayLineService.java
          ├── IT065DeleteClaimPayLineService.java
          └── impl/
              ├── T065NewClaimPayLineServiceImpl.java
              ├── T065SaveClaimPayLineServiceImpl.java
              └── T065DeleteClaimPayLineServiceImpl.java
```

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 模板编号 | ✅ | T+3位数字 | T014, T065, T099 |
| 业务描述 | ✅ | 报账单业务说明 | "资产采购报账单" |
| 业务分类 | ✅ | 所属业务大类 | "资金类报账" |
| --with-pay | ❌ | 是否包含付款行 | 不传则不包含 |
| --author | ❌ | 作者名称 | sevenxiao |

## 生成后的操作清单

### 1. 更新ClaimTemplateEnum

在 `com.yili.common.constant.claim.ClaimTemplateEnum` 中添加：

```java
T014("014", "资产采购报账单"),
```

### 2. 配置菜单权限

在系统菜单配置中添加T014的菜单项和权限配置

### 3. 自定义业务逻辑

根据具体业务需求，在Service实现类中添加特定逻辑：

#### NewClaimServiceImpl
```java
@Override
protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
    log.debug("T014NewClaimServiceImpl.preExecute开始");
    
    // 设置T014特有的字段
    claim.setCustomField1("value1");
    claim.setCustomField2("value2");
    
    log.debug("T014NewClaimServiceImpl.preExecute完成");
    return claim;
}
```

#### SaveClaimServiceImpl
```java
@Override
protected void preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
    log.debug("T014SaveClaimServiceImpl.preExecute开始");
    
    // 保存前的业务校验
    validateBusinessRules(claim);
    
    log.debug("T014SaveClaimServiceImpl.preExecute完成");
}

@Override
protected void postExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
    log.debug("T014SaveClaimServiceImpl.postExecute开始");
    
    // 保存后的关联操作
    processRelatedData(claim);
    
    log.debug("T014SaveClaimServiceImpl.postExecute完成");
}
```

### 4. 添加单元测试

为每个Service创建对应的测试类：

```java
@SpringBootTest
class T014NewClaimServiceImplTest {
    
    @Resource
    private IT014NewClaimService service;
    
    @Test
    void should_create_new_claim_successfully() {
        // given
        UserObjectFullDto user = createTestUser();
        
        // when
        TRmbsClaimPageDto result = service.newClaim("T014", user);
        
        // then
        assertNotNull(result);
        assertEquals(user.getUserid(), result.getExpenseIssuerId());
    }
}
```

## 常见问题

### Q1: 生成的代码编译报错？
A: 确保已经引入所有必需的依赖，特别是claim-common模块

### Q2: 如何修改业务描述？
A: 在Controller的@Tag注解中修改description参数

### Q3: 如何添加自定义接口？
A: 在Controller中添加新的@PostMapping方法，并创建对应的Service

### Q4: 是否可以修改标准接口？
A: 可以，但建议尽量保持一致性，方便维护

## 最佳实践

1. **遵循命名规范**：所有T{XXX}保持大小写一致
2. **完善注释**：在关键方法添加详细的业务说明
3. **异常处理**：使用BusinessException进行业务异常抛出
4. **日志记录**：关键步骤记录debug级别日志
5. **单元测试**：核心业务逻辑必须有测试覆盖

## 文件对照表

### Head Services

| 服务名称 | 接口 | 实现 | 说明 |
|---------|------|------|------|
| New | IT{XXX}NewClaimService | T{XXX}NewClaimServiceImpl | 新建报账单 |
| Load | IT{XXX}LoadClaimService | T{XXX}LoadClaimServiceImpl | 加载报账单 |
| Save | IT{XXX}SaveClaimService | T{XXX}SaveClaimServiceImpl | 保存报账单 |
| Delete | IT{XXX}DeleteClaimService | T{XXX}DeleteClaimServiceImpl | 删除报账单 |

### Line Services

| 服务名称 | 接口 | 实现 | 说明 |
|---------|------|------|------|
| New | IT{XXX}NewClaimLineService | T{XXX}NewClaimLineServiceImpl | 新建明细行 |
| Save | IT{XXX}SaveClaimLineService | T{XXX}SaveClaimLineServiceImpl | 保存明细行 |
| Update | IT{XXX}UpdateClaimLineService | T{XXX}UpdateClaimLineServiceImpl | 更新明细行 |
| Delete | IT{XXX}DeleteClaimLineService | T{XXX}DeleteClaimLineServiceImpl | 删除明细行 |

### Pay Services (可选)

| 服务名称 | 接口 | 实现 | 说明 |
|---------|------|------|------|
| New | IT{XXX}NewClaimPayLineService | T{XXX}NewClaimPayLineServiceImpl | 新建付款行 |
| Save | IT{XXX}SaveClaimPayLineService | T{XXX}SaveClaimPayLineServiceImpl | 保存付款行 |
| Delete | IT{XXX}DeleteClaimPayLineService | T{XXX}DeleteClaimPayLineServiceImpl | 删除付款行 |

### BPM Services (总是生成)

| 服务名称 | 接口 | 实现 | 说明 |
|---------|------|------|------|
| CallBack | IT{XXX}CallBackClaimService | T{XXX}CallBackClaimServiceImpl | BPM流程回调 |
| Submit | IT{XXX}SubmitClaimService | T{XXX}SubmitClaimServiceImpl | 报账单提交校验 |
