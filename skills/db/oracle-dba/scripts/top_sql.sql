-- ============================================================================
-- TOP SQL分析脚本
-- 功能: 分析当前系统中性能影响最大的SQL
-- 使用: sqlplus user/pass@db @top_sql.sql
-- 作者: sevenxiao
-- 日期: 2025-02-28
-- ============================================================================

SET LINESIZE 250
SET PAGESIZE 1000
SET FEEDBACK OFF
SET VERIFY OFF
SET LONG 10000

PROMPT ============================================================================
PROMPT                           TOP SQL分析报告
PROMPT ============================================================================
PROMPT 

-- 按CPU时间排序的TOP SQL
PROMPT >>> 1. TOP SQL - 按CPU时间排序
PROMPT 
COL sql_id FORMAT A15
COL executions FORMAT 999,999,999
COL cpu_sec FORMAT 999,999.99
COL elapsed_sec FORMAT 999,999.99
COL buffer_gets FORMAT 999,999,999
COL disk_reads FORMAT 999,999,999
COL rows_proc FORMAT 999,999,999

SELECT 
    sql_id,
    executions,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    buffer_gets,
    disk_reads,
    rows_processed rows_proc,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    ROUND(rows_processed/NULLIF(executions,0)) rows_per_exec
FROM v$sql
WHERE executions > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
ORDER BY cpu_time DESC
FETCH FIRST 20 ROWS ONLY;

-- 按逻辑读排序的TOP SQL
PROMPT 
PROMPT >>> 2. TOP SQL - 按逻辑读（Buffer Gets）排序
PROMPT 
SELECT 
    sql_id,
    executions,
    buffer_gets,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    disk_reads,
    rows_processed rows_proc
FROM v$sql
WHERE executions > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
ORDER BY buffer_gets DESC
FETCH FIRST 20 ROWS ONLY;

-- 按物理读排序的TOP SQL
PROMPT 
PROMPT >>> 3. TOP SQL - 按物理读（Disk Reads）排序
PROMPT 
SELECT 
    sql_id,
    executions,
    disk_reads,
    ROUND(disk_reads/NULLIF(executions,0)) reads_per_exec,
    buffer_gets,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    rows_processed rows_proc
FROM v$sql
WHERE executions > 0
  AND disk_reads > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
ORDER BY disk_reads DESC
FETCH FIRST 20 ROWS ONLY;

-- 按执行次数排序的TOP SQL
PROMPT 
PROMPT >>> 4. TOP SQL - 按执行次数排序（高频SQL）
PROMPT 
SELECT 
    sql_id,
    executions,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    buffer_gets,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    ROUND(elapsed_time/NULLIF(executions,0)/1000, 2) ms_per_exec
FROM v$sql
WHERE executions > 100
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
ORDER BY executions DESC
FETCH FIRST 20 ROWS ONLY;

-- 低效SQL（逻辑读高但返回行少）
PROMPT 
PROMPT >>> 5. 低效SQL - 逻辑读高但返回行少（可能全表扫描）
PROMPT 
SELECT 
    sql_id,
    executions,
    buffer_gets,
    rows_processed rows_proc,
    ROUND(buffer_gets/NULLIF(rows_processed,0)) gets_per_row,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    ROUND(cpu_time/1000000, 2) cpu_sec
FROM v$sql
WHERE executions > 0
  AND rows_processed > 0
  AND buffer_gets/rows_processed > 1000  -- 每行超过1000次逻辑读
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
ORDER BY buffer_gets/rows_processed DESC
FETCH FIRST 20 ROWS ONLY;

-- 解析次数多的SQL（硬解析问题）
PROMPT 
PROMPT >>> 6. 硬解析问题 - 解析次数多的SQL
PROMPT 
SELECT 
    sql_id,
    version_count,
    executions,
    parse_calls,
    ROUND(parse_calls/NULLIF(executions,0)*100, 2) parse_pct,
    ROUND(cpu_time/1000000, 2) cpu_sec
FROM v$sql
WHERE executions > 0
  AND parse_calls > executions * 0.8  -- 解析次数超过执行次数80%
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
ORDER BY parse_calls DESC
FETCH FIRST 20 ROWS ONLY;

-- 显示指定SQL的详细信息
PROMPT 
PROMPT >>> 如需查看某个SQL的完整文本和执行计划，请输入SQL_ID:
ACCEPT sql_id_input PROMPT 'SQL_ID (直接回车跳过): '

SET TERMOUT OFF
COLUMN has_input NEW_VALUE run_detail
SELECT CASE WHEN '&sql_id_input' IS NULL OR '&sql_id_input' = '' 
            THEN 'NO' ELSE 'YES' END has_input 
FROM dual;
SET TERMOUT ON

PROMPT 
SET TERMOUT &run_detail

PROMPT >>> SQL完整文本:
PROMPT 
SELECT sql_fulltext
FROM v$sql
WHERE sql_id = '&sql_id_input'
  AND ROWNUM = 1;

PROMPT 
PROMPT >>> SQL执行计划:
PROMPT 
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id_input', NULL, 'ALLSTATS LAST'));

PROMPT 
PROMPT >>> SQL执行统计:
PROMPT 
SELECT 
    sql_id,
    child_number,
    plan_hash_value,
    executions,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    buffer_gets,
    disk_reads,
    rows_processed,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    ROUND(rows_processed/NULLIF(executions,0)) rows_per_exec,
    parse_calls,
    loads,
    invalidations
FROM v$sql
WHERE sql_id = '&sql_id_input';

SET TERMOUT ON

PROMPT 
PROMPT ============================================================================
PROMPT                        TOP SQL分析完成
PROMPT 
PROMPT 优化建议:
PROMPT 1. CPU高的SQL: 检查执行计划，考虑索引优化
PROMPT 2. 逻辑读高的SQL: 可能全表扫描，需要添加索引
PROMPT 3. 物理读高的SQL: 考虑增加buffer cache或优化I/O
PROMPT 4. 高频SQL: 即使单次快，累计影响大，优先优化
PROMPT 5. 硬解析多的SQL: 使用绑定变量
PROMPT ============================================================================
PROMPT 

SET FEEDBACK ON
SET VERIFY ON
UNDEFINE sql_id_input
