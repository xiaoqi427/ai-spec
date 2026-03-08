# 领域模型规范

## 1. 实体（Entity）

### 定义
具有唯一标识的领域对象，其标识在整个生命周期内保持不变。实体的核心在于**连续性和标识**，而非属性。

### 识别标准

| 判断条件 | 是实体 | 不是实体 |
|----------|--------|----------|
| 需要跟踪其生命周期变化 | ✅ | |
| 需要区分两个属性相同的对象 | ✅ | |
| 拥有唯一业务标识 | ✅ | |
| 仅由属性值定义，无需区分身份 | | ✅ |

### 设计原则

1. **标识策略**：优先使用业务标识（如订单号），其次使用技术标识（如UUID/自增ID）
2. **行为丰富**：实体应包含与自身状态相关的业务行为，避免贫血模型
3. **关联精简**：仅保留业务上必要的关联关系，优先使用ID引用而非对象引用
4. **保护不变量**：通过构造函数和方法保护实体的业务规则

### 示例：报账单实体

```java
/**
 * 报账单 - 聚合根实体
 * 核心业务标识：报账单号 claimNo
 */
public class Claim {
    /** 唯一标识 */
    private ClaimId id;
    /** 业务标识 */
    private ClaimNo claimNo;
    /** 报账单状态（生命周期核心） */
    private ClaimStatus status;
    /** 申请人（ID引用，非对象引用） */
    private UserId applicantId;
    /** 报账金额（值对象） */
    private Money totalAmount;
    /** 报账单行项（实体集合，聚合内部） */
    private List<ClaimLine> lines;

    /**
     * 提交报账单 - 业务行为
     * 保护不变量：只有草稿状态可提交
     */
    public void submit() {
        if (this.status != ClaimStatus.DRAFT) {
            throw new DomainException("只有草稿状态的报账单可以提交");
        }
        if (this.lines.isEmpty()) {
            throw new DomainException("报账单至少包含一个行项");
        }
        this.status = ClaimStatus.SUBMITTED;
        // 发布领域事件
        registerEvent(new ClaimSubmittedEvent(this.id, this.claimNo));
    }

    /**
     * 添加行项 - 维护聚合一致性
     */
    public void addLine(ClaimLine line) {
        this.lines.add(line);
        this.totalAmount = recalculateTotal();
    }
}
```

---

## 2. 值对象（Value Object）

### 定义
没有唯一标识的领域对象，完全由其属性值定义。两个属性相同的值对象被视为相等。

### 识别标准

| 判断条件 | 是值对象 |
|----------|----------|
| 描述实体的某个特征 | ✅ |
| 可以自由替换（相同值=可互换） | ✅ |
| 不可变（创建后不修改） | ✅ |
| 没有独立的生命周期 | ✅ |
| 多个属性组合表达一个完整概念 | ✅ |

### 设计原则

1. **不可变性**：创建后不能修改，变更则创建新实例
2. **自验证**：构造时即验证合法性
3. **无副作用**：方法不修改自身，返回新对象
4. **相等性**：基于所有属性判等，而非引用

### 常见值对象模式

```java
/**
 * 金额 - 典型值对象
 * 组合了数值和币种两个属性表达"钱"的完整概念
 */
public record Money(BigDecimal amount, Currency currency) {

    public Money {
        // 自验证：构造时保证合法性
        if (amount == null || amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new DomainException("金额不能为空或负数");
        }
        Objects.requireNonNull(currency, "币种不能为空");
    }

    /** 加法 - 返回新对象，不修改自身 */
    public Money add(Money other) {
        assertSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }

    /** 乘法 */
    public Money multiply(BigDecimal factor) {
        return new Money(this.amount.multiply(factor), this.currency);
    }
}

/** 地址 - 多属性组合值对象 */
public record Address(String province, String city, String district, String detail) {
    public Address {
        Objects.requireNonNull(province, "省份不能为空");
        Objects.requireNonNull(city, "城市不能为空");
    }
}

/** 日期范围 - 区间型值对象 */
public record DateRange(LocalDate start, LocalDate end) {
    public DateRange {
        if (start != null && end != null && start.isAfter(end)) {
            throw new DomainException("开始日期不能晚于结束日期");
        }
    }

    public boolean contains(LocalDate date) {
        return !date.isBefore(start) && !date.isAfter(end);
    }
}
```

---

## 3. 聚合（Aggregate）与聚合根（Aggregate Root）

### 定义
- **聚合**：一组相关对象的集合，作为数据修改的一致性边界
- **聚合根**：聚合的入口点，外部只能通过聚合根访问聚合内部对象

### 设计规则

| 规则 | 说明 |
|------|------|
| **保护不变量** | 聚合内部的所有业务规则必须始终满足 |
| **事务边界** | 一个事务只修改一个聚合 |
| **通过ID引用** | 聚合间通过ID引用，不持有对方对象引用 |
| **小聚合优先** | 聚合尽量小，仅包含强一致性要求的对象 |
| **最终一致性** | 聚合间使用领域事件实现最终一致性 |

### 聚合边界判定流程

```
1. 识别核心不变量（业务规则）
      ↓
2. 确定哪些对象需要共同维护该不变量
      ↓
3. 这些对象构成一个聚合
      ↓
4. 选择生命周期最长的实体作为聚合根
      ↓
5. 检查：能否进一步拆小？
```

### 示例：报账单聚合

```
┌─────────────────────────────────────┐
│         报账单聚合（Claim）           │
│                                     │
│  ┌───────────┐    ┌──────────────┐  │
│  │   Claim    │───▶│  ClaimLine   │  │
│  │ (聚合根)   │    │  (聚合内实体) │  │
│  └───────────┘    └──────────────┘  │
│       │                             │
│       ▼                             │
│  ┌───────────┐    ┌──────────────┐  │
│  │   Money    │    │  DateRange   │  │
│  │ (值对象)   │    │  (值对象)     │  │
│  └───────────┘    └──────────────┘  │
│                                     │
│  不变量:                             │
│  • 报账金额 = ∑行项金额              │
│  • 草稿状态才可编辑                   │
│  • 至少包含一个行项才可提交            │
└─────────────────────────────────────┘
         │ ID引用
         ▼
┌─────────────────┐
│  审批流聚合       │
│  (另一个聚合)     │
└─────────────────┘
```

### 聚合根代码骨架

```java
public abstract class AggregateRoot<ID> {
    private final ID id;
    private final List<DomainEvent> domainEvents = new ArrayList<>();
    private int version; // 乐观锁

    protected void registerEvent(DomainEvent event) {
        this.domainEvents.add(event);
    }

    public List<DomainEvent> getDomainEvents() {
        return Collections.unmodifiableList(domainEvents);
    }

    public void clearEvents() {
        this.domainEvents.clear();
    }
}
```

---

## 4. 领域服务（Domain Service）

### 何时使用

当业务操作不属于任何一个实体或值对象时，使用领域服务：
- 操作涉及多个聚合的协调
- 操作的概念本身就是一个动作（如"转账"）
- 操作需要外部信息（通过接口注入）

### 判断标准

```
这个行为属于某个实体吗？
    ├── 是 → 放在实体中
    └── 否 → 这个行为涉及多个聚合吗？
              ├── 是 → 领域服务
              └── 否 → 再看是否是纯粹的领域概念
                        ├── 是 → 领域服务
                        └── 否 → 应用服务
```

### 示例

```java
/**
 * 报账金额校验服务 - 领域服务
 * 涉及报账单聚合和预算聚合的协调，不属于任何一个实体
 */
public class ClaimAmountValidationService {

    /**
     * 校验报账金额是否超过预算
     */
    public ValidationResult validate(Claim claim, BudgetLimit budgetLimit) {
        Money claimAmount = claim.getTotalAmount();
        Money remainingBudget = budgetLimit.getRemaining();

        if (claimAmount.isGreaterThan(remainingBudget)) {
            return ValidationResult.fail("报账金额 %s 超过剩余预算 %s",
                claimAmount, remainingBudget);
        }
        return ValidationResult.success();
    }
}
```

---

## 5. 仓储（Repository）

### 设计原则

1. **每个聚合根一个仓储**：不为聚合内部实体创建独立仓储
2. **面向集合接口**：接口设计像操作内存集合（add/remove/findBy）
3. **领域层定义接口**：仓储接口属于领域层，实现属于基础设施层

### 接口定义

```java
/**
 * 报账单仓储 - 领域层接口
 */
public interface ClaimRepository {
    /** 根据ID查找 */
    Optional<Claim> findById(ClaimId id);
    /** 根据业务标识查找 */
    Optional<Claim> findByClaimNo(ClaimNo claimNo);
    /** 保存（新增或更新） */
    void save(Claim claim);
    /** 删除 */
    void remove(Claim claim);
    /** 获取下一个ID */
    ClaimId nextId();
}
```

---

## 6. 工厂（Factory）

### 何时使用

- 创建过程复杂（多步骤、多依赖）
- 需要封装创建逻辑，隐藏具体实现
- 需要根据条件创建不同类型的对象

### 示例

```java
/**
 * 报账单工厂 - 封装复杂创建逻辑
 */
public class ClaimFactory {

    public Claim createExpenseClaim(UserId applicant, String description) {
        ClaimNo claimNo = ClaimNoGenerator.generate("EXP");
        return Claim.builder()
            .id(ClaimId.generate())
            .claimNo(claimNo)
            .applicantId(applicant)
            .description(description)
            .status(ClaimStatus.DRAFT)
            .totalAmount(Money.zero(Currency.CNY))
            .lines(new ArrayList<>())
            .createdAt(LocalDateTime.now())
            .build();
    }
}
```

---

## 检查清单

### 实体检查
- [ ] 有唯一标识
- [ ] 包含业务行为（非贫血模型）
- [ ] 保护了不变量
- [ ] 关联关系使用ID引用

### 值对象检查
- [ ] 不可变
- [ ] 自验证（构造时校验）
- [ ] 基于值判等
- [ ] 无副作用方法

### 聚合检查
- [ ] 边界尽量小
- [ ] 一个事务只修改一个聚合
- [ ] 外部只通过聚合根访问
- [ ] 聚合间通过ID引用
- [ ] 业务不变量在聚合内得到保护
