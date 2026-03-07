# 老代码结构参考文档

> 来源: `yldc-caiwugongxiangpingtai-fsscYR-master/`
> 框架: Spring MVC + Hibernate/JDBC (非 Spring Boot)

---

## 1. 老代码根路径

```
yldc-caiwugongxiangpingtai-fsscYR-master/
└── src/
    └── com/ibm/gbs/efinance/business/
        ├── ylService/claim/                # 各报账单T模块的业务服务（重点）
        │   ├── T001/
        │   ├── T002/
        │   ├── ...
        │   └── T0XX/
        │       ├── NewT{XXX}ClaimService.java
        │       ├── InsertT{XXX}ClaimService.java
        │       ├── UpdateT{XXX}ClaimService.java
        │       ├── DeleteT{XXX}ClaimService.java
        │       ├── DeleteT{XXX}ClaimLinesService.java
        │       ├── LoadAllT{XXX}Service.java
        │       ├── CallBackT{XXX}Service.java
        │       ├── SubmitT{XXX}Service.java
        │       ├── ListAllT{XXX}ClaimLinesService.java
        │       └── ViewT{XXX}ClaimService.java / ViewT{XXX}ClaimLineService.java
        └── service/
            ├── TBaseService/               # 通用基类 Service（底层实现）
            │   ├── NewClaimService.java
            │   ├── InsertClaimService.java
            │   ├── UpdateClaimService.java
            │   ├── DeleteClaimService.java
            │   ├── DeleteClaimLineService.java
            │   ├── ViewClaimService.java
            │   ├── ListAllClaimLinesService.java
            │   └── SubmitClaimService.java  （14545行，核心基类）
            └── ClaimServiceBase.java        （13468行，全局基类）
```

---

## 2. 老代码 Service 命名规律

| 功能 | 老代码类名模式 | 核心方法 |
|------|--------------|---------|
| 新建报账单头 | `NewT{XXX}ClaimService` | `execute(MessageObject mo)` |
| 新建报账单行 | `NewT{XXX}ClaimLineService` | `execute(MessageObject mo)` |
| 新增保存头 | `InsertT{XXX}ClaimService` | `preExecute()` / `insertClaimLineFromClaim()` / `execute()` |
| 更新保存头 | `UpdateT{XXX}ClaimService` | `updateClaimLineFromClaim()` / `execute()` |
| 新增保存行 | `InsertT{XXX}ClaimLineService` | `execute()` |
| 更新保存行 | `UpdateT{XXX}ClaimLineService` | `execute()` |
| 删除报账单头 | `DeleteT{XXX}ClaimService` | `execute()` |
| 删除报账单行 | `DeleteT{XXX}ClaimLinesService` | `execute()` |
| 加载查看头+行 | `LoadAllT{XXX}Service` | `execute()` |
| 查看报账单头 | `ViewT{XXX}ClaimService` | `execute()` |
| 查看报账单行 | `ViewT{XXX}ClaimLineService` | `execute()` |
| 审批回调 | `CallBackT{XXX}Service` | `executeEnd()` / `preExecute()` |
| 提交审批 | `SubmitT{XXX}Service` | `execute()` / `validate()` |
| 列表查询行 | `ListAllT{XXX}ClaimLinesService` | `execute()` |

---

## 3. 老代码核心数据结构

### 3.1 核心实体类（Pojo）
```
com.ibm.gbs.efinance.business.pojo/
├── TRmbsClaim             # 报账单主表
├── TRmbsClaimLine         # 报账单行表
├── TRmbsClaimTicketLine   # 票据行
├── TRmbsClaimTravelLine   # 差旅行
├── TRmbsClaiminvoice      # 发票关联
├── TRmbsClaimrel          # 关联关系
├── TRmbsAsset             # 资产信息
└── TRmbsTemplate          # 模板配置
```

### 3.2 核心入参对象
```java
// 老代码统一使用 MessageObject 传递参数
MessageObject mo = ...; 

// 从 mo 中获取参数（字符串 key/value 模式）
String claimId = mo.get("claimId");         // 报账单ID
String itemId  = mo.get("itemId");          // 模板ID
String data    = mo.get("data");            // JSON数据
String piid    = mo.get("piid");            // 流程实例ID
```

### 3.3 核心常量（ClaimServiceBase）
```java
public static final String REQ_ITEM_ID      = "itemId";
public static final String REQ_CLAIM_ID     = "claimId";
public static final String REQ_DATA         = "data";
public static final String REQ_CLAIM_NO     = "claimNo";
public static final String REQ_DELETE_IDS   = "deleteIds";
public static final String REQ_CLAIMLINE_ID = "claimLineId";
public static final String REQ_PIID         = "piid";
public static final String EMPLOYEE_VENDOR  = "EMP";
public static final String COMPANY_VENDOR   = "COMP";
```

---

## 4. 老代码典型结构示例

### 4.1 NewT{XXX}ClaimService（新建头）典型结构
```java
public class NewT010ClaimService extends NewClaimService {
    @Override
    protected void preExecute(MessageObject mo) throws Exception {
        super.preExecute(mo);
        // T0XX 特有初始化逻辑
        // 设置 itemId、默认字段等
    }
}
```

### 4.2 InsertT{XXX}ClaimService（新增保存头）典型结构
```java
public class InsertT010ClaimService extends InsertClaimService {
    @Override
    protected void preExecute(MessageObject mo) throws Exception {
        super.preExecute(mo);
        // 初始化特有字段
    }
    
    @Override
    protected void validate(MessageObject mo) throws Exception {
        super.validate(mo);
        // T0XX 业务校验
    }
    
    @Override
    protected void insertClaimLineFromClaim(MessageObject mo) throws Exception {
        // 新建默认明细行（部分模块有此逻辑）
    }
}
```

### 4.3 CallBackT{XXX}Service（回调）典型结构
```java
public class CallBackT010Service extends ICallBackService {
    @Override
    public void executeEnd(MessageObject mo) throws Exception {
        // 审批通过后的回调逻辑
    }
    
    @Override
    public void preExecute(MessageObject mo) throws Exception {
        // 回调前置处理
    }
}
```

### 4.4 SubmitT{XXX}Service（提交）典型结构
```java
public class SubmitT010Service extends SubmitClaimService {
    @Override
    protected void validate(MessageObject mo) throws Exception {
        super.validate(mo);
        // T0XX 提交前校验
    }
    
    @Override
    protected void preExecute(MessageObject mo) throws Exception {
        super.preExecute(mo);
        // 提交前处理
    }
}
```

---

## 5. 老代码 DAO 模式

```java
// 老代码使用 Spring 注入 DAO
@Autowired
private IRmbsClaimDAO claimDao;

@Autowired
private IRmbsClaimLineDAO claimLineDao;

// DAO 方法
claimDao.save(claim);
claimDao.update(claim);
claimDao.delete(claimId);
claimDao.getById(claimId);
```

---

## 6. 老代码 SystemConstants 常量

所在包: `com.ibm.gbs.efinance.business.eip.SystemConstants`

常用常量:
```java
SystemConstants.CLAIM_STATUS_DRAFT      // 草稿
SystemConstants.CLAIM_STATUS_SUBMITTED  // 已提交
SystemConstants.CLAIM_STATUS_APPROVED   // 已审批
SystemConstants.CLAIM_STATUS_REJECTED   // 已拒绝
SystemConstants.CLAIM_STATUS_PAID       // 已支付
```

---

## 7. 老代码特殊模式

### 7.1 Insert + Update 合并为 Save（新框架重要变化）
- 老代码: `InsertT{XXX}ClaimService` 和 `UpdateT{XXX}ClaimService` 是两个独立类
- 新框架: 合并为 `T{XXX}SaveClaimServiceImpl`，通过 `claimId == null` 判断新增还是更新

### 7.2 Load 合并（新框架重要变化）
- 老代码: `LoadAllT{XXX}Service` + `ViewT{XXX}ClaimService` + `ViewT{XXX}ClaimLineService` 是多个类
- 新框架: 合并为 `T{XXX}LoadClaimServiceImpl`

### 7.3 ListAllClaimLines 独立（新框架独立保留）
- 老代码: `ListAllT{XXX}ClaimLinesService`（通常只有几行，继承基类）
- 新框架: `T{XXX}LoadClaimLineService`（独立保留）

### 7.4 gd 前缀子类
- 老代码中存在 `gd/` 目录，如 `GdViewT001ClaimService`，是 GD 公司定制的子类
- 迁移时忽略 gd 前缀类，只迁移主逻辑

---

## 8. 老代码与新框架步骤对应关系

| 步骤 | 老代码类 | 新代码类 |
|------|---------|---------|
| 1. New头 | `NewT{XXX}ClaimService` | `T{XXX}NewClaimServiceImpl` |
| 2. New行 | `NewT{XXX}ClaimLineService` | `T{XXX}NewClaimLineServiceImpl` |
| 3. Save头 | `InsertT{XXX}ClaimService` + `UpdateT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` |
| 4. Save行 | `InsertT{XXX}ClaimLineService` + `UpdateT{XXX}ClaimLineService` | `T{XXX}SaveClaimLineServiceImpl` + `T{XXX}UpdateClaimLineServiceImpl` |
| 5. Delete头 | `DeleteT{XXX}ClaimService` | `T{XXX}DeleteClaimServiceImpl` |
| 6. Delete行 | `DeleteT{XXX}ClaimLinesService` | `T{XXX}DeleteClaimLineServiceImpl` |
| 7. Load | `LoadAllT{XXX}Service` + `ViewT{XXX}ClaimService` + `ViewT{XXX}ClaimLineService` | `T{XXX}LoadClaimServiceImpl` |
| 8. Callback | `CallBackT{XXX}Service` | `T{XXX}CallBackClaimServiceImpl` |
| 9. Submit | `SubmitT{XXX}Service` | `T{XXX}SubmitClaimServiceImpl` |
| 10. Load行 | `ListAllT{XXX}ClaimLinesService` | `T{XXX}LoadClaimLineService` |
