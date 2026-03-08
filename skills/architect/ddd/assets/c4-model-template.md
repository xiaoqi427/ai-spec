# C4 模型模板

> C4 模型提供四个层次的架构视图：系统上下文、容器、组件、代码。
> 使用 Mermaid 语法，可直接在 Markdown 中渲染。

---

## Level 1: 系统上下文图（System Context）

**目的**: 展示系统与外部用户、外部系统的关系

```mermaid
graph TB
    User[用户/角色名称]
    System[目标系统名称]
    External1[外部系统1]
    External2[外部系统2]

    User -->|使用| System
    System -->|调用| External1
    System -->|集成| External2
```

**填写模板**:

```yaml
system_context:
  system:
    name: "{系统名称}"
    description: "{系统一句话描述}"
  
  users:
    - name: "{用户角色1}"
      description: "{角色描述}"
      interaction: "{如何使用系统}"
    - name: "{用户角色2}"
      description: "{角色描述}"
      interaction: "{如何使用系统}"
  
  external_systems:
    - name: "{外部系统1}"
      description: "{系统描述}"
      interaction: "{集成方式和目的}"
    - name: "{外部系统2}"
      description: "{系统描述}"
      interaction: "{集成方式和目的}"
```

### 示例：财务共享服务中心

```mermaid
graph TB
    Employee[员工]
    Approver[审批人]
    Finance[财务人员]
    FSSC[财务共享服务中心]
    Bank[银行系统]
    Tax[税务系统]
    ERP[ERP系统]

    Employee -->|提交报账单| FSSC
    Approver -->|审批单据| FSSC
    Finance -->|处理支付/记账| FSSC
    FSSC -->|付款指令| Bank
    FSSC -->|发票验真| Tax
    FSSC -->|凭证同步| ERP
```

---

## Level 2: 容器图（Container）

**目的**: 展示系统内部的技术构成（服务、数据库、消息队列等）

```mermaid
graph TB
    subgraph 目标系统
        WebApp[Web前端]
        Service1[服务1]
        Service2[服务2]
        DB1[(数据库1)]
        MQ[消息队列]
    end

    WebApp -->|REST API| Service1
    Service1 -->|读写| DB1
    Service1 -->|发布事件| MQ
    MQ -->|消费事件| Service2
```

**填写模板**:

```yaml
containers:
  - name: "{容器名称}"
    type: "Web App / Service / Database / MQ / Cache"
    technology: "{技术栈}"
    description: "{容器职责}"
    
  relationships:
    - from: "{容器A}"
      to: "{容器B}"
      description: "{交互说明}"
      technology: "{通信技术}"
```

### 示例：FSSC 容器图

```mermaid
graph TB
    subgraph FSSC财务共享服务中心
        Web[fssc-web<br/>Vue.js前端]
        Gateway[fssc-gateway<br/>Spring Cloud Gateway]
        ClaimSvc[fssc-claim-service<br/>报账服务]
        ConfigSvc[fssc-config-service<br/>配置服务]
        BpmSvc[fssc-bpm-service<br/>审批服务]
        FundSvc[fssc-fund-service<br/>资金服务]
        VoucherSvc[fssc-voucher-service<br/>凭证服务]
        MySQL[(MySQL)]
        Redis[(Redis)]
        RabbitMQ[RabbitMQ]
    end

    Web -->|HTTP| Gateway
    Gateway -->|路由| ClaimSvc
    Gateway -->|路由| ConfigSvc
    ClaimSvc -->|Feign| ConfigSvc
    ClaimSvc -->|Feign| BpmSvc
    ClaimSvc -->|事件| RabbitMQ
    RabbitMQ -->|消费| FundSvc
    RabbitMQ -->|消费| VoucherSvc
    ClaimSvc -->|读写| MySQL
    ClaimSvc -->|缓存| Redis
```

---

## Level 3: 组件图（Component）

**目的**: 展示单个容器内部的组件结构（对应 DDD 分层）

```mermaid
graph TB
    subgraph 服务名称
        Controller[Controller层]
        AppService[应用服务层]
        DomainModel[领域模型层]
        DomainService[领域服务]
        Repository[仓储接口]
        RepoImpl[仓储实现]
        Mapper[数据访问层]
    end

    Controller --> AppService
    AppService --> DomainModel
    AppService --> DomainService
    DomainService --> Repository
    RepoImpl --> Repository
    RepoImpl --> Mapper
```

**填写模板**:

```yaml
components:
  container: "{所属容器名称}"
  layers:
    interface:
      - name: "{Controller名}"
        responsibility: "{职责}"
    application:
      - name: "{Application Service名}"
        responsibility: "{职责}"
    domain:
      entities:
        - name: "{Entity名}"
          type: "aggregate_root / entity / value_object"
      services:
        - name: "{Domain Service名}"
          responsibility: "{职责}"
      repositories:
        - name: "{Repository名}"
    infrastructure:
      - name: "{实现类名}"
        responsibility: "{职责}"
```

### 示例：报账服务组件图

```mermaid
graph TB
    subgraph fssc-claim-service
        ClaimCtrl[ClaimController]
        ClaimApp[ClaimApplicationService]
        ClaimAgg[Claim 聚合根]
        ClaimLine[ClaimLine 实体]
        Money[Money 值对象]
        ClaimDomSvc[ClaimAmountValidationService]
        ClaimRepo[ClaimRepository 接口]
        ClaimRepoImpl[ClaimRepositoryImpl]
        ClaimMapper[ClaimDoMapper]
    end

    ClaimCtrl --> ClaimApp
    ClaimApp --> ClaimAgg
    ClaimApp --> ClaimDomSvc
    ClaimAgg --> ClaimLine
    ClaimAgg --> Money
    ClaimDomSvc --> ClaimRepo
    ClaimApp --> ClaimRepo
    ClaimRepoImpl --> ClaimRepo
    ClaimRepoImpl --> ClaimMapper
```

---

## Level 4: 代码图（Code）

**目的**: 展示类级别的详细设计（通常由 IDE 自动生成，此处提供类图模板）

```mermaid
classDiagram
    class AggregateRoot {
        -ID id
        -List~DomainEvent~ events
        +registerEvent(event)
        +clearEvents()
    }

    class Claim {
        -ClaimId id
        -ClaimNo claimNo
        -ClaimStatus status
        -Money totalAmount
        -List~ClaimLine~ lines
        +submit()
        +approve()
        +addLine(line)
    }

    class ClaimLine {
        -ClaimLineId id
        -String description
        -Money amount
        -ExpenseTypeCode expenseType
    }

    class Money {
        -BigDecimal amount
        -Currency currency
        +add(other) Money
        +multiply(factor) Money
    }

    AggregateRoot <|-- Claim
    Claim "1" --> "*" ClaimLine
    Claim --> Money
    ClaimLine --> Money
```

---

## 使用说明

1. **自顶向下**: 从 Level 1 开始，逐层细化
2. **按需深入**: 不需要每个组件都画到 Level 4
3. **保持更新**: 架构变更时同步更新图表
4. **受众适配**: Level 1-2 给管理层看，Level 3-4 给开发团队看
