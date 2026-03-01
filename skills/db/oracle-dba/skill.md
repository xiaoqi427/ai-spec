---
name: oracle-dba
description: Oracle高级DBA工具集，提供性能诊断、SQL优化、健康检查、备份恢复等专业能力。当用户需要分析AWR报告、优化SQL、检查数据库健康状态、诊断性能问题、管理表空间、分析执行计划或进行数据库故障排查时使用。
---

# Oracle高级DBA工具集

## 概述

此skill为Oracle数据库管理员提供专业的诊断、优化和管理工具，涵盖性能分析、SQL调优、健康检查、备份恢复等核心DBA工作场景。

## 适用场景

- 🔍 **性能诊断**: AWR报告分析、等待事件分析、性能瓶颈定位
- 🚀 **SQL优化**: 执行计划分析、索引建议、SQL改写
- ✅ **健康检查**: 表空间使用率、会话监控、锁/死锁检测
- 💾 **备份恢复**: RMAN备份策略、恢复方案、闪回技术
- 📊 **容量规划**: 增长趋势分析、空间管理、归档策略

## 核心功能

### 1. 性能诊断与优化

#### AWR报告分析
```sql
-- 生成AWR报告（最近1小时）
@?/rdbms/admin/awrrpt.sql

-- 快速查看最近的AWR快照
SELECT snap_id, begin_interval_time, end_interval_time
FROM dba_hist_snapshot
ORDER BY snap_id DESC
FETCH FIRST 10 ROWS ONLY;

-- 分析Top SQL（按CPU时间）
SELECT sql_id, 
       executions_delta,
       cpu_time_delta/1000000 cpu_sec,
       elapsed_time_delta/1000000 elapsed_sec,
       buffer_gets_delta,
       disk_reads_delta
FROM dba_hist_sqlstat
WHERE snap_id BETWEEN &begin_snap AND &end_snap
ORDER BY cpu_time_delta DESC
FETCH FIRST 20 ROWS ONLY;
```

#### 等待事件分析
```sql
-- 查看当前TOP等待事件
SELECT event,
       total_waits,
       total_timeouts,
       time_waited,
       average_wait
FROM v$system_event
WHERE event NOT LIKE 'SQL*Net%'
  AND event NOT LIKE '%timer%'
  AND event NOT LIKE '%idle%'
ORDER BY time_waited DESC
FETCH FIRST 10 ROWS ONLY;

-- 查看会话等待
SELECT s.sid,
       s.serial#,
       s.username,
       s.program,
       w.event,
       w.wait_time,
       w.seconds_in_wait,
       w.state
FROM v$session s
JOIN v$session_wait w ON s.sid = w.sid
WHERE s.username IS NOT NULL
  AND w.event NOT LIKE '%timer%'
ORDER BY w.seconds_in_wait DESC;
```

### 2. SQL分析与优化

#### 执行计划分析
```sql
-- 查看SQL的执行计划（从游标缓存）
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id', NULL, 'ALLSTATS LAST'));

-- 查看历史执行计划（从AWR）
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_AWR('&sql_id'));

-- 分析执行计划关键指标
SELECT sql_id,
       child_number,
       executions,
       rows_processed,
       buffer_gets,
       disk_reads,
       cpu_time/1000000 cpu_sec,
       elapsed_time/1000000 elapsed_sec,
       ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
       ROUND(rows_processed/NULLIF(executions,0)) rows_per_exec
FROM v$sql
WHERE sql_id = '&sql_id';
```

#### SQL调优建议
```sql
-- 使用SQL Tuning Advisor
DECLARE
  l_task_name VARCHAR2(30);
BEGIN
  l_task_name := DBMS_SQLTUNE.CREATE_TUNING_TASK(
    sql_id => '&sql_id',
    task_name => 'tune_sql_&sql_id',
    time_limit => 300
  );
  
  DBMS_SQLTUNE.EXECUTE_TUNING_TASK(task_name => l_task_name);
  
  -- 查看建议
  DBMS_OUTPUT.PUT_LINE(
    DBMS_SQLTUNE.REPORT_TUNING_TASK(task_name => l_task_name)
  );
END;
/
```

#### 索引建议
```sql
-- 查找缺失索引的表（高逻辑读）
SELECT owner, table_name, num_rows,
       blocks, avg_row_len
FROM dba_tables
WHERE owner = '&schema'
  AND num_rows > 10000
  AND NOT EXISTS (
    SELECT 1 FROM dba_indexes i
    WHERE i.owner = dba_tables.owner
      AND i.table_name = dba_tables.table_name
  )
ORDER BY blocks DESC;

-- 查找未使用的索引
SELECT owner, index_name, table_name,
       last_used, num_rows
FROM dba_index_usage
WHERE owner = '&schema'
  AND total_access_count = 0
  AND last_used < SYSDATE - 30;
```

### 3. 数据库健康检查

#### 表空间监控
```sql
-- 表空间使用率
SELECT tablespace_name,
       ROUND(used_space_mb, 2) used_mb,
       ROUND(tablespace_size_mb, 2) total_mb,
       ROUND(used_percent, 2) used_pct,
       ROUND(tablespace_size_mb - used_space_mb, 2) free_mb
FROM (
  SELECT tablespace_name,
         SUM(bytes)/1024/1024 used_space_mb,
         MAX(maxbytes)/1024/1024 tablespace_size_mb,
         SUM(bytes)/MAX(maxbytes)*100 used_percent
  FROM dba_data_files
  GROUP BY tablespace_name
)
ORDER BY used_percent DESC;

-- 表空间增长趋势（需要AWR）
SELECT tablespace_name,
       TRUNC(rtime) stat_date,
       MAX(tablespace_size)/1024/1024 size_mb
FROM dba_hist_tbspc_space_usage
WHERE tablespace_name = '&tablespace_name'
  AND rtime > SYSDATE - 30
GROUP BY tablespace_name, TRUNC(rtime)
ORDER BY stat_date;
```

#### 会话监控
```sql
-- 当前活动会话
SELECT s.sid,
       s.serial#,
       s.username,
       s.status,
       s.program,
       s.machine,
       s.logon_time,
       s.last_call_et seconds_since_last_call,
       sq.sql_text current_sql
FROM v$session s
LEFT JOIN v$sql sq ON s.sql_id = sq.sql_id
WHERE s.username IS NOT NULL
  AND s.status = 'ACTIVE'
ORDER BY s.last_call_et DESC;

-- 长时间运行的SQL
SELECT s.sid,
       s.serial#,
       s.username,
       s.sql_id,
       s.sql_exec_start,
       ROUND((SYSDATE - s.sql_exec_start) * 24 * 60, 2) runtime_min,
       sq.sql_text
FROM v$session s
JOIN v$sql sq ON s.sql_id = sq.sql_id
WHERE s.sql_exec_start IS NOT NULL
  AND (SYSDATE - s.sql_exec_start) * 24 * 60 > 5
ORDER BY runtime_min DESC;
```

#### 锁和死锁检测
```sql
-- 当前锁等待
SELECT l1.sid waiting_sid,
       s1.username waiting_user,
       l2.sid holding_sid,
       s2.username holding_user,
       o.object_name,
       o.object_type,
       l1.type lock_type,
       l1.lmode lock_mode,
       l1.request
FROM v$lock l1
JOIN v$session s1 ON l1.sid = s1.sid
JOIN v$lock l2 ON l1.id1 = l2.id1 AND l1.id2 = l2.id2
JOIN v$session s2 ON l2.sid = s2.sid
JOIN dba_objects o ON l1.id1 = o.object_id
WHERE l1.block = 1
  AND l2.request > 0;

-- 死锁历史（从alert log或trace文件）
SELECT * FROM v$diag_alert_ext
WHERE message_text LIKE '%deadlock%'
  AND originating_timestamp > SYSDATE - 7
ORDER BY originating_timestamp DESC;
```

### 4. 备份恢复管理

#### RMAN备份状态检查
```sql
-- 最近备份情况
SELECT session_key,
       input_type,
       status,
       TO_CHAR(start_time, 'YYYY-MM-DD HH24:MI:SS') start_time,
       TO_CHAR(end_time, 'YYYY-MM-DD HH24:MI:SS') end_time,
       ROUND(elapsed_seconds/60, 2) elapsed_min,
       ROUND(input_bytes/1024/1024/1024, 2) input_gb,
       ROUND(output_bytes/1024/1024/1024, 2) output_gb
FROM v$rman_backup_job_details
WHERE start_time > SYSDATE - 7
ORDER BY start_time DESC;

-- 备份集信息
SELECT bs.recid,
       bs.set_stamp,
       bs.set_count,
       TO_CHAR(bs.completion_time, 'YYYY-MM-DD HH24:MI:SS') backup_time,
       bp.handle backup_piece,
       ROUND(bp.bytes/1024/1024/1024, 2) size_gb,
       bs.backup_type,
       bs.incremental_level
FROM v$backup_set bs
JOIN v$backup_piece bp ON bs.set_stamp = bp.set_stamp
WHERE bs.completion_time > SYSDATE - 30
ORDER BY bs.completion_time DESC;
```

#### 归档日志检查
```sql
-- 归档日志生成速率
SELECT TRUNC(first_time) log_date,
       COUNT(*) archives_generated,
       ROUND(SUM(blocks * block_size)/1024/1024/1024, 2) total_gb,
       ROUND(AVG(blocks * block_size)/1024/1024, 2) avg_mb
FROM v$archived_log
WHERE first_time > SYSDATE - 7
  AND dest_id = 1
GROUP BY TRUNC(first_time)
ORDER BY log_date DESC;

-- 归档目标空间
SELECT dest_name,
       destination,
       status,
       ROUND(space_limit/1024/1024/1024, 2) limit_gb,
       ROUND(space_used/1024/1024/1024, 2) used_gb,
       ROUND(space_used/space_limit*100, 2) used_pct
FROM v$recovery_file_dest;
```

### 5. 统计信息管理

#### 统计信息收集
```sql
-- 检查陈旧统计信息
SELECT owner, table_name, num_rows,
       last_analyzed,
       TRUNC(SYSDATE - last_analyzed) days_old,
       stattype_locked
FROM dba_tab_statistics
WHERE owner = '&schema'
  AND (last_analyzed IS NULL OR last_analyzed < SYSDATE - 7)
  AND num_rows > 1000
ORDER BY days_old DESC NULLS FIRST;

-- 收集统计信息
BEGIN
  DBMS_STATS.GATHER_SCHEMA_STATS(
    ownname => '&schema',
    estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
    method_opt => 'FOR ALL COLUMNS SIZE AUTO',
    degree => 4,
    cascade => TRUE,
    no_invalidate => FALSE
  );
END;
/

-- 检查直方图统计
SELECT owner, table_name, column_name,
       num_distinct, num_buckets, histogram
FROM dba_tab_col_statistics
WHERE owner = '&schema'
  AND histogram != 'NONE'
ORDER BY num_buckets DESC;
```

## 工作流程

### 性能问题诊断流程

```
1. 【发现问题】
   - 用户报告慢查询或系统变慢
   
2. 【快速诊断】
   ├─ 检查当前活动会话（见"会话监控"）
   ├─ 查看TOP等待事件（见"等待事件分析"）
   └─ 识别问题SQL（按CPU/等待时间排序）
   
3. 【深入分析】
   ├─ 分析执行计划（DISPLAY_CURSOR）
   ├─ 检查统计信息是否陈旧
   ├─ 查看历史性能（AWR）
   └─ 分析索引使用情况
   
4. 【优化建议】
   ├─ SQL改写建议（SQL Tuning Advisor）
   ├─ 索引创建/删除建议
   ├─ 统计信息收集
   └─ 系统参数调整（如需要）
   
5. 【验证效果】
   └─ 对比优化前后性能指标
```

### 日常健康检查清单

```markdown
## 每日检查

- [ ] 表空间使用率（>80%告警）
- [ ] 归档日志生成速率
- [ ] 备份状态（过去24小时）
- [ ] Alert Log错误
- [ ] 长时间运行SQL（>30分钟）
- [ ] 锁等待情况

## 每周检查

- [ ] AWR报告分析
- [ ] TOP SQL性能趋势
- [ ] 陈旧统计信息
- [ ] 未使用索引
- [ ] 表增长趋势
- [ ] 会话连接池使用率

## 每月检查

- [ ] 容量规划（表空间/归档）
- [ ] 备份策略评估
- [ ] 索引碎片整理需求
- [ ] 分区表维护
- [ ] 性能基线对比
```

## 脚本工具

### 使用方式

所有脚本位于 `scripts/` 目录下，可直接在SQL*Plus或SQLcl中执行：

```bash
# SQL*Plus
sqlplus user/pass@db @scripts/health_check.sql

# SQLcl
sql user/pass@db @scripts/health_check.sql

# Python工具
python scripts/awr_analyzer.py --db prod --hours 2
```

### 可用脚本清单

| 脚本名称 | 功能说明 | 使用场景 |
|---------|---------|---------|
| `health_check.sql` | 综合健康检查 | 日常巡检 |
| `top_sql.sql` | TOP SQL分析 | 性能诊断 |
| `wait_events.sql` | 等待事件分析 | 性能诊断 |
| `tablespace_report.sql` | 表空间报告 | 容量规划 |
| `session_monitor.sql` | 会话监控 | 问题排查 |
| `lock_tree.sql` | 锁等待树 | 锁问题排查 |
| `awr_analyzer.py` | AWR报告解析（Python） | 自动化分析 |
| `sql_tuning.sql` | SQL调优助手 | SQL优化 |

## 最佳实践

### SQL优化原则

1. **执行计划优先**: 永远先看执行计划再动手优化
2. **统计信息为王**: 确保统计信息准确且及时
3. **索引有的放矢**: 根据访问模式创建索引，避免过度索引
4. **关注谓词**: WHERE条件的选择性是关键
5. **避免隐式转换**: 数据类型不匹配会导致索引失效

### 性能分析技巧

```sql
-- 技巧1：使用GATHER_PLAN_STATISTICS提示获取实际执行统计
SELECT /*+ GATHER_PLAN_STATISTICS */ * 
FROM large_table 
WHERE ...;

-- 查看实际行数 vs 估计行数
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));

-- 技巧2：使用MONITOR提示跟踪长SQL
SELECT /*+ MONITOR */ * 
FROM huge_table t1
JOIN another_table t2 ON ...;

-- 查看实时执行进度
SELECT sql_id, status, 
       ROUND(elapsed_time/1000000, 2) elapsed_sec,
       ROUND(cpu_time/1000000, 2) cpu_sec
FROM v$sql_monitor
WHERE sql_id = '&sql_id';

-- 技巧3：使用SQL Trace深度分析
ALTER SESSION SET EVENTS '10046 trace name context forever, level 12';
-- 执行SQL
ALTER SESSION SET EVENTS '10046 trace name context off';
-- 使用tkprof分析trace文件
```

### 索引设计原则

1. **高选择性列优先**: WHERE条件中选择性高的列
2. **组合索引顺序**: 等值条件列在前，范围条件列在后
3. **覆盖索引**: 包含SELECT列避免回表
4. **避免函数索引滥用**: 优先考虑SQL改写
5. **定期维护**: 重建碎片化索引

### 表空间管理

```sql
-- 自动扩展配置建议
ALTER DATABASE DATAFILE '/path/to/datafile.dbf'
  AUTOEXTEND ON 
  NEXT 1G 
  MAXSIZE 32G;

-- 监控自动扩展次数（频繁扩展说明需要手动扩容）
SELECT tablespace_name, file_name,
       autoextensible,
       increment_by * (SELECT value FROM v$parameter WHERE name='db_block_size') / 1024 / 1024 increment_mb,
       maxbytes / 1024 / 1024 / 1024 max_gb
FROM dba_data_files
WHERE autoextensible = 'YES';
```

## 故障排查指南

### 慢查询排查

```
症状: SQL执行缓慢

步骤:
1. 获取SQL_ID和执行计划
   → SELECT sql_id FROM v$session WHERE sid = &sid;
   
2. 检查执行计划是否合理
   → SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id'));
   
3. 对比历史执行计划（是否发生变化）
   → SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_AWR('&sql_id'));
   
4. 检查统计信息
   → 见"统计信息管理"部分
   
5. 查看等待事件
   → SELECT event, seconds_in_wait FROM v$session_wait WHERE sid = &sid;
   
常见原因:
- ❌ 全表扫描（缺索引）
- ❌ 索引失效（隐式转换）
- ❌ 统计信息陈旧
- ❌ 执行计划改变（绑定变量窥探）
- ❌ 资源争用（锁等待、I/O瓶颈）
```

### 锁等待问题

```
症状: 事务挂起、超时

步骤:
1. 查找锁等待链
   → 使用 scripts/lock_tree.sql
   
2. 识别阻塞会话
   → SELECT blocking_session FROM v$session WHERE blocking_session IS NOT NULL;
   
3. 分析持锁时间
   → 见"锁和死锁检测"部分
   
4. 确定是否需要强制终止
   → ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;
   
预防措施:
- ✅ 缩短事务时间
- ✅ 避免长时间持锁
- ✅ 合理设置锁超时
- ✅ 使用行级锁而非表锁
```

### 表空间满

```
症状: ORA-01653 unable to extend table

步骤:
1. 确认哪个表空间满了
   → 见"表空间监控"
   
2. 检查是否有可回收空间
   → SELECT * FROM dba_free_space WHERE tablespace_name = '&ts';
   
3. 临时解决（扩容）
   → ALTER DATABASE DATAFILE '...' RESIZE 20G;
   或
   → ALTER TABLESPACE ... ADD DATAFILE '...' SIZE 10G;
   
4. 长期方案
   - 清理历史数据（归档/删除）
   - 分区表（按时间分区）
   - 压缩（COMPRESS FOR OLTP）
```

## 附加资源

### 参考文档

详细的SQL语句、参数说明和高级用法请参考：

- [AWR报告解读指南](references/awr_guide.md) - AWR各项指标含义
- [等待事件详解](references/wait_events.md) - 常见等待事件及优化建议
- [执行计划解读](references/explain_plan.md) - 执行计划关键操作和Cost含义
- [RMAN完整手册](references/rman_guide.md) - 备份恢复完整方案

### 示例场景

实际问题案例和解决方案：

- [案例1：全表扫描优化](examples/case_full_scan.md)
- [案例2：索引选择性问题](examples/case_index_selectivity.md)
- [案例3：SQL执行计划突变](examples/case_plan_change.md)
- [案例4：表空间快速增长](examples/case_tablespace_growth.md)

## 常见问题 FAQ

**Q: 如何判断SQL是否需要优化？**

A: 关注以下指标：
- 执行时间 > 1秒
- 逻辑读 > 100,000（buffer gets）
- 物理读/逻辑读比例 > 10%
- CPU时间占比 < 50%（说明等待多）

**Q: 统计信息多久收集一次？**

A: 
- 频繁变化的表：每天
- 一般表：每周
- 静态表：每月或数据量变化>10%时
- 使用AUTO任务：Oracle会自动判断

**Q: 什么时候需要重建索引？**

A: 
- 碎片率 > 30%（查询 INDEX_STATS）
- 删除数据超过20%
- 性能明显下降且统计信息准确
- 注意：大多数情况下REBUILD无必要，COALESCE足够

**Q: AWR快照保留多久？**

A: 
- 默认：8天
- 建议：至少保留30天用于趋势分析
- 修改：`DBMS_WORKLOAD_REPOSITORY.MODIFY_SNAPSHOT_SETTINGS`

## 注意事项

⚠️ **安全警告**

1. **生产环境操作需谨慎**
   - 所有修改操作（KILL SESSION、ALTER SYSTEM等）需要评估影响
   - 建议先在测试环境验证
   
2. **权限要求**
   - 大部分查询需要SELECT_CATALOG_ROLE
   - AWR/ADDM需要DIAGNOSTIC+TUNING pack license
   - RMAN操作需要SYSDBA权限
   
3. **性能影响**
   - 避免高峰期收集统计信息
   - AWR报告生成会占用CPU
   - 深度trace会显著影响性能

4. **数据隐私**
   - SQL文本可能包含敏感数据
   - 导出AWR报告前脱敏处理

## 更新日志

- 2025-02-28: 初始版本创建
  - 性能诊断模块
  - SQL优化模块
  - 健康检查模块
  - 备份恢复模块

---

## 使用此Skill

当用户提出以下需求时，自动应用此skill：

- "帮我分析这个慢SQL"
- "检查数据库健康状态"
- "表空间快满了怎么办"
- "为什么这个查询这么慢"
- "分析AWR报告"
- "这个执行计划合理吗"
- "数据库有锁等待"
- "RMAN备份失败了"

AI应该：
1. 识别用户问题类型（性能/锁/空间等）
2. 提供相应的诊断SQL
3. 解读查询结果
4. 给出优化建议和具体步骤
5. 如需执行脚本，使用 `scripts/` 目录下的工具
