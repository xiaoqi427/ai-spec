---
name: db-query
description: Oracle 数据库查询工具。在 Bug 修复过程中查询业务数据，辅助定位前端调不到数据、后端逻辑分支判断、修复后数据验证等场景。支持自由查询、按报账单号/模板编号自动生成查询、修复前后数据对比、字段值分支追踪。可独立使用，也可被 bug-fix-pipeline 在分析/测试/验证环节调用。
allowed-tools: Bash(sql:*, cat:*, grep:*, python3:*)
---
# DB Query (数据库查询工具)
@author: sevenxiao

## 概述

此 skill 专注于在 **Bug 修复过程中查询 Oracle 数据库**，辅助定位和验证问题。

核心能力:
1. **`query`** - 自由 SQL 查询，执行任意 SELECT 语句
2. **`check-data`** - 按 Bug 上下文自动生成查询（报账单号、模板编号等）
3. **`verify-fix`** - 修复前后数据对比验证
4. **`trace-branch`** - 查字段值判断代码走哪个分支

## 外部依赖

| 依赖 | 说明 |
|------|------|
| Oracle SQLcl (`sql` 命令) | 必须。Oracle 命令行客户端，用于执行 SQL |

验证安装:
```bash
which sql
sql -version
```

如果 `sql` 命令不可用，可以使用 `sqlplus` 替代（需要调整连接字符串格式）。

---

## 使用方式

```bash
# 自由查询
/skill db-query query "SELECT * FROM T_RMBS_CLAIM WHERE CLAIM_NO = 'xxx'"

# 按报账单号查询头行数据
/skill db-query check-data --claim-no "RMBS2025001234"

# 按模板编号查最近报账单
/skill db-query check-data --template T044 --limit 10

# 修复前后对比
/skill db-query verify-fix --claim-no "RMBS2025001234" --fields "STATUS,AMOUNT,MODIFIER_ID"

# 查字段值判断分支
/skill db-query trace-branch --table T_RMBS_CLAIM --where "CLAIM_NO='xxx'" --field STATUS

# 指定环境
/skill db-query query --env sit "SELECT ..."
```

---

## 连接配置

### 配置文件

路径: `ai-spec/skills/code/bug-fix-cycle/db-query/config/db-connection.yaml`

从模板复制并填写:
```bash
cp config/db-connection.yaml.example config/db-connection.yaml
# 编辑填写密码
```

配置文件已加入 `.gitignore`，不会提交到代码库。

### 连接方式

使用 Oracle SQLcl 连接:
```bash
sql '<username>/<password>'@<host>:<port>/<sid>
```

参考 `oracle-dba/scripts/run_resource_hog.sh` 的连接方式。

---

## 核心能力

### query (自由查询)

**输入**: SQL 语句（字符串）

**执行流程**:

```bash
# 1. 读取连接配置
# 从 config/db-connection.yaml 读取目标环境的连接信息

# 2. 安全检查
# 检查 SQL 是否为 SELECT 语句
# 如果包含 INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE → 必须先询问用户确认

# 3. 生成临时 SQL 文件
cat > /tmp/db_query_tmp.sql << 'EOSQL'
SET LINESIZE 300
SET PAGESIZE 1000
SET FEEDBACK ON
SET VERIFY OFF
SET LONG 10000
SET TRIMSPOOL ON

SPOOL <output_dir>/query_<timestamp>.txt

<用户的 SQL>;

SPOOL OFF
EXIT
EOSQL

# 4. 执行查询
./scripts/run_query.sh "<SQL语句>"

# 5. 读取并格式化输出
cat <output_dir>/query_latest.txt
```

**输出格式**:
```markdown
## 查询结果

**SQL**: `SELECT * FROM T_RMBS_CLAIM WHERE CLAIM_NO = 'xxx'`
**环境**: local (10.119.254.69:1521/yldb)
**时间**: 2026-04-04 10:30:00
**行数**: 1

| CLAIM_NO | STATUS | TEMPLATE_ID | AMOUNT | CREATOR |
|----------|--------|-------------|--------|---------|
| xxx      | 2      | T044        | 1500.00 | zhangsan |

**结果已保存**: output/query_20260404_103000.txt
```

---

### check-data (按 Bug 上下文查询)

**输入**: Bug 上下文信息（报账单号、模板编号、用户名等）

**自动生成查询策略**:

| 输入条件 | 自动生成的查询 |
|----------|--------------|
| `--claim-no` | 查报账单头 + 行数据 |
| `--template` | 查该模板最近的报账单列表 |
| `--user` | 查该用户最近的报账单 |
| `--table --where` | 按条件查指定表 |

**按报账单号查询**:

```sql
-- 1. 查报账单头
SELECT CLAIM_NO, TEMPLATE_ID, STATUS, TOTAL_AMOUNT,
       CREATOR, CREATE_TIME, MODIFIER, MODIFY_TIME,
       OU_CODE, COMPANY_CODE
FROM T_RMBS_CLAIM
WHERE CLAIM_NO = '&claim_no';

-- 2. 查报账单行
SELECT LINE_NO, ITEM_CODE, ITEM_NAME, AMOUNT,
       CURRENCY_CODE, TAX_AMOUNT
FROM T_RMBS_CLAIM_ITEM
WHERE CLAIM_NO = '&claim_no'
ORDER BY LINE_NO;

-- 3. 查支付信息
SELECT PAYLIST_NO, PAY_STATUS, PAY_AMOUNT,
       BANK_ACCOUNT, PAYEE_NAME
FROM T_RMBS_PAYLIST
WHERE CLAIM_NO = '&claim_no';
```

**按模板编号查最近报账单**:

```sql
SELECT CLAIM_NO, STATUS, TOTAL_AMOUNT,
       CREATOR, CREATE_TIME
FROM T_RMBS_CLAIM
WHERE TEMPLATE_ID = '&template_id'
ORDER BY CREATE_TIME DESC
FETCH FIRST &limit ROWS ONLY;
```

**执行步骤**:

1. 根据输入参数确定查询策略
2. 生成对应 SQL（可能是多条）
3. 依次执行并汇总结果
4. 分析数据含义（状态码 → 状态名、金额校验等）

**数据含义解读**:

查询完成后，自动解读关键字段:
- STATUS 字段: 0=草稿, 1=待审批, 2=已审批, 3=已退回, 4=已作废
- 金额字段: 检查头行合计是否一致
- 时间字段: 格式化为可读时间
- 关联字段: 提示可以继续查关联表

---

### verify-fix (修复验证)

**输入**: 报账单号 + 关注的字段列表

**执行流程**:

```
1. 修复前: 执行查询，记录当前数据 → 保存为 before_<timestamp>.txt
2. 用户修复代码 + 执行操作
3. 修复后: 再次执行相同查询 → 保存为 after_<timestamp>.txt
4. 对比: diff before after → 输出变化的字段
```

**对比输出**:

```markdown
## 修复验证对比

**报账单号**: RMBS2025001234
**关注字段**: STATUS, AMOUNT, MODIFIER_ID

| 字段 | 修复前 | 修复后 | 变化 |
|------|--------|--------|------|
| STATUS | 1 | 2 | 待审批 → 已审批 |
| AMOUNT | 1500.00 | 1500.00 | 无变化 |
| MODIFIER_ID | zhangsan | lisi | 已更新 |

**结论**: 修复生效，MODIFIER_ID 已正确更新
```

---

### trace-branch (分支追踪)

**输入**: 表名 + 条件 + 关注字段

**场景**: 后端代码有 if/switch 逻辑，需要知道数据库中该字段的当前值来判断走哪个分支。

**执行步骤**:

```bash
# 1. 查字段值
SELECT <field> FROM <table> WHERE <condition>;

# 2. 输出值 + 对应的代码分支提示
```

**输出格式**:

```markdown
## 分支追踪结果

**表**: T_RMBS_CLAIM
**条件**: CLAIM_NO = 'xxx'
**字段**: STATUS
**当前值**: 2

根据代码逻辑:
- STATUS = 0 → 走草稿保存分支
- STATUS = 1 → 走提交审批分支
- **STATUS = 2 → 走已审批分支** (当前)
- STATUS = 3 → 走退回分支

当前数据会走 "已审批" 分支。
```

---

## 与 Pipeline 集成

db-query 可在 bug-fix-pipeline 的多个环节按需调用:

```
Step 2.2 分析 Bug
  └─ [可选] db-query.check-data
     → 查库了解报账单当前状态、字段值
     → 辅助判断是数据问题还是逻辑问题

Step 2.5 修复代码时
  └─ [可选] db-query.trace-branch
     → 查字段值确定代码走哪个分支
     → 辅助理解业务逻辑

Step 2.6 本地接口测试后
  └─ [可选] db-query.verify-fix
     → 验证接口调用后数据是否正确写入

Step 2.10 SIT 验证分析时
  └─ [推荐] db-query.query (--env sit)
     → API 返回错误时查库对比实际数据
     → 判断是查询逻辑问题还是数据本身问题
```

### 在 sit-verify-analyze 中的使用

当 API 返回错误时，新增 DB 验证路径:

```
API 返回错误
  │
  ├─ db-query.query → 查库确认数据
  │
  ├─ 库里有正确数据 + API 没返回 → 后端查询逻辑有问题（SQL/条件/映射）
  ├─ 库里没数据 → 后端写入逻辑有问题（保存未生效）
  └─ 库里数据不对 → 数据本身有问题（历史脏数据/并发问题）
```

---

## 查询脚本

### 通用查询脚本

路径: `scripts/run_query.sh`

```bash
# 执行 SQL 文件
./scripts/run_query.sh @scripts/common_queries.sql

# 执行内联 SQL
./scripts/run_query.sh "SELECT * FROM T_RMBS_CLAIM WHERE ROWNUM <= 5"

# 指定环境
./scripts/run_query.sh --env sit "SELECT ..."
```

### 常用查询模板

路径: `scripts/common_queries.sql`

预置了按报账单号、模板编号、用户等常用查询。

### 业务表映射

路径: `references/table-mapping.md`

包含系统所有业务表名、对应 DO 类和说明，方便快速定位要查哪个表。

---

## SQL 生成规则

AI 在自动生成 SQL 时必须遵守:

1. **默认加 ROWNUM/FETCH FIRST 限制**: 防止全表扫描拖垮数据库
   ```sql
   -- 默认最多返回 100 行
   FETCH FIRST 100 ROWS ONLY;
   ```

2. **不查敏感字段**: 不查询密码、Token、密钥等字段
   ```sql
   -- 查用户表时排除密码
   SELECT USER_ID, USER_NAME, STATUS FROM SYS_USER WHERE ...;
   ```

3. **使用绑定变量格式**: SQL 中的变量用 `&` 前缀
   ```sql
   SELECT * FROM T_RMBS_CLAIM WHERE CLAIM_NO = '&claim_no';
   ```

4. **多表查询加 schema**: 明确表归属
   ```sql
   SELECT * FROM YLADMIN.T_RMBS_CLAIM WHERE ...;
   ```

5. **大表加索引提示**: 查大表时使用索引字段作为条件
   ```sql
   -- T_RMBS_CLAIM 的索引: CLAIM_NO, TEMPLATE_ID, CREATOR, CREATE_TIME
   SELECT * FROM T_RMBS_CLAIM WHERE CLAIM_NO = 'xxx';  -- 走索引
   ```

---

## 安全约束

1. **默认只读**: 只执行 SELECT 语句，DML/DDL 需要用户显式确认
2. **结果行数限制**: 默认最多返回 100 行，防止大结果集
3. **不查敏感数据**: 不查询密码、Token、密钥等字段
4. **连接信息保密**: 密码放 yaml 配置文件，不写入 SKILL.md 或日志
5. **结果自动保存**: 每次查询自动 SPOOL 保存带时间戳
6. **不在生产环境执行**: 只支持 local 和 sit 环境
7. **查询超时**: 单次查询超时 60 秒，防止长查询占用连接
8. **写操作二次确认**: INSERT/UPDATE/DELETE 必须展示 SQL 并等用户确认

## 参考

- Oracle 连接参考: `ai-spec/skills/db/oracle-dba/scripts/run_resource_hog.sh`
- 资源诊断脚本: `ai-spec/skills/db/oracle-dba/scripts/resource_hog_sql.sql`
- 连接配置模板: `config/db-connection.yaml.example`
- 通用查询脚本: `scripts/run_query.sh`
- 常用查询模板: `scripts/common_queries.sql`
- 业务表映射: `references/table-mapping.md`
- Pipeline 编排: `ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/SKILL.md`
- SIT 验证分析: `ai-spec/skills/code/bug-fix-cycle/sit-verify-analyze/SKILL.md`
