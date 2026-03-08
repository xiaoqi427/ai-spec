# 通用语言（Ubiquitous Language）

## 1. 核心概念

通用语言是领域驱动设计的基石。它是开发团队与领域专家共享的语言，贯穿于对话、文档、代码和测试中。

### 核心原则

| 原则 | 说明 |
|------|------|
| **统一性** | 团队中每个人（开发、产品、业务）使用相同的术语表达相同的概念 |
| **精确性** | 每个术语有且仅有一个明确的含义，消除歧义 |
| **演进性** | 语言随着对领域理解的深入而不断演进 |
| **代码即语言** | 代码中的类名、方法名、变量名必须与通用语言一致 |

### 反模式

```
❌ 开发说"表单"，业务说"报账单"，文档写"申请单" → 三个词指同一概念
❌ 代码中用 form/bill/request 等不同命名 → 术语不一致
❌ 同一个词在不同上下文含义不同却未区分 → 歧义
✅ 统一使用"报账单（Claim）"，代码中对应 Claim 类
```

---

## 2. 术语表构建方法

### 2.1 收集术语

**来源**:
- 领域专家访谈
- 业务流程文档
- 现有系统界面和代码
- 行业标准术语

**步骤**:
```
1. 列出所有业务术语（中英文）
2. 标注每个术语的定义和边界
3. 识别同义词并统一
4. 识别多义词并按上下文区分
5. 团队评审确认
```

### 2.2 术语表模板

```yaml
# 术语表 - {领域名称}
# 最后更新: {日期}

terms:
  - name: 报账单
    english: Claim
    definition: 员工或部门提交的费用报销或采购支付请求单据
    bounded_context: 报账上下文
    aliases: []  # 不允许别名，统一使用"报账单"
    code_mapping:
      entity: Claim
      table: t_claim
      api_path: /claims
    examples:
      - 差旅费报账单
      - 采购付款报账单
    notes: 不要与"发票(Invoice)"混淆，报账单是内部流程单据

  - name: 报账单行
    english: ClaimLine
    definition: 报账单中的明细项，记录具体的费用或采购项
    bounded_context: 报账上下文
    parent: 报账单
    code_mapping:
      entity: ClaimLine
      table: t_claim_line
    invariants:
      - 金额不能为负数
      - 必须关联一个费用类型

  - name: 费用类型
    english: ExpenseType
    definition: 对报账费用进行分类的标准编码
    bounded_context: 配置上下文
    code_mapping:
      entity: ExpenseType
      table: t_expense_type
    examples:
      - 差旅费
      - 办公费
      - 业务招待费
```

---

## 3. 业务规则表达

### 3.1 规则分类

| 类型 | 说明 | 示例 |
|------|------|------|
| **不变量** | 始终为真的约束 | "报账金额 = 所有行项金额之和" |
| **前置条件** | 操作执行前必须满足的条件 | "只有草稿状态的报账单可以提交" |
| **后置条件** | 操作执行后保证的状态 | "提交后报账单状态变为待审批" |
| **推导规则** | 值由其他值计算得出 | "税额 = 金额 × 税率" |

### 3.2 规则表达规范

**使用自然语言 + 结构化格式**:

```yaml
rule:
  name: 报账单提交规则
  type: 前置条件
  context: 报账上下文
  when: 用户点击"提交"按钮
  given:
    - 报账单状态为"草稿"
    - 报账单至少包含一个行项
    - 所有行项金额大于零
    - 申请人已关联部门
  then:
    - 报账单状态变更为"待审批"
    - 生成审批流程实例
    - 发送"报账单已提交"事件
  otherwise:
    - 返回具体的校验失败原因
```

### 3.3 规则到代码的映射

```java
// 通用语言: "只有草稿状态的报账单可以提交，且至少包含一个行项"
// 代码直接反映业务规则，方法名和变量名使用通用语言

public class Claim {

    public void submit() {
        // 前置条件：草稿状态
        assertDraftStatus();
        // 前置条件：至少一个行项
        assertHasLines();
        // 后置条件：状态变更
        this.status = ClaimStatus.SUBMITTED;
        // 后置条件：发布事件
        registerEvent(new ClaimSubmittedEvent(this.id));
    }

    private void assertDraftStatus() {
        if (this.status != ClaimStatus.DRAFT) {
            throw new ClaimNotEditableException(
                "报账单 %s 当前状态为 %s，只有草稿状态可提交",
                this.claimNo, this.status.getDescription());
        }
    }

    private void assertHasLines() {
        if (this.lines == null || this.lines.isEmpty()) {
            throw new ClaimValidationException(
                "报账单 %s 至少需要一个行项才能提交", this.claimNo);
        }
    }
}
```

---

## 4. 模型验证

### 4.1 语言一致性检查

```
检查项:
□ 代码中的类名是否与术语表一致
□ 方法名是否使用业务动词（submit/approve/reject 而非 update/process）
□ 变量名是否使用业务名词（claim/line 而非 data/item/obj）
□ 异常信息是否使用业务语言
□ API 路径是否使用业务术语
□ 数据库表名/字段名是否与模型对应
```

### 4.2 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| **术语不统一** | 同一概念多种叫法 | 建立术语表，团队对齐 |
| **贫血语言** | 代码只有 getter/setter | 将业务规则移入实体 |
| **技术语言污染** | 类名如 DataProcessor | 用业务术语重命名 |
| **隐式概念** | 业务规则写在注释中 | 提炼为显式的类或方法 |

---

## 5. 实践示例

### 示例1: 财务共享中心术语对齐

**问题**: 系统中"报账"相关概念混乱

```
旧代码术语          →  统一后的通用语言
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Form               →  Claim（报账单）
FormLine           →  ClaimLine（报账单行）
Bill               →  Claim（报账单）
ApplyAmount        →  ClaimAmount（报账金额）
CheckStatus        →  ApprovalStatus（审批状态）
doSubmit()         →  submit()（提交）
doCheck()          →  approve()（审批通过）
doReject()         →  reject()（审批驳回）
```

### 示例2: 跨上下文术语区分

```yaml
# "用户"在不同上下文中含义不同

contexts:
  报账上下文:
    term: 申请人（Applicant）
    definition: 提交报账单的员工
    attributes: [员工号, 姓名, 部门]

  审批上下文:
    term: 审批人（Approver）
    definition: 审批报账单的管理者
    attributes: [员工号, 姓名, 审批权限, 审批额度]

  支付上下文:
    term: 收款人（Payee）
    definition: 接收报账款项的账户持有人
    attributes: [姓名, 银行账号, 开户行]
```

### 示例3: 隐式概念显式化

```java
// ❌ 隐式概念：业务规则隐藏在条件判断中
if (amount > 5000 && level < 3) {
    // 需要高级审批
}

// ✅ 显式概念：提炼为领域概念
public class ApprovalPolicy {
    /** 审批策略：判断是否需要高级审批 */
    public boolean requiresSeniorApproval(Money amount, ApprovalLevel level) {
        return amount.isGreaterThan(SENIOR_APPROVAL_THRESHOLD)
            && level.isBelow(ApprovalLevel.SENIOR);
    }
}
```

---

## 检查清单

- [ ] 已建立领域术语表
- [ ] 术语表覆盖所有核心业务概念
- [ ] 代码命名与术语表一致
- [ ] 不存在同义词（多个词表达同一概念）
- [ ] 不存在多义词（同一词在不同场景含义不同但未区分）
- [ ] 业务规则在代码中有明确体现
- [ ] 异常信息使用业务语言
