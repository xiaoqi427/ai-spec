# 案例分析：全表扫描优化

## 案例背景

**问题描述**:
某电商系统订单查询功能响应缓慢，用户投诉查询订单需要15-20秒。

**业务场景**:
- 功能：根据订单号查询订单详情
- 表：ORDERS表，约500万条记录
- 查询频率：每秒约100次（高峰期）

## 问题发现

### 1. 用户报告慢查询

业务人员反馈：订单查询功能很慢，客户体验差。

### 2. 定位问题SQL

通过应用日志和数据库监控，定位到慢SQL：

```sql
SELECT * FROM ORDERS 
WHERE ORDER_NO = '202502280001';
```

执行时间：**约18秒**

## 诊断过程

### 步骤1：检查当前会话等待

```sql
SELECT sid, event, seconds_in_wait
FROM v$session_wait
WHERE sid = (SELECT sid FROM v$mystat WHERE ROWNUM = 1);
```

**结果**:
```
SID    EVENT                         SECONDS_IN_WAIT
-----  --------------------------    ---------------
156    db file scattered read        12
```

**分析**: `db file scattered read` 表示多块读，通常是**全表扫描**！

### 步骤2：查看执行计划

```sql
-- 先执行SQL并获取SQL_ID
SELECT sql_id 
FROM v$sql 
WHERE sql_text LIKE '%202502280001%'
  AND sql_text NOT LIKE '%v$sql%';

-- 查看执行计划
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id'));
```

**执行计划**:
```
Plan hash value: 1234567890

---------------------------------------------------------------------------
| Id  | Operation         | Name   | Rows  | Bytes | Cost (%CPU)| Time     |
---------------------------------------------------------------------------
|   0 | SELECT STATEMENT  |        |       |       |  5678 (100)|          |
|*  1 |  TABLE ACCESS FULL| ORDERS |     1 | 2000  |  5678   (1)| 00:01:08 |
---------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------
   1 - filter("ORDER_NO"='202502280001')
```

**问题确认**: 
- ❌ **TABLE ACCESS FULL** - 全表扫描！
- ❌ Cost = 5678，预计时间68秒
- ❌ 扫描整个表（500万行）只为找1行数据

### 步骤3：检查是否有索引

```sql
SELECT index_name, column_name, column_position
FROM dba_ind_columns
WHERE table_owner = 'ORDERDB'
  AND table_name = 'ORDERS'
  AND column_name = 'ORDER_NO';
```

**结果**: 
```
no rows selected
```

**结论**: **ORDER_NO列上没有索引！**

### 步骤4：检查统计信息

```sql
SELECT table_name, num_rows, last_analyzed
FROM dba_tables
WHERE owner = 'ORDERDB'
  AND table_name = 'ORDERS';
```

**结果**:
```
TABLE_NAME   NUM_ROWS    LAST_ANALYZED
-----------  ----------  -------------
ORDERS       5,234,891   2025-02-15
```

统计信息是最新的，不是统计信息问题。

### 步骤5：分析SQL性能指标

```sql
SELECT 
    sql_id,
    executions,
    buffer_gets,
    disk_reads,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    ROUND(buffer_gets/executions) gets_per_exec,
    rows_processed
FROM v$sql
WHERE sql_id = '&sql_id';
```

**结果**:
```
SQL_ID         EXECS  BUFFER_GETS  DISK_READS  ELAPSED_SEC  GETS_PER_EXEC  ROWS
-------------  -----  -----------  ----------  -----------  -------------  ----
9babjv8yq8ru3  1,234  678,901,234  123,456     22,345.67    550,162        1,234
```

**分析**:
- 每次执行550,162次逻辑读（buffer gets）！
- 这个值太高了，正常应该是个位数到几百
- 物理读也很高，说明数据无法缓存

## 根本原因

**ORDER_NO列上缺少索引，导致每次查询都要全表扫描**

## 优化方案

### 方案1：创建索引（推荐）

```sql
-- 创建索引
CREATE INDEX IDX_ORDERS_ORDER_NO 
ON ORDERS(ORDER_NO)
TABLESPACE USERS_IDX
PCTFREE 10
STORAGE (INITIAL 10M NEXT 10M);

-- 收集索引统计信息
EXEC DBMS_STATS.GATHER_INDEX_STATS('ORDERDB', 'IDX_ORDERS_ORDER_NO');
```

**为什么这样设计**:
- ORDER_NO是唯一标识，选择性极高
- 查询条件是等值查询（=），B树索引最佳
- 分配到单独的表空间，便于管理

### 方案2：创建唯一索引（更优）

```sql
-- 如果ORDER_NO确保唯一，创建唯一索引
CREATE UNIQUE INDEX UK_ORDERS_ORDER_NO 
ON ORDERS(ORDER_NO)
TABLESPACE USERS_IDX;
```

**优势**:
- 唯一性约束保证数据质量
- Oracle知道最多返回1行，执行计划更优
- 索引更紧凑

## 验证效果

### 1. 重新查看执行计划

```sql
-- 刷新SQL（让它使用新索引）
ALTER SYSTEM FLUSH SHARED_POOL;

-- 再次执行并查看计划
EXPLAIN PLAN FOR
SELECT * FROM ORDERS WHERE ORDER_NO = '202502280001';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

**优化后的执行计划**:
```
Plan hash value: 9876543210

-------------------------------------------------------------------------------------------
| Id  | Operation                   | Name                | Rows  | Bytes | Cost (%CPU)|
-------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT            |                     |     1 |  2000 |     3   (0)|
|   1 |  TABLE ACCESS BY INDEX ROWID| ORDERS              |     1 |  2000 |     3   (0)|
|*  2 |   INDEX UNIQUE SCAN         | UK_ORDERS_ORDER_NO  |     1 |       |     2   (0)|
-------------------------------------------------------------------------------------------

Predicate Information:
---------------------------------------------------
   2 - access("ORDER_NO"='202502280001')
```

**对比**:
| 指标 | 优化前 | 优化后 | 改善 |
|-----|-------|-------|------|
| Operation | TABLE ACCESS FULL | INDEX UNIQUE SCAN | ✅ |
| Cost | 5678 | 3 | ↓ 99.9% |
| Estimated Time | 68秒 | <1秒 | ↓ 99%+ |

### 2. 实际执行对比

```sql
-- 开启时间统计
SET TIMING ON

-- 优化前（全表扫描）
-- 18.23秒

-- 优化后（索引扫描）
SELECT * FROM ORDERS WHERE ORDER_NO = '202502280001';
-- 0.02秒
```

**性能提升**: **900倍+**！

### 3. 验证逻辑读

```sql
SET AUTOTRACE ON

SELECT * FROM ORDERS WHERE ORDER_NO = '202502280001';
```

**优化后统计**:
```
Statistics
----------------------------------------------------------
  0  recursive calls
  0  db block gets
  4  consistent gets  ← 原来是550,162！
  0  physical reads
```

**逻辑读从550,162降到4**，减少了99.999%！

## 持续监控

### 1. 创建监控脚本

```sql
-- 监控该SQL的性能
SELECT 
    TO_CHAR(sample_time, 'YYYY-MM-DD HH24:MI') time,
    AVG(CASE WHEN event = 'db file scattered read' THEN 1 ELSE 0 END) full_scan_pct,
    COUNT(*) total_samples
FROM dba_hist_active_sess_history
WHERE sql_id = '9babjv8yq8ru3'
  AND sample_time > SYSDATE - 7
GROUP BY TRUNC(sample_time, 'MI')
ORDER BY time DESC;
```

### 2. 设置告警

如果该SQL再次出现全表扫描，说明索引可能失效：
- 索引被删除？
- 统计信息陈旧？
- 隐式类型转换？

## 经验总结

### 全表扫描典型特征

1. **等待事件**: `db file scattered read`
2. **执行计划**: `TABLE ACCESS FULL`
3. **逻辑读极高**: 接近表的总块数
4. **Cost很高**: 通常是索引扫描的几百倍

### 优化决策流程

```
发现慢查询
    ↓
查看执行计划
    ↓
是否全表扫描？
    ├─ 是 → 检查索引
    │   ├─ 无索引 → 创建索引 ✅
    │   ├─ 索引失效 → 分析原因（类型转换/函数/统计信息）
    │   └─ 索引存在但不用 → 检查查询条件
    │
    └─ 否 → 进一步分析执行计划
```

### 何时全表扫描是合理的？

**不是所有全表扫描都需要优化**，以下情况全表扫描可能更优：

1. **小表** (< 1000行)
   - 索引扫描 + 回表可能比全表扫描慢
   
2. **返回大量数据** (> 表的5%)
   - 索引扫描需要大量回表，不如全表扫描
   
3. **并行查询**
   - 大表统计分析，全表扫描+并行更快
   
4. **表完全缓存在内存中**
   - 全表扫描的I/O代价很小

### 索引设计原则

1. **高选择性列优先**
   - ORDER_NO（唯一值）> STATUS（几个状态值）
   
2. **WHERE条件常用列**
   - 频繁查询的列优先索引
   
3. **组合索引顺序**
   - 等值条件在前，范围条件在后
   
4. **避免过度索引**
   - 每个索引都有维护成本（INSERT/UPDATE/DELETE变慢）
   - 监控索引使用情况，删除未使用的索引

### 常见陷阱

**陷阱1: 索引列上使用函数**
```sql
-- ❌ 索引失效
SELECT * FROM ORDERS WHERE UPPER(ORDER_NO) = 'ABC123';

-- ✅ 正确
SELECT * FROM ORDERS WHERE ORDER_NO = 'ABC123';
```

**陷阱2: 隐式类型转换**
```sql
-- ORDER_NO是VARCHAR2类型
-- ❌ 索引失效（数字转字符串）
SELECT * FROM ORDERS WHERE ORDER_NO = 202502280001;

-- ✅ 正确（使用字符串）
SELECT * FROM ORDERS WHERE ORDER_NO = '202502280001';
```

**陷阱3: NULL值处理**
```sql
-- B树索引不包含全NULL的行
-- ❌ 可能不走索引
SELECT * FROM ORDERS WHERE ORDER_NO IS NULL;

-- ✅ 使用函数索引或位图索引
CREATE INDEX idx_orders_no_null ON ORDERS(
  CASE WHEN ORDER_NO IS NULL THEN 1 ELSE 0 END
);
```

## 延伸阅读

- [执行计划解读](explain_plan.md)
- [索引失效的12种场景](../references/index_issues.md)
- [如何选择索引类型](../references/index_types.md)
