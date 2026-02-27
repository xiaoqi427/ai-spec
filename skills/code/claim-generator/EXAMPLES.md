# TR Claim Generator - 完整使用示例

本文档提供完整的TR报账单模块生成示例，帮助快速上手使用。

---

## 📋 目录

1. [快速开始](#快速开始)
2. [完整示例：生成T014](#完整示例生成t014)
3. [完整示例：生成T065](#完整示例生成t065)
4. [生成文件详解](#生成文件详解)
5. [后续配置步骤](#后续配置步骤)
6. [常见问题解答](#常见问题解答)

---

## 🚀 快速开始

### 前提条件

确保您已了解：
- TR报账单的业务背景
- 需要生成的报账单编号（如T014、T065等）
- 是否需要付款行功能

### 基本调用格式

```bash
# 不含付款行
/skill tr-claim-generator <模板编号> "<业务描述>" "<业务分类>"

# 含付款行
/skill tr-claim-generator <模板编号> "<业务描述>" "<业务分类>" --with-pay
```

---

## 📦 完整示例：生成T014

### 步骤1：调用Skill

```bash
/skill tr-claim-generator T014 "资产采购报账单" "资金类报账"
```

### 步骤2：AI自动生成以下文件

#### Controller层（1个文件）

**文件路径**: `claim-tr-web/src/main/java/com/yili/claim/tr/web/controller/claim/T014ClaimController.java`

```java
package com.yili.claim.tr.web.controller.claim;

import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageFullDto;
import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
import com.yili.claim.tr.claim.t014.head.IT014DeleteClaimService;
import com.yili.claim.tr.claim.t014.head.IT014LoadClaimService;
import com.yili.claim.tr.claim.t014.head.IT014NewClaimService;
import com.yili.claim.tr.claim.t014.head.IT014SaveClaimService;
// ... 更多导入

@Slf4j
@RestController
@RequestMapping("T014")
@Tag(name = "(TR)资金类报账/资产采购报账单(T014)", description = "资产采购报账单")
public class T014ClaimController {
    
    private final String itemId = ClaimTemplateEnum.T014.name();
    
    @Resource
    private IT014NewClaimService newClaimService;
    
    // ... 更多服务注入
    
    @Operation(summary = "新增-页面初始化", description = "新增-页面初始化")
    @PostMapping(value = "new")
    public TRmbsClaimPageDto newClaim(@Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        return newClaimService.newClaim(itemId, user);
    }
    
    // ... 更多接口方法
}
```

#### Head层接口（4个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/IT014NewClaimService.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/IT014LoadClaimService.java`
3. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/IT014SaveClaimService.java`
4. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/IT014DeleteClaimService.java`

#### Head层实现（4个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/impl/T014NewClaimServiceImpl.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/impl/T014LoadClaimServiceImpl.java`
3. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/impl/T014SaveClaimServiceImpl.java`
4. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/head/impl/T014DeleteClaimServiceImpl.java`

#### Line层接口（4个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/IT014NewClaimLineService.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/IT014SaveClaimLineService.java`
3. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/IT014UpdateClaimLineService.java`
4. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/IT014DeleteClaimLineService.java`

#### Line层实现（4个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/impl/T014NewClaimLineServiceImpl.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/impl/T014SaveClaimLineServiceImpl.java`
3. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/impl/T014UpdateClaimLineServiceImpl.java`
4. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/line/impl/T014DeleteClaimLineServiceImpl.java`

#### BPM层接口（2个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/bpm/IT014CallBackClaimService.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/bpm/IT014SubmitClaimService.java`

#### BPM层实现（2个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/bpm/impl/T014CallBackClaimServiceImpl.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/bpm/impl/T014SubmitClaimServiceImpl.java`

**总计**: 21个文件

### 步骤3：手动配置

#### 3.1 更新ClaimTemplateEnum

在 `com.yili.common.constant.claim.ClaimTemplateEnum` 中添加：

```java
T014("014", "资产采购报账单"),
```

#### 3.2 配置系统菜单

在系统管理后台添加T014的菜单配置和权限。

#### 3.3 自定义业务逻辑（可选）

在生成的Service实现类中添加特定的业务逻辑：

**示例：T014NewClaimServiceImpl**
```java
@Override
protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
    log.debug("T014NewClaimServiceImpl.preExecute开始");
    
    // 设置报销人信息
    claim.setExpenseIssuerId(user.getUserid());
    claim.setExpenseIssuerName(user.getFullname());
    claim.setExpenseIssuerDeptId(user.getCurGroupId());
    
    // TODO: 添加T014特定的业务逻辑
    // 例如：设置资产采购相关的默认值
    claim.setAssetType("FIXED_ASSET");
    claim.setDepreciationMethod("STRAIGHT_LINE");
    
    log.debug("T014NewClaimServiceImpl.preExecute完成");
    return claim;
}
```

---

## 📦 完整示例：生成T065（含付款行）

### 步骤1：调用Skill

```bash
/skill tr-claim-generator T065 "收入成本报账单" "订单到收款总账记账业务" --with-pay
```

### 步骤2：AI自动生成文件

除了T014的17个文件外，还会额外生成：

#### Pay层接口（3个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/pay/IT065NewClaimPayLineService.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/pay/IT065SaveClaimPayLineService.java`
3. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/pay/IT065DeleteClaimPayLineService.java`

#### Pay层实现（3个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/pay/impl/T065NewClaimPayLineServiceImpl.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/pay/impl/T065SaveClaimPayLineServiceImpl.java`
3. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/pay/impl/T065DeleteClaimPayLineServiceImpl.java`

#### BPM层接口（2个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/bpm/IT065CallBackClaimService.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/bpm/IT065SubmitClaimService.java`

#### BPM层实现（2个文件）

1. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/bpm/impl/T065CallBackClaimServiceImpl.java`
2. `claim-tr-service/src/main/java/com/yili/claim/tr/claim/t065/bpm/impl/T065SubmitClaimServiceImpl.java`

**总计**: 27个文件（17 + 6 + 4）

### 步骤3：手动配置

同T014的配置步骤，但需要额外注意：

- 确保`ITRmbsPaylistInitService`服务可用
- 配置付款相关的权限和菜单

---

## 📄 生成文件详解

### 目录结构

```
fssc-claim-service/
├── claim-tr-web/
│   └── src/main/java/com/yili/claim/tr/web/controller/claim/
│       └── T{XXX}ClaimController.java
│
└── claim-tr-service/
    └── src/main/java/com/yili/claim/tr/claim/t{xxx}/
        ├── head/
        │   ├── IT{XXX}NewClaimService.java
        │   ├── IT{XXX}LoadClaimService.java
        │   ├── IT{XXX}SaveClaimService.java
        │   ├── IT{XXX}DeleteClaimService.java
        │   └── impl/
        │       ├── T{XXX}NewClaimServiceImpl.java
        │       ├── T{XXX}LoadClaimServiceImpl.java
        │       ├── T{XXX}SaveClaimServiceImpl.java
        │       └── T{XXX}DeleteClaimServiceImpl.java
        ├── line/
        │   ├── IT{XXX}NewClaimLineService.java
        │   ├── IT{XXX}SaveClaimLineService.java
        │   ├── IT{XXX}UpdateClaimLineService.java
        │   ├── IT{XXX}DeleteClaimLineService.java
        │   └── impl/
        │       ├── T{XXX}NewClaimLineServiceImpl.java
        │       ├── T{XXX}SaveClaimLineServiceImpl.java
        │       ├── T{XXX}UpdateClaimLineServiceImpl.java
        │       └── T{XXX}DeleteClaimLineServiceImpl.java
        └── pay/  (可选)
            ├── IT{XXX}NewClaimPayLineService.java
            ├── IT{XXX}SaveClaimPayLineService.java
            ├── IT{XXX}DeleteClaimPayLineService.java
            └── impl/
                ├── T{XXX}NewClaimPayLineServiceImpl.java
                ├── T{XXX}SaveClaimPayLineServiceImpl.java
                └── T{XXX}DeleteClaimPayLineServiceImpl.java
```

### 接口说明

#### Head接口

| 接口路径 | HTTP方法 | 说明 | 请求参数 | 返回类型 |
|---------|---------|------|---------|---------|
| /T{XXX}/new | POST | 新增-页面初始化 | UserObjectFullDto | TRmbsClaimPageDto |
| /T{XXX}/load | POST | 报账单加载 | TRmbsClaimPageDto | TRmbsClaimPageFullDto |
| /T{XXX}/save | POST | 报账单保存 | TRmbsClaimPageDto | TRmbsClaimPageDto |
| /T{XXX}/delete | POST | 报账单删除 | TRmbsClaimPageDto | void |

#### Line接口

| 接口路径 | HTTP方法 | 说明 | 请求参数 | 返回类型 |
|---------|---------|------|---------|---------|
| /T{XXX}/newClaimLine | POST | 明细行初始化 | Long claimId | TRmbsClaimLineDto |
| /T{XXX}/saveClaimLine | POST | 明细行新增 | TRmbsClaimLineDto | TRmbsClaimLineDto |
| /T{XXX}/updateClaimLine | POST | 明细行修改 | TRmbsClaimLineDto | TRmbsClaimLineDto |
| /T{XXX}/deleteClaimLine | POST | 明细行删除 | TRmbsClaimLineDto | void |

#### Pay接口（可选）

| 接口路径 | HTTP方法 | 说明 | 请求参数 | 返回类型 |
|---------|---------|------|---------|---------|
| /T{XXX}/initPaylist | POST | 计划付款初始化 | ClaimPayListReqParams | TRmbsPaylistDo |
| /T{XXX}/newClaimPayLine | POST | 发票核销初始化 | ClaimClaimPayLineReqDto | List<TRmbsPaylistDto> |
| /T{XXX}/saveClaimPayLine | POST | 发票核销保存 | ClaimClaimPayLineReqDto | void |
| /T{XXX}/deleteClaimPayLine | POST | 发票核销删除 | ClaimClaimPayLineReqDto | void |

---

## ⚙️ 后续配置步骤

### 1. 编译验证

```bash
cd fssc-claim-service/claim-tr
mvn clean compile
```

### 2. 运行单元测试

```bash
mvn test
```

### 3. 启动应用

```bash
mvn spring-boot:run
```

### 4. 接口测试

使用Swagger或Postman测试生成的接口：

**访问Swagger UI**:
```
http://localhost:8080/swagger-ui.html
```

**找到T014相关接口**:
- 搜索 "T014"
- 测试 `/T014/new` 接口

---

## ❓ 常见问题解答

### Q1: 生成的代码无法编译？

**A**: 检查以下几点：
1. 确保`claim-common`模块已正确引入
2. 检查Base服务类是否存在（`BaseNewClaimService`等）
3. 运行`mvn clean install`重新构建

### Q2: Controller注入Service失败？

**A**: 确保：
1. Service实现类有`@Service`注解
2. 包扫描路径包含生成的Service
3. 使用`@Resource`而非`@Autowired`

### Q3: 如何修改业务描述？

**A**: 修改Controller的`@Tag`注解：
```java
@Tag(name = "(TR)新分类/新描述(T014)", description = "新描述")
```

### Q4: 如何添加自定义字段？

**A**: 在对应的Service实现类的`preExecute`或`postExecute`方法中添加：
```java
@Override
protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
    claim.setCustomField("customValue");
    return claim;
}
```

### Q5: 如何添加自定义验证？

**A**: 在Save或Update的`preExecute`方法中添加：
```java
@Override
protected void preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
    if (claim.getAmount() == null || claim.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
        throw new BusinessException("金额必须大于0");
    }
}
```

### Q6: 付款行功能是否必须？

**A**: 不是必须的。只有涉及付款流程的报账单才需要使用`--with-pay`参数。

### Q7: 如何删除已生成的代码？

**A**: 直接删除对应的目录即可：
```bash
# 删除Controller
rm claim-tr-web/src/main/java/com/yili/claim/tr/web/controller/claim/T014ClaimController.java

# 删除Service
rm -rf claim-tr-service/src/main/java/com/yili/claim/tr/claim/t014/
```

---

## 📝 总结

使用TR Claim Generator，您可以在几秒钟内生成完整的TR报账单模块代码，包括：

✅ 完整的Controller层（17-23个文件）  
✅ 标准的Service接口和实现  
✅ 符合项目规范的分层架构  
✅ 完整的Javadoc注释  
✅ 可扩展的业务逻辑钩子  

这大大提升了开发效率，减少了重复性工作，让您可以专注于业务逻辑的实现。
