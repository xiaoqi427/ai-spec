# 新代码结构参考文档

> 来源: `fssc-claim-service/`
> 框架: Spring Boot 3 + Java 21 + MyBatis Plus + MapStruct + Lombok

---

## 1. 新代码模块结构

```
fssc-claim-service/
├── claim-base/                    # 基础服务（公共头）
├── claim-common/                  # 公共模块（基类、通用 DTO、通用 Mapper）
│   ├── claim-common-do/           # 数据实体层（DO）
│   ├── claim-common-api-param/    # DTO + Converter（MapStruct）
│   ├── claim-common-api/          # Feign API 接口
│   └── claim-common-service/      # 业务逻辑层（基类 Service / Facade / Mapper）
├── claim-ptp/                     # PTP 模块（包含 T010、T012 等）
├── claim-eer/                     # EER 模块
├── claim-otc/                     # OTC 模块
├── claim-tr/                      # TR 模块
├── claim-fa/                      # FA 模块
└── claim-rtr/                     # RTR 模块
```

---

## 2. 单模块包结构

```
claim-{module}-service/
└── src/main/java/com/yili/claim/{module}/
    └── claim/
        └── t{xxx}/
            ├── head/                    # 报账单头相关
            │   ├── IT{XXX}NewClaimService.java
            │   ├── IT{XXX}SaveClaimService.java
            │   ├── IT{XXX}DeleteClaimService.java
            │   ├── IT{XXX}LoadClaimService.java
            │   └── impl/
            │       ├── T{XXX}NewClaimServiceImpl.java
            │       ├── T{XXX}SaveClaimServiceImpl.java
            │       ├── T{XXX}DeleteClaimServiceImpl.java
            │       └── T{XXX}LoadClaimServiceImpl.java
            ├── line/                    # 报账单行相关
            │   ├── IT{XXX}NewClaimLineService.java
            │   ├── IT{XXX}SaveClaimLineService.java
            │   ├── IT{XXX}UpdateClaimLineService.java
            │   ├── IT{XXX}DeleteClaimLineService.java
            │   ├── T{XXX}LoadClaimLineService.java
            │   └── impl/
            │       ├── T{XXX}NewClaimLineServiceImpl.java
            │       ├── T{XXX}SaveClaimLineServiceImpl.java
            │       ├── T{XXX}UpdateClaimLineServiceImpl.java
            │       └── T{XXX}DeleteClaimLineServiceImpl.java
            └── bpm/                     # BPM 流程相关
                ├── IT{XXX}CallBackClaimService.java
                ├── IT{XXX}SubmitClaimService.java
                └── impl/
                    ├── T{XXX}CallBackClaimServiceImpl.java
                    └── T{XXX}SubmitClaimServiceImpl.java
```

---

## 3. 新代码基类继承体系

### 3.1 报账单头基类（位于 claim-common-service）

| 基类 | 包路径 | 关键方法 | 对应老代码 |
|------|--------|---------|----------|
| `BaseNewClaimService` | `claim.common.service.claim.service.impl` | `newClaim(itemId, user)` / `preExecute(claim, user)` | `NewClaimService` |
| `BaseSaveOrUpdateClaimService` | `claim.common.service.claim.service.impl` | `save(full, user)` / `validation(...)` / `updateClaimLineFromClaim(...)` | `InsertClaimService` + `UpdateClaimService` |
| `BaseSaveClaimService` | `claim.common.service.claim.service.impl` | 继承自 `BaseSaveOrUpdateClaimService` | `InsertClaimService` |
| `BaseDeleteClaimService` | `claim.common.service.claim.service.impl` | `delete(claimId, user)` | `DeleteClaimService` |
| `BaseLoadClaimService` | `claim.common.service.claim.service.impl` | `load(claimId, user)` | `LoadAllT{XXX}Service` + View 系列 |
| `BaseSubmitClaimService` | `claim.common.service.claim.service.impl` | `submit(params)` / `validate(full, params)` / `preResult(full)` | `SubmitClaimService` |
| `BaseCallBackClaimService` | `claim.common.service.claim.service.impl` | `executeEnd(full, user)` / `preExecute(full, user)` | `ICallBackService` |

### 3.2 报账单行基类

| 基类 | 关键方法 | 对应老代码 |
|------|---------|----------|
| `BaseNewClaimLineService` | `newLine(itemId, claimId, user)` | `NewClaimLineService` |
| `BaseSaveClaimLineService` | `save(...)` | `InsertClaimLineService` |
| `BaseUpdateClaimLineService` | `update(...)` | `UpdateClaimLineService` |
| `BaseDeleteClaimLineService` | `delete(...)` | `DeleteClaimLineService` |
| `BaseLoadClaimLineService` | `loadLines(...)` | `ListAllT{XXX}ClaimLinesService` |

---

## 4. 新代码核心数据结构

### 4.1 DO 实体（claim-common-do）
```
com.yili.claim.common.entity/
├── claim/
│   ├── TRmbsClaimDo         # 报账单主表 DO
│   └── TRmbsClaimLineDo     # 报账单行 DO
├── TRmbsClaimTicketLineDo   # 票据行 DO
└── ...
```

### 4.2 DTO（claim-common-api-param）
```
com.yili.claim.common.api.param/
└── claim/dto/
    ├── TRmbsClaimBaseDto        # 报账单基础 DTO（对外 API 使用）
    └── TRmbsClaimLineBaseDto    # 报账单行基础 DTO
```

### 4.3 Service 内部 DTO（claim-common-service）
```
com.yili.claim.common.service.claim.dto/
├── TRmbsClaimPageDto            # 报账单页面 DTO（New/Load 返回）
├── TRmbsClaimPageFullDto        # 完整报账单 DTO（Submit/Save 入参）
└── TRmbsClaimLineDto            # 报账单行页面 DTO
```

### 4.4 用户信息
```java
// 新框架通过 UserObjectFullDto 传递用户信息
UserObjectFullDto user = UserThreadLocal.get();
user.getCurCompId()    // 当前公司 ID
user.getCurCostCenterId()  // 成本中心 ID
user.getUsernum()      // 用户工号
user.getOrgId()        // 组织 ID
user.getCurrency()     // 货币
```

---

## 5. 新代码关键注解与约定

### 5.1 类注解
```java
@Slf4j                           // 日志（必须）
@Service                         // Spring Bean（必须）
public class T010SaveClaimServiceImpl 
    extends BaseSaveOrUpdateClaimService 
    implements IT010SaveClaimService {
```

### 5.2 依赖注入
```java
@Resource
private ISomeDoService someDoService;  // 使用 @Resource，不用 @Autowired
```

### 5.3 行号注释规范
```java
/**
 * 方法说明
 *
 * 原代码: OldServiceName.java 第XX-XX行
 */
@Override
protected void someMethod(...) {
    // 原代码: OldServiceName.java 第XX-XX行
    // 业务逻辑
}
```

---

## 6. 新框架 BaseSubmitClaimService 关键 Override 方法

```java
// 提交前加载数据（对应老代码 preExecute 非校验逻辑）
@Override
protected void preResult(TRmbsClaimPageFullDto full) {
    // 加载报账单完整数据
}

// 子类扩展校验（对应老代码 validate 方法）
@Override
public <P extends TRmbsClaimPageDto> ChainValidator validate(
        TRmbsClaimPageFullDto full, P params) {
    ChainValidator validator = super.validate(full, params);
    // 添加 T0XX 特有校验
    validator.add("xxx", () -> validateSomething(full));
    return validator;
}
```

---

## 7. 新框架 BaseCallBackClaimService 关键 Override 方法

```java
// 审批通过后回调（对应老代码 executeEnd）
@Override
protected void executeEnd(TRmbsClaimPageFullDto full, UserObjectFullDto user) {
    super.executeEnd(full, user);
    // T0XX 特有回调逻辑
}

// 回调前置处理（对应老代码 preExecute）
@Override
protected void preExecute(TRmbsClaimPageFullDto full, UserObjectFullDto user) {
    // T0XX 回调前处理
}
```

---

## 8. 新代码 ClaimTemplateEnum（必须使用）

```java
// 位于 com.yili.common.constant.claim.ClaimTemplateEnum
ClaimTemplateEnum.T010.getCode()   // "T010"
ClaimTemplateEnum.T047.getCode()   // "T047"
// ...用于 itemId 判断，禁止使用硬编码字符串
```

---

## 9. 新代码 ChainValidator 校验链模式

```java
// Submit 校验链模式
ChainValidator validator = ChainValidator.of().severity(ValidationSeverity.PASS);
validator.add("校验名称", () -> {
    // 返回 ChainValidator 或 void
    // 抛出异常 = 校验失败
    if (condition) {
        throw new I18nException("错误信息");
    }
});
return validator;
```

---

## 10. 新代码层间调用约定

```
Controller → Business（Service层）
  └─ Business → DoService（Facade层）
       └─ DoService → Mapper
            └─ Mapper → Database (DO)
```

**关键约定**:
- `Business（Service）`可调用其他 `Business（Service）`（平层调用）
- `DoService（Facade）`只能调用 `Mapper`，绝对不允许写 if/SQL/业务逻辑
- `BaseXxxClaimService` 系列属于 Business 层
