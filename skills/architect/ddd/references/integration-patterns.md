# 集成模式与防腐层

## 1. 概述

当限界上下文需要交互时，选择合适的集成模式至关重要。错误的集成会导致模型污染、耦合加剧。

---

## 2. 集成模式详解

### 2.1 防腐层（Anti-Corruption Layer, ACL）

**场景**: 保护自身领域模型不被外部系统的模型污染。

**结构**:
```
自身上下文                    防腐层                     外部系统
┌──────────┐         ┌─────────────────┐         ┌──────────┐
│ 领域模型  │ ──────▶ │  Translator     │ ──────▶ │ 外部API  │
│          │         │  (翻译器)        │         │          │
│ 内部术语  │ ◀────── │  Adapter        │ ◀────── │ 外部模型  │
│          │         │  (适配器)        │         │          │
│ 干净、纯粹 │         │  Facade         │         │ 复杂、异构 │
└──────────┘         │  (外观)         │         └──────────┘
                     └─────────────────┘
```

**组成部分**:
- **Facade（外观）**: 简化外部系统的接口，提供统一入口
- **Adapter（适配器）**: 适配外部协议（REST/SOAP/MQ）
- **Translator（翻译器）**: 外部模型 ↔ 内部模型的转换

**示例: 银行网关防腐层**

```java
/**
 * 银行网关防腐层 - Facade
 * 统一多家银行的接口差异
 */
public interface BankGateway {
    PaymentResult executePayment(PaymentRequest request);
    PaymentStatus queryStatus(String transactionId);
}

/**
 * 工商银行适配器
 */
@Component
public class IcbcBankAdapter implements BankGateway {

    private final IcbcApiClient icbcClient;
    private final IcbcTranslator translator;

    @Override
    public PaymentResult executePayment(PaymentRequest request) {
        // 1. 内部模型 → 外部模型（翻译）
        IcbcPayReq icbcReq = translator.toIcbcRequest(request);
        // 2. 调用外部系统（适配）
        IcbcPayResp icbcResp = icbcClient.pay(icbcReq);
        // 3. 外部模型 → 内部模型（翻译）
        return translator.toPaymentResult(icbcResp);
    }
}

/**
 * 工商银行翻译器
 */
@Component
public class IcbcTranslator {

    public IcbcPayReq toIcbcRequest(PaymentRequest request) {
        IcbcPayReq req = new IcbcPayReq();
        req.setTranAmt(request.getAmount().getAmount().toString());
        req.setCurType(mapCurrency(request.getAmount().getCurrency()));
        req.setPayAccNo(request.getPayerAccount().getAccountNo());
        req.setRcvAccNo(request.getPayeeAccount().getAccountNo());
        req.setRcvAccNam(request.getPayeeAccount().getAccountName());
        return req;
    }

    public PaymentResult toPaymentResult(IcbcPayResp resp) {
        return PaymentResult.builder()
            .transactionId(resp.getTranSerialNo())
            .status(mapStatus(resp.getRetCode()))
            .message(resp.getRetMsg())
            .completedAt(parseDateTime(resp.getTranDate(), resp.getTranTime()))
            .build();
    }

    private PaymentStatus mapStatus(String retCode) {
        return switch (retCode) {
            case "0000" -> PaymentStatus.SUCCESS;
            case "0001" -> PaymentStatus.PENDING;
            default -> PaymentStatus.FAILED;
        };
    }
}
```

### 2.2 开放主机服务（Open Host Service, OHS）

**场景**: 提供标准化的服务接口供多个消费者使用。

**结构**:
```
消费者A ──┐
          │     ┌────────────────────┐
消费者B ──┼───▶ │  Open Host Service  │ ──▶ 内部领域模型
          │     │  (标准化API)         │
消费者C ──┘     └────────────────────┘
```

**示例: 配置服务开放接口**

```java
/**
 * 配置服务 - 开放主机服务
 * 提供标准化API供多个上下文消费
 */
@RestController
@RequestMapping("/api/v1/config")
public class ConfigOpenHostController {

    @Resource
    private ConfigQueryService configQueryService;

    /**
     * 标准化接口：查询费用类型
     * 消费者：报账上下文、凭证上下文、预算上下文
     */
    @GetMapping("/expense-types/{code}")
    public Result<ExpenseTypeDto> getExpenseType(@PathVariable String code) {
        return Result.success(configQueryService.getExpenseType(code));
    }

    /**
     * 标准化接口：查询组织架构
     */
    @GetMapping("/departments/{deptId}")
    public Result<DepartmentDto> getDepartment(@PathVariable Long deptId) {
        return Result.success(configQueryService.getDepartment(deptId));
    }
}

/**
 * Feign Client - 消费者使用
 */
@FeignClient(name = "fssc-config-service")
public interface ConfigApi {
    @GetMapping("/api/v1/config/expense-types/{code}")
    Result<ExpenseTypeDto> getExpenseType(@PathVariable String code);
}
```

### 2.3 发布语言（Published Language, PL）

**场景**: 跨上下文使用标准化数据格式交换信息。

```java
/**
 * 发布语言 - 标准化事件格式
 * 所有上下文都理解的通用消息格式
 */
public class IntegrationEvent {
    private String eventId;
    private String eventType;
    private String sourceContext;
    private LocalDateTime timestamp;
    private String payload; // JSON格式的事件数据
    private Map<String, String> metadata;
}

/**
 * 发布语言 - 标准化的报账单摘要
 * 用于跨上下文传递报账单基本信息
 */
public record ClaimSummary(
    String claimId,
    String claimNo,
    String claimType,
    BigDecimal totalAmount,
    String currency,
    String applicantId,
    String status
) {}
```

### 2.4 客户-供应商（Customer-Supplier）

**场景**: 上下游明确的服务关系，下游的需求影响上游的API设计。

```
供应商（上游）                    客户（下游）
┌──────────────┐              ┌──────────────┐
│  配置服务      │   提供API    │  报账服务      │
│              │ ───────────▶ │              │
│  优先满足      │              │  提出需求      │
│  下游需求      │ ◀─────────── │              │
└──────────────┘   需求反馈    └──────────────┘
```

### 2.5 共享内核（Shared Kernel）

**场景**: 两个上下文共享一小部分核心模型，需紧密协调。

```java
// 共享内核模块（fssc-common-constant）
// 两个上下文共同依赖且共同维护

/** 共享的用户标识 */
public record UserId(Long value) {}

/** 共享的金额值对象 */
public record Money(BigDecimal amount, String currency) {}

/** 共享的审批状态枚举 */
public enum ApprovalStatus {
    PENDING, APPROVED, REJECTED;
}
```

**注意**: 共享内核应尽量小，变更需双方协商。

---

## 3. 模式选择指南

### 决策矩阵

| 场景 | 推荐模式 | 原因 |
|------|----------|------|
| 对接第三方系统（银行/税务） | ACL | 隔离外部复杂性 |
| 公共基础服务（配置/用户） | OHS + PL | 标准化，多消费者 |
| 团队间协作开发 | Customer-Supplier | 需求驱动API设计 |
| 核心共享概念（少量） | Shared Kernel | 保持一致，紧密协调 |
| 遗留系统集成 | ACL | 保护新模型不被污染 |
| 无直接关联 | Separate Ways | 避免不必要的耦合 |

### 集成反模式

```
❌ 共享数据库
  → 多个服务直接操作同一张表
  → 导致隐式耦合，无法独立部署

❌ 上游模型泄漏
  → 直接在业务代码中使用外部系统的DTO
  → 导致外部变更影响内部逻辑

❌ 同步调用链过长
  → A → B → C → D 同步调用
  → 延迟叠加，单点故障传播

❌ 无翻译直接透传
  → 外部数据不经转换直接传递给领域层
  → 领域模型被外部概念污染
```

---

## 4. 实践示例

### 示例1: 报账单提交 → 审批流程创建

```java
// ===== 报账上下文（供应商） =====
// 报账单提交后发布事件

@Service
public class ClaimApplicationService {
    @Transactional(rollbackFor = Exception.class)
    public void submit(ClaimId id) {
        Claim claim = repository.findById(id).orElseThrow();
        claim.submit();
        repository.save(claim);
        // 发布集成事件到MQ
        eventPublisher.publish(new ClaimSubmittedIntegrationEvent(
            claim.getId(), claim.getClaimNo(), claim.getTotalAmount()
        ));
    }
}

// ===== 审批上下文（客户） =====
// 消费事件，使用ACL翻译

@Component
public class ClaimApprovalEventConsumer {
    @Resource
    private ApprovalRequestFactory factory;
    @Resource
    private ApprovalApplicationService approvalService;

    @RabbitListener(queues = "approval.claim-submitted")
    public void onClaimSubmitted(ClaimSubmittedIntegrationEvent event) {
        // ACL翻译：将报账上下文的概念转为审批上下文的概念
        CreateApprovalCommand cmd = CreateApprovalCommand.builder()
            .sourceId(event.getClaimId())
            .sourceType("CLAIM")
            .requestAmount(event.getTotalAmount())
            .build();
        approvalService.createApproval(cmd);
    }
}
```

### 示例2: 遗留系统防腐层

```java
/**
 * 老报账系统防腐层
 * 隔离老系统的复杂数据结构
 */
@Component
public class LegacyClaimAntiCorruptionLayer {

    private final LegacyClaimDao legacyDao;

    /**
     * 从老系统查询报账单，翻译为新领域模型
     */
    public Optional<ClaimSnapshot> queryFromLegacy(String claimNo) {
        // 老系统返回Map结构
        Map<String, Object> legacyData = legacyDao.queryByClaimNo(claimNo);
        if (legacyData == null || legacyData.isEmpty()) {
            return Optional.empty();
        }

        // 翻译为新模型
        return Optional.of(ClaimSnapshot.builder()
            .claimNo(getString(legacyData, "BILL_NO"))
            .applicantName(getString(legacyData, "APPLY_USER_NAME"))
            .totalAmount(new Money(
                getBigDecimal(legacyData, "TOTAL_AMT"),
                getString(legacyData, "CURRENCY_CODE")))
            .status(mapLegacyStatus(getString(legacyData, "BILL_STATUS")))
            .build());
    }

    private ClaimStatus mapLegacyStatus(String legacyStatus) {
        return switch (legacyStatus) {
            case "10" -> ClaimStatus.DRAFT;
            case "20" -> ClaimStatus.SUBMITTED;
            case "30" -> ClaimStatus.APPROVED;
            case "40" -> ClaimStatus.PAID;
            case "99" -> ClaimStatus.CANCELLED;
            default -> throw new UnknownStatusException(
                "未知的老系统状态码: " + legacyStatus);
        };
    }
}
```

---

## 检查清单

- [ ] 每个外部系统集成都有明确的集成模式
- [ ] 外部系统的模型不直接出现在领域层
- [ ] 防腐层包含完整的翻译逻辑
- [ ] 开放主机服务有版本管理
- [ ] 共享内核尽量小，变更需协商
- [ ] 集成事件使用标准化格式
- [ ] 异步集成考虑了幂等性和重试
