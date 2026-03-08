# 领域事件（Domain Events）

## 1. 核心概念

领域事件表示领域中发生的有意义的业务事实。事件是过去式，描述已经发生的事情，不可变且不可撤销。

### 特征

| 特征 | 说明 |
|------|------|
| **过去式命名** | `ClaimSubmitted`（已提交），不是 `SubmitClaim` |
| **不可变** | 事件一旦发布，不能修改 |
| **包含上下文** | 携带足够信息让消费者无需回查 |
| **因果关系** | 一个事件可以触发后续的命令或事件 |

---

## 2. 事件设计

### 2.1 事件结构

```java
/**
 * 领域事件基类
 */
public abstract class DomainEvent {
    /** 事件ID */
    private final String eventId;
    /** 发生时间 */
    private final LocalDateTime occurredAt;
    /** 聚合ID */
    private final String aggregateId;
    /** 聚合类型 */
    private final String aggregateType;
    /** 事件版本 */
    private final int version;

    protected DomainEvent(String aggregateId, String aggregateType) {
        this.eventId = UUID.randomUUID().toString();
        this.occurredAt = LocalDateTime.now();
        this.aggregateId = aggregateId;
        this.aggregateType = aggregateType;
        this.version = 1;
    }
}
```

### 2.2 事件命名规范

```
格式: {聚合名}{动作过去分词}Event

示例:
  ClaimSubmittedEvent      报账单已提交
  ClaimApprovedEvent       报账单已审批通过
  ClaimRejectedEvent       报账单已驳回
  PaymentExecutedEvent     付款已执行
  InvoiceVerifiedEvent     发票已验真
```

### 2.3 具体事件示例

```java
/**
 * 报账单已提交事件
 */
public class ClaimSubmittedEvent extends DomainEvent {
    /** 报账单号 */
    private final String claimNo;
    /** 申请人ID */
    private final Long applicantId;
    /** 报账金额 */
    private final BigDecimal totalAmount;
    /** 报账类型 */
    private final String claimType;

    public ClaimSubmittedEvent(ClaimId claimId, ClaimNo claimNo,
                               UserId applicantId, Money totalAmount,
                               String claimType) {
        super(claimId.toString(), "Claim");
        this.claimNo = claimNo.getValue();
        this.applicantId = applicantId.getValue();
        this.totalAmount = totalAmount.getAmount();
        this.claimType = claimType;
    }
}
```

---

## 3. 事件风暴（Event Storming）

### 3.1 概述

事件风暴是一种协作式建模方法，通过识别领域事件来发现业务流程和领域模型。

### 3.2 工作坊流程

```
阶段1: 事件收集（30分钟）
  → 参与者在便利贴上写下领域事件（橙色）
  → 按时间线排列
  → 不讨论，只收集

阶段2: 时间线梳理（20分钟）
  → 排列事件的先后顺序
  → 识别并行和分支流程
  → 标记关键里程碑

阶段3: 补充元素（30分钟）
  → 命令（蓝色）：触发事件的动作
  → 参与者/角色（黄色）：执行命令的人
  → 策略（紫色）：自动化规则
  → 外部系统（粉色）：外部依赖
  → 读模型（绿色）：做决策需要的信息

阶段4: 聚合识别（20分钟）
  → 围绕命令和事件识别聚合
  → 确定聚合边界

阶段5: 限界上下文划分（20分钟）
  → 将相关聚合归入上下文
  → 识别上下文间关系
```

### 3.3 便利贴颜色规范

| 颜色 | 元素 | 示例 |
|------|------|------|
| 🟧 橙色 | 领域事件 | 报账单已提交 |
| 🟦 蓝色 | 命令 | 提交报账单 |
| 🟨 黄色 | 参与者/角色 | 报账人、审批人 |
| 🟪 紫色 | 策略/规则 | 金额>5000需高级审批 |
| 🟩 绿色 | 读模型 | 报账单详情视图 |
| 🩷 粉色 | 外部系统 | 银行网关、税务系统 |
| 🟥 红色 | 痛点/问题 | 审批超时无通知 |

### 3.4 事件风暴示例：报账单流程

```
时间线 →

[报账人]        [报账人]       [系统策略]      [审批人]        [系统策略]
   │               │              │              │              │
   ▼               ▼              ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ 创建     │  │ 提交     │  │ 路由     │  │ 审批     │  │ 触发     │
│ 报账单   │  │ 报账单   │  │ 审批流程  │  │ 通过     │  │ 付款     │
│ (命令)   │  │ (命令)   │  │ (策略)   │  │ (命令)   │  │ (策略)   │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     ▼             ▼             ▼             ▼             ▼
╔═════════╗  ╔══════════╗  ╔══════════╗  ╔══════════╗  ╔══════════╗
║ 报账单  ║  ║ 报账单   ║  ║ 审批流程  ║  ║ 报账单   ║  ║ 付款单   ║
║ 已创建  ║  ║ 已提交   ║  ║ 已创建   ║  ║ 已通过   ║  ║ 已创建   ║
║ (事件)  ║  ║ (事件)   ║  ║ (事件)   ║  ║ (事件)   ║  ║ (事件)   ║
╚═════════╝  ╚══════════╝  ╚══════════╝  ╚══════════╝  ╚══════════╝
```

---

## 4. 事件溯源（Event Sourcing）

### 4.1 概念

事件溯源不存储实体的当前状态，而是存储所有发生过的事件。通过重放事件来恢复实体状态。

### 4.2 适用场景

| 适用 | 不适用 |
|------|--------|
| 需要完整审计轨迹 | 简单 CRUD |
| 需要回溯历史状态 | 数据量极大且不需回溯 |
| 复杂业务流程 | 团队对事件溯源不熟悉 |
| 需要对账和核查 | 实时性要求极高 |

### 4.3 实现骨架

```java
/**
 * 事件溯源聚合根
 */
public abstract class EventSourcedAggregate {
    private final List<DomainEvent> uncommittedEvents = new ArrayList<>();
    private int version = 0;

    /** 从事件历史中恢复状态 */
    public void rehydrate(List<DomainEvent> history) {
        for (DomainEvent event : history) {
            apply(event, false);
        }
    }

    /** 应用新事件 */
    protected void applyNewEvent(DomainEvent event) {
        apply(event, true);
    }

    private void apply(DomainEvent event, boolean isNew) {
        // 调用子类的事件处理方法
        handle(event);
        this.version++;
        if (isNew) {
            this.uncommittedEvents.add(event);
        }
    }

    /** 子类实现：根据事件类型更新状态 */
    protected abstract void handle(DomainEvent event);
}

/**
 * 报账单 - 事件溯源实现
 */
public class Claim extends EventSourcedAggregate {

    private ClaimId id;
    private ClaimStatus status;
    private Money totalAmount;

    /** 提交：产生事件而非直接修改状态 */
    public void submit() {
        if (this.status != ClaimStatus.DRAFT) {
            throw new DomainException("只有草稿状态可提交");
        }
        applyNewEvent(new ClaimSubmittedEvent(this.id));
    }

    @Override
    protected void handle(DomainEvent event) {
        switch (event) {
            case ClaimCreatedEvent e -> {
                this.id = e.getClaimId();
                this.status = ClaimStatus.DRAFT;
            }
            case ClaimSubmittedEvent e -> {
                this.status = ClaimStatus.SUBMITTED;
            }
            case ClaimApprovedEvent e -> {
                this.status = ClaimStatus.APPROVED;
            }
            default -> { /* 未知事件忽略 */ }
        }
    }
}
```

---

## 5. 事件发布与订阅

### 5.1 进程内事件

```java
// 使用 Spring ApplicationEvent
@Service
public class ClaimApplicationService {

    @Resource
    private ApplicationEventPublisher publisher;

    @Transactional(rollbackFor = Exception.class)
    public void submitClaim(ClaimId id) {
        Claim claim = repository.findById(id).orElseThrow();
        claim.submit();
        repository.save(claim);
        // 发布事件
        claim.getDomainEvents().forEach(publisher::publishEvent);
        claim.clearEvents();
    }
}

// 事件监听
@Component
@Slf4j
public class ClaimEventHandler {

    @EventListener
    public void onClaimSubmitted(ClaimSubmittedEvent event) {
        log.info("报账单已提交: {}", event.getClaimNo());
        // 触发审批流程创建
    }
}
```

### 5.2 跨进程事件（消息队列）

```java
// 发布到 MQ
@Component
public class DomainEventPublisher {

    @Resource
    private RabbitTemplate rabbitTemplate;

    public void publish(DomainEvent event) {
        String routingKey = event.getClass().getSimpleName();
        rabbitTemplate.convertAndSend("domain.events", routingKey, event);
    }
}

// 消费 MQ 事件
@Component
@Slf4j
public class PaymentEventConsumer {

    @RabbitListener(queues = "claim.approved")
    public void onClaimApproved(ClaimApprovedEvent event) {
        log.info("收到审批通过事件，创建付款单: claimId={}", event.getAggregateId());
        // 创建付款单
    }
}
```

---

## 6. 事件建模模式

### 6.1 事件-命令-事件链

```
事件A → 策略/监听器 → 命令B → 事件B → 策略/监听器 → 命令C → 事件C

示例：
ClaimSubmittedEvent
    → 创建审批流程（命令）
        → ApprovalCreatedEvent
            → 通知审批人（命令）
                → NotificationSentEvent
```

### 6.2 Saga 模式（长事务）

```
当业务流程跨多个聚合/服务时，使用 Saga 协调：

报账单提交 Saga:
1. 提交报账单     → ClaimSubmittedEvent
2. 冻结预算       → BudgetFrozenEvent
3. 创建审批流程    → ApprovalCreatedEvent
   ├── 审批通过   → 执行支付
   └── 审批驳回   → 释放预算（补偿操作）
```

---

## 检查清单

- [ ] 事件使用过去式命名
- [ ] 事件是不可变的
- [ ] 事件包含足够上下文信息
- [ ] 事件在聚合内注册，在应用层发布
- [ ] 事件监听器不修改发起方的聚合
- [ ] 跨上下文事件使用消息队列
- [ ] 补偿逻辑已考虑（Saga 模式）
