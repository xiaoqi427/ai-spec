---
name: fix-verify
description: 修复验证工具。在 Bug 修复后编译通过的基础上，提供单元测试发现与执行、数据库数据验证两大能力，生成综合验证报告。编排 db-query 实现数据验证，不重复实现查询逻辑。全部为可选步骤，测试失败不自动阻塞流程，报告给用户决策。可独立使用，也可被 bug-fix-pipeline Phase 3 在编译验证后、git commit 前调用。
allowed-tools: Bash(mvn:*, find:*, python3:*, cat:*, grep:*)
---
# Fix Verify (修复验证工具)

@author: sevenxiao

## 概述

此 skill 专注于 **Bug 修复后的综合验证**，在编译通过（mvn compile）之后、git commit 之前执行。

验证层级:
```
L1 编译验证 (mvn compile)         ← 已有，fix-verify 之前
L2 单元测试 (fix-verify.run-tests) ← 本 skill 提供
L3 数据验证 (fix-verify.verify-data → db-query) ← 本 skill 编排
L4 接口测试 (local-api-test)       ← 已有，fix-verify 之后
```

核心能力:
1. **`discover-tests`** - 根据修改的文件自动发现对应的单元测试类
2. **`run-tests`** - 运行发现的单元测试，解析 Surefire 报告
3. **`verify-data`** - 编排 db-query，根据 Bug 上下文做数据验证
4. **`report`** - 汇总单元测试 + 数据验证结果，生成验证报告

## 外部依赖

| 依赖 | 说明 |
|------|------|
| **JDK 21（必须）** | 项目强制 Java 21，低版本编译/测试不通过 |
| Maven 3.9.6+ | 必须。用于运行单元测试 |
| JUnit 5 (spring-boot-starter-test) | 项目已有。测试框架 |
| Oracle SQLcl (`sql` 命令) | 可选。数据验证需要，由 db-query 负责 |

## 内部依赖

| Skill | 关系 | 说明 |
|-------|------|------|
| `db-query` | 编排调用 | verify-data 操作编排 db-query 的 check-data/trace-branch/verify-fix |

---

## 使用方式

```bash
# 发现修改文件对应的测试类
/skill fix-verify discover-tests --files "T047NewClaimServiceImpl.java,T047SaveClaimServiceImpl.java"

# 运行指定模块的单元测试
/skill fix-verify run-tests --module claim-otc/claim-otc-service --tests "T047NewClaimServiceImplTest,T047LoadClaimServiceImplTest"

# 数据验证（编排 db-query）
/skill fix-verify verify-data --template T047 --claim-no "RMBS2025001234" --fields "STATUS,AMOUNT"

# 生成综合验证报告
/skill fix-verify report --bug-id 5001

# 一键验证（discover + run + report）
/skill fix-verify all --files "T047NewClaimServiceImpl.java" --bug-id 5001
```

---

## 核心能力

### discover-tests (发现相关测试)

**输入**: 修改的文件列表

**匹配策略** (按优先级):

| 优先级 | 匹配方式 | 示例 |
|--------|---------|------|
| 1 | 精确类名匹配 | `XxxServiceImpl.java` → `XxxServiceImplTest.java` |
| 2 | 包路径映射 | `src/main/java/com/yili/...` → `src/test/java/com/yili/...Test.java` |
| 3 | 同包递归查找 | 修改了 `t047/head/impl/` → 查找该包下所有 `*Test.java` |
| 4 | 模块内扫描 | 修改了 `claim-otc-service` → 扫描 `claim-otc-service/src/test/` |

**匹配规则详解**:

```
源文件: claim-otc/claim-otc-service/src/main/java/com/yili/claim/otc/claim/t047/head/impl/T047NewClaimServiceImpl.java

→ 策略1 精确匹配:
  claim-otc/claim-otc-service/src/test/java/com/yili/claim/otc/claim/t047/head/impl/T047NewClaimServiceImplTest.java

→ 策略2 包路径映射:
  将 src/main/java 替换为 src/test/java，类名加 Test 后缀

→ 策略3 同包递归:
  find claim-otc/claim-otc-service/src/test/java/com/yili/claim/otc/claim/t047/ -name "*Test.java"

→ 策略4 模块扫描:
  find claim-otc/claim-otc-service/src/test/ -name "*Test.java"
```

**输出格式**:

```json
{
  "modified_files": ["T047NewClaimServiceImpl.java", "T047SaveClaimServiceImpl.java"],
  "discovered_tests": [
    {
      "test_class": "T047NewClaimServiceImplTest",
      "test_path": "claim-otc/claim-otc-service/src/test/java/com/yili/claim/otc/claim/t047/head/impl/T047NewClaimServiceImplTest.java",
      "module": "claim-otc/claim-otc-service",
      "match_strategy": "exact",
      "source_file": "T047NewClaimServiceImpl.java"
    }
  ],
  "missing_tests": [
    {
      "source_file": "T047SaveClaimServiceImpl.java",
      "source_path": "claim-otc/claim-otc-service/src/main/java/com/yili/claim/otc/claim/t047/head/impl/T047SaveClaimServiceImpl.java",
      "suggested_test_path": "claim-otc/claim-otc-service/src/test/java/com/yili/claim/otc/claim/t047/head/impl/T047SaveClaimServiceImplTest.java"
    }
  ],
  "summary": {
    "total_modified": 2,
    "tests_found": 1,
    "tests_missing": 1,
    "coverage_ratio": "50%"
  }
}
```

**脚本**: `scripts/discover_tests.py`

```bash
python3 scripts/discover_tests.py \
  --files "T047NewClaimServiceImpl.java,T047SaveClaimServiceImpl.java" \
  --project-root /Users/xiaoqi/Documents/work/yili/fssc-claim-service \
  --output json
```

---

### run-tests (运行单元测试)

**输入**: 测试类列表 + 模块路径

**前置条件**: 项目默认 `skipTests=true`，必须显式覆盖

**执行命令**:

```bash
# 运行指定测试类（覆盖 skipTests 配置）
mvn test \
  -pl <module> \
  -Dtest=<Test1>,<Test2> \
  -DskipTests=false \
  -Dmaven.test.skip=false \
  -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository \
  -T 1C \
  --fail-at-end

# 示例
mvn test \
  -pl claim-otc/claim-otc-service \
  -Dtest=T047NewClaimServiceImplTest,T047LoadClaimServiceImplTest \
  -DskipTests=false \
  -Dmaven.test.skip=false \
  -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository \
  -T 1C \
  --fail-at-end
```

**超时**: 单模块最长 5 分钟 (300s)

**结果解析**:

读取 Surefire 报告: `<module>/target/surefire-reports/TEST-*.xml`

```xml
<!-- Surefire XML 结构 -->
<testsuite name="..." tests="10" failures="1" errors="0" skipped="2" time="3.456">
  <testcase name="should_xxx" classname="..." time="0.123"/>
  <testcase name="should_yyy" classname="..." time="0.234">
    <failure message="Expected: 100, Actual: 0">...</failure>
  </testcase>
</testsuite>
```

**输出格式**:

```json
{
  "module": "claim-otc/claim-otc-service",
  "test_classes": ["T047NewClaimServiceImplTest"],
  "execution_time": "3.456s",
  "result": {
    "total": 10,
    "passed": 7,
    "failed": 1,
    "skipped": 2,
    "error": 0
  },
  "failures": [
    {
      "test_class": "T047NewClaimServiceImplTest",
      "test_method": "should_set_default_amount_when_null",
      "message": "Expected: 100, Actual: 0",
      "type": "org.opentest4j.AssertionFailedError"
    }
  ],
  "verdict": "WARN"
}
```

**判定标准**:

| 结果 | verdict | 说明 |
|------|---------|------|
| 全部通过 | PASS | 所有测试绿灯 |
| 有失败但 < 30% | WARN | 测试有失败，报告给用户决策 |
| 失败率 >= 30% | FAIL | 较多测试失败，建议用户检查 |
| 无测试可运行 | SKIP | 没有找到对应测试类 |

**重要**: 测试结果仅作为辅助参考，不自动阻塞 git commit 流程。
将 verdict 报告给用户，由用户决定是否继续提交。

---

### verify-data (数据验证 - 编排 db-query)

**输入**: Bug 上下文 (模板号、报账单号、修复涉及的表/字段)

**编排逻辑**:

此操作不直接执行 SQL，而是编排 db-query skill 的已有能力:

```
verify-data 编排流程:
  │
  ├─ 1. 数据现状检查
  │   └─ db-query.check-data(--template T047 / --claim-no xxx)
  │   → 确认相关数据存在且状态正确
  │
  ├─ 2. 分支走向验证 (如修复涉及条件判断)
  │   └─ db-query.trace-branch(--table <table> --field <field> --where <cond>)
  │   → 确认修复后的代码分支走向正确
  │
  └─ 3. 修复前后对比 (如已执行本地接口测试)
      └─ db-query.verify-fix(--claim-no xxx --fields "STATUS,AMOUNT,...")
      → 对比修复前后数据变化
```

**触发条件**:

| 场景 | 自动编排 | 说明 |
|------|---------|------|
| Bug 涉及报账单操作 | check-data | 查报账单头行状态 |
| Bug 涉及金额计算 | check-data + trace-branch | 查金额字段 + 计算分支 |
| Bug 涉及状态流转 | trace-branch | 查状态字段确认走向 |
| 已执行 local-api-test | verify-fix | 对比接口调用前后数据 |
| 无法确定验证策略 | 跳过 | 不强制数据验证 |

**输出格式**:

```json
{
  "checks": [
    {
      "type": "check-data",
      "description": "查 T047 模板最近报账单状态",
      "result": "数据存在，STATUS=2(已审批)",
      "verdict": "PASS"
    },
    {
      "type": "trace-branch",
      "description": "验证 STATUS 字段分支走向",
      "result": "STATUS=2，走已审批分支，符合预期",
      "verdict": "PASS"
    }
  ],
  "overall_verdict": "PASS"
}
```

---

### report (生成验证报告)

**输入**: Bug ID + 单元测试结果 + 数据验证结果

**输出文件**: `yili-out/bug-prefetch/{bug-id}/verify-report.md`

**报告格式**:

```markdown
## 修复验证报告

**Bug ID**: #5001
**标题**: T044 金额计算错误
**验证时间**: 2026-04-04 14:30:00

### 单元测试

| 指标 | 值 |
|------|-----|
| 测试类 | T044SaveClaimServiceImplTest |
| 总数 | 10 |
| 通过 | 8 |
| 失败 | 1 |
| 跳过 | 1 |
| 耗时 | 3.5s |
| 判定 | WARN |

失败详情:
- `should_calculate_tax_amount`: Expected 150.00, Actual 0.00

### 数据验证

| 检查项 | 结果 |
|--------|------|
| 报账单头状态 | PASS - STATUS=2(已审批) |
| 金额字段分支 | PASS - AMOUNT 走正常计算分支 |

### 综合结论

| 层级 | 结果 |
|------|------|
| 编译 (L1) | PASS |
| 单元测试 (L2) | WARN - 1 个测试失败 |
| 数据验证 (L3) | PASS |

**建议**: 单元测试有 1 个失败，请确认是否与本次修复相关。
```

**verdict 汇总规则**:

| 单元测试 | 数据验证 | 综合 verdict |
|---------|---------|-------------|
| PASS | PASS | PASS |
| PASS | SKIP | PASS |
| WARN | PASS | WARN |
| WARN | FAIL | FAIL |
| FAIL | * | FAIL |
| SKIP | PASS | PASS |
| SKIP | SKIP | SKIP |

---

## 与 Pipeline 集成

fix-verify 在 bug-fix-pipeline Phase 3 中的位置:

```
Phase 3 (action=fix):
  3.6 执行修复 (yili-code-fix.fix)
  3.7 编译验证 (mvn compile -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository)
  │
  3.7.1 [可选] 单元测试验证 (fix-verify)
  │   ├─ fix-verify.discover-tests(modified_files)
  │   ├─ fix-verify.run-tests(discovered_tests)
  │   └─ 测试结果 → verdict (PASS/WARN/FAIL/SKIP)
  │
  3.7.2 [可选] 数据验证 (fix-verify → db-query)
  │   └─ fix-verify.verify-data(bug_context)
  │       ├─ db-query.check-data
  │       ├─ db-query.trace-branch
  │       └─ db-query.verify-fix
  │
  3.8 [可选] 本地接口测试 (local-api-test)
  3.9 git commit
```

### 结果写入 fix-queue.json

验证结果记录到 `fix-queue.json.results[bug-id]`:

```json
{
  "5001": {
    "status": "fixed",
    "files": ["..."],
    "compile": "pass",
    "unit_test": {
      "verdict": "WARN",
      "total": 10,
      "passed": 8,
      "failed": 1,
      "skipped": 1,
      "failures": ["should_calculate_tax_amount"]
    },
    "data_verify": {
      "verdict": "PASS",
      "checks": 2,
      "passed": 2
    },
    "local_test": "pass",
    "commit_hash": "abc1234",
    "comment_draft": "..."
  }
}
```

### Phase 5 评论引用

Phase 5 生成 Coding 评论时，如果有验证结果，追加到评论中:

```
仅供参考：
修复文件: ...
编译: 通过
单元测试: 8/10 通过 (1 失败, 1 跳过)
数据验证: 2/2 通过
```

---

## 关键约束

1. **全部可选**: 所有验证步骤标记为 `[可选]`，不阻塞主流程
2. **不自动阻塞**: 测试失败报告给用户决策，不自动阻止 git commit
3. **编排不重复**: 数据验证编排 db-query，不自己写 SQL
4. **超时保护**: 单元测试单模块最长 5 分钟
5. **增量运行**: 只运行与修改文件相关的测试，不全量跑
6. **报告持久化**: 验证报告保存到本地，供 Phase 5 引用

## 参考

- 测试模式参考: [references/test-patterns.md](references/test-patterns.md)
- 测试发现脚本: [scripts/discover_tests.py](scripts/discover_tests.py)
- 数据库查询: `ai-spec/skills/code/bug-fix-cycle/db-query/SKILL.md`
- Pipeline 编排: `ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/SKILL.md`
