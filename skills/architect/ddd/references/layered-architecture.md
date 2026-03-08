# 分层架构设计原则

## 1. DDD 分层架构概览

```
┌──────────────────────────────────┐
│         接口层 (Interface)        │  Controller / API / DTO
├──────────────────────────────────┤
│         应用层 (Application)      │  应用服务 / 命令处理 / 编排
├──────────────────────────────────┤
│         领域层 (Domain)           │  实体 / 值对象 / 领域服务 / 仓储接口
├──────────────────────────────────┤
│       基础设施层 (Infrastructure)  │  持久化 / 消息 / 外部集成
└──────────────────────────────────┘

依赖规则: 上层依赖下层，领域层不依赖任何层
```

---

## 2. 各层职责与规则

### 2.1 接口层（Interface / Presentation）

**职责**: 接收外部请求，转换参数，返回响应

**包含**:
- REST Controller
- 请求/响应 DTO
- 参数校验（格式校验）
- DTO ↔ 领域对象转换

**规则**:
```
✅ 接收 HTTP 请求，调用应用层
✅ 参数格式校验（@Valid, @NotNull）
✅ DTO 转换
❌ 禁止包含业务逻辑
❌ 禁止直接调用领域层或基础设施层
❌ 禁止操作数据库
```

**示例**:
```java
@RestController
@RequestMapping("/api/claims")
@Slf4j
public class ClaimController {

    @Resource
    private ClaimApplicationService claimApplicationService;

    @PostMapping
    @Operation(summary = "创建报账单")
    public Result<ClaimDto> create(@Valid @RequestBody CreateClaimCommand cmd) {
        // 仅调用应用层，不含业务逻辑
        ClaimDto result = claimApplicationService.createClaim(cmd);
        return Result.success(result);
    }
}
```

### 2.2 应用层（Application）

**职责**: 协调领域对象完成用例，不包含业务规则

**包含**:
- 应用服务（Application Service）
- 命令/查询对象（Command / Query）
- 事务管理
- 安全与权限检查
- 领域事件发布

**规则**:
```
✅ 编排领域对象和领域服务
✅ 管理事务边界
✅ 权限检查
✅ 发布领域事件
❌ 禁止包含业务规则（if 业务判断）
❌ 禁止直接操作数据库
❌ 业务规则必须委托给领域层
```

**关键区分**: 应用层"薄而扁"，只做编排，不做决策。

**示例**:
```java
@Service
@Slf4j
public class ClaimApplicationService {

    @Resource
    private ClaimRepository claimRepository;
    @Resource
    private ClaimFactory claimFactory;
    @Resource
    private ClaimAmountValidationService validationService;
    @Resource
    private ApplicationEventPublisher eventPublisher;

    /**
     * 创建报账单 - 应用层编排
     * 注意：业务规则在领域对象中，这里只做协调
     */
    @Transactional(rollbackFor = Exception.class)
    public ClaimDto createClaim(CreateClaimCommand cmd) {
        // 1. 使用工厂创建领域对象
        Claim claim = claimFactory.create(cmd);
        // 2. 持久化
        claimRepository.save(claim);
        // 3. 发布事件
        claim.getDomainEvents().forEach(eventPublisher::publishEvent);
        claim.clearEvents();
        // 4. 转换返回
        return ClaimDtoConverter.INSTANCE.toDto(claim);
    }

    /**
     * 提交报账单
     */
    @Transactional(rollbackFor = Exception.class)
    public void submitClaim(ClaimId claimId) {
        // 1. 加载聚合
        Claim claim = claimRepository.findById(claimId)
            .orElseThrow(() -> new EntityNotFoundException("报账单不存在"));
        // 2. 调用领域行为（业务规则在 Claim.submit() 中）
        claim.submit();
        // 3. 保存
        claimRepository.save(claim);
        // 4. 发布事件
        claim.getDomainEvents().forEach(eventPublisher::publishEvent);
        claim.clearEvents();
    }
}
```

### 2.3 领域层（Domain）

**职责**: 表达业务概念、业务规则和业务状态

**包含**:
- 实体（Entity）
- 值对象（Value Object）
- 聚合根（Aggregate Root）
- 领域服务（Domain Service）
- 仓储接口（Repository Interface）
- 领域事件（Domain Event）
- 工厂（Factory）

**规则**:
```
✅ 包含所有业务规则和不变量
✅ 定义仓储接口（不实现）
✅ 定义领域事件
✅ 领域服务处理跨实体逻辑
❌ 禁止依赖框架（Spring, MyBatis 等）
❌ 禁止依赖基础设施
❌ 禁止直接访问数据库
❌ 禁止依赖接口层或应用层
```

**核心原则**: 领域层是系统的心脏，应该是**纯粹的 Java 代码**，不依赖任何框架。

**示例**:
```java
// ===== 领域层：纯业务逻辑，无框架依赖 =====

/** 报账单聚合根 */
public class Claim extends AggregateRoot<ClaimId> {

    private ClaimNo claimNo;
    private ClaimStatus status;
    private UserId applicantId;
    private Money totalAmount;
    private List<ClaimLine> lines;

    /** 业务规则：提交 */
    public void submit() {
        assertStatus(ClaimStatus.DRAFT, "只有草稿状态可提交");
        assertNotEmpty(lines, "至少包含一个行项");
        this.status = ClaimStatus.SUBMITTED;
        registerEvent(new ClaimSubmittedEvent(this.id, this.claimNo));
    }

    /** 业务规则：审批通过 */
    public void approve() {
        assertStatus(ClaimStatus.SUBMITTED, "只有已提交的报账单可审批");
        this.status = ClaimStatus.APPROVED;
        registerEvent(new ClaimApprovedEvent(this.id, this.totalAmount));
    }
}

/** 仓储接口 - 领域层定义，基础设施层实现 */
public interface ClaimRepository {
    Optional<Claim> findById(ClaimId id);
    void save(Claim claim);
}

/** 领域服务 */
public class ClaimAmountValidationService {
    public ValidationResult validate(Claim claim, BudgetLimit limit) {
        if (claim.getTotalAmount().isGreaterThan(limit.getRemaining())) {
            return ValidationResult.fail("超过预算限额");
        }
        return ValidationResult.success();
    }
}
```

### 2.4 基础设施层（Infrastructure）

**职责**: 技术实现细节，包括持久化、消息、外部服务集成

**包含**:
- 仓储实现（Repository Implementation）
- 数据库访问（MyBatis Mapper, JPA Repository）
- 消息队列发送/接收
- 外部服务客户端
- 文件存储
- 缓存实现

**规则**:
```
✅ 实现领域层定义的接口
✅ 数据库访问和 ORM 映射
✅ DO ↔ 领域对象转换
✅ 外部系统集成
❌ 禁止包含业务逻辑
❌ 禁止被领域层依赖
```

**示例**:
```java
/** 仓储实现 - 基础设施层 */
@Repository
public class ClaimRepositoryImpl implements ClaimRepository {

    @Resource
    private ClaimDoMapper claimDoMapper;
    @Resource
    private ClaimLineDOMapper claimLineDoMapper;

    @Override
    public Optional<Claim> findById(ClaimId id) {
        ClaimDo claimDo = claimDoMapper.selectById(id.getValue());
        if (claimDo == null) {
            return Optional.empty();
        }
        List<ClaimLineDo> lineDos = claimLineDoMapper
            .selectList(new LambdaQueryWrapper<ClaimLineDo>()
                .eq(ClaimLineDo::getClaimId, id.getValue()));
        // DO → 领域对象转换
        return Optional.of(ClaimAssembler.toDomain(claimDo, lineDos));
    }

    @Override
    public void save(Claim claim) {
        ClaimDo claimDo = ClaimAssembler.toDo(claim);
        claimDoMapper.insertOrUpdate(claimDo);
    }
}
```

---

## 3. 依赖方向

```
接口层 → 应用层 → 领域层 ← 基础设施层

关键: 基础设施层依赖领域层（依赖倒置）
      领域层不依赖任何其他层
```

### 依赖倒置原则

```java
// 领域层定义接口
public interface ClaimRepository {
    Optional<Claim> findById(ClaimId id);
}

// 基础设施层实现接口
@Repository
public class ClaimRepositoryImpl implements ClaimRepository {
    // MyBatis 实现细节
}

// 应用层通过接口使用
@Service
public class ClaimApplicationService {
    @Resource
    private ClaimRepository claimRepository; // 依赖接口，非实现
}
```

---

## 4. CQRS 模式（可选）

对于复杂查询场景，可引入 CQRS（命令查询职责分离）：

```
命令侧 (Command):
  Controller → Application Service → Domain → Repository

查询侧 (Query):
  Controller → Query Service → 直接查数据库（跳过领域层）
```

**适用条件**:
- 读写模型差异大
- 查询需要跨多个聚合的数据
- 需要专门的查询优化

---

## 5. 层间数据传递

```
接口层          应用层          领域层          基础设施层
  DTO    ←→    Command/DTO  ←→  Entity/VO   ←→    DO
                              
  请求DTO →     Command     →   实体操作    →    DO 持久化
  响应DTO ←     DTO转换      ←   实体返回    ←    DO 查询
```

| 层 | 使用的对象 | 转换时机 |
|----|-----------|----------|
| 接口层 | Request/Response DTO | 入口转 Command，出口转 DTO |
| 应用层 | Command / DTO | 调用领域层时传入参数 |
| 领域层 | Entity / Value Object | 纯业务对象 |
| 基础设施层 | DO (Data Object) | 仓储中 DO ↔ Entity 转换 |

---

## 检查清单

- [ ] 领域层不依赖任何框架
- [ ] 业务规则全部在领域层
- [ ] 应用层只做编排，不含业务判断
- [ ] 接口层只做参数转换和调用应用层
- [ ] 基础设施层实现领域层定义的接口
- [ ] 依赖方向正确（上层依赖下层，基础设施依赖领域层）
- [ ] 每层使用正确的数据对象类型
