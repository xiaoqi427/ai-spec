-- ============================================================================
-- 资源消耗SQL定位脚本
-- 功能: 多维度定位当前系统中资源消耗最大的SQL和会话
-- 使用: sql user/pass@db @resource_hog_sql.sql
-- 输出: 结果自动保存到 output/resource_hog_sql_YYYYMMDD_HH24MISS.txt
-- 作者: sevenxiao
-- 日期: 2026-03-10
-- ============================================================================
-- 维度覆盖:
--   1. 活跃会话资源消耗全景（CPU + 等待事件 + SQL）
--   2. TOP SQL by CPU 时间
--   3. TOP SQL by 总耗时（Elapsed Time）
--   4. TOP SQL by 内存消耗（Shared Memory / Sharable Mem）
--   5. TOP SQL by I/O（物理读写）
--   6. 会话级 PGA/Temp/Undo 资源消耗
--   7. 并行查询资源消耗
--   8. 最近活跃高资源SQL（ASH 实时）
--   9. 全表扫描大表SQL
--  10. 资源消耗趋势（按小时统计）
-- ============================================================================

-- 创建输出目录
HOST mkdir -p /Users/xiaoqi/Documents/work/yili/ai-spec/skills/db/oracle-dba/output

-- 输出到固定文件（SPOOL OFF 后会自动复制带时间戳副本）
SPOOL /Users/xiaoqi/Documents/work/yili/ai-spec/skills/db/oracle-dba/output/resource_hog_sql_latest.txt

SET LINESIZE 300
SET PAGESIZE 1000
SET FEEDBACK OFF
SET VERIFY OFF
SET LONG 10000
SET TRIMSPOOL ON
COL sql_id FORMAT A15
COL username FORMAT A20
COL program FORMAT A30
COL module FORMAT A30
COL machine FORMAT A25
COL event FORMAT A40
COL sql_preview FORMAT A80
COL dml_type FORMAT A8
COL object_name FORMAT A30
COL tablespace_name FORMAT A20

PROMPT ============================================================================
PROMPT              资源消耗SQL定位报告 (Resource Hog SQL Finder)
PROMPT ============================================================================
PROMPT 报告时间:
SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') report_time FROM dual;
PROMPT 

-- ============================================================================
-- 1. 活跃会话资源消耗全景
-- ============================================================================
PROMPT >>> 1. 活跃会话资源消耗全景（当前正在消耗资源的会话 + SQL）
PROMPT     说明: ON CPU 表示正在计算; 其他event表示在等待某种资源
PROMPT 

COL cpu_sec FORMAT 999,999.99
COL elapsed_sec FORMAT 999,999.99
COL seconds_in_wait FORMAT 999,999

SELECT 
    s.sid,
    s.serial#,
    s.username,
    s.status,
    s.event,
    s.seconds_in_wait,
    s.sql_id,
    SUBSTR(q.sql_text, 1, 80) sql_preview,
    q.executions,
    ROUND(q.elapsed_time/1000000, 2) elapsed_sec,
    ROUND(q.cpu_time/1000000, 2) cpu_sec,
    s.program,
    s.module,
    s.machine
FROM v$session s
JOIN v$sql q ON s.sql_id = q.sql_id AND s.sql_child_number = q.child_number
WHERE s.status = 'ACTIVE'
  AND s.type != 'BACKGROUND'
  AND s.username IS NOT NULL
ORDER BY q.cpu_time DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 2. TOP SQL by CPU 时间（累计最高CPU消耗）
-- ============================================================================
PROMPT 
PROMPT >>> 2. TOP SQL by CPU 时间（累计CPU消耗最高的SQL）
PROMPT     说明: 即使单次CPU消耗低,执行次数多累计也会很高
PROMPT 

COL gets_per_exec FORMAT 999,999,999
COL rows_per_exec FORMAT 999,999,999
COL ms_per_exec FORMAT 999,999.99

SELECT 
    sql_id,
    executions,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    buffer_gets,
    disk_reads,
    rows_processed,
    ROUND(cpu_time/NULLIF(executions,0)/1000, 2) ms_per_exec,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    parsing_schema_name,
    module
FROM v$sql
WHERE executions > 0
  AND cpu_time > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
  AND parsing_schema_name NOT IN ('SYS', 'SYSTEM')
ORDER BY cpu_time DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 3. TOP SQL by Elapsed Time（总耗时最长）
-- ============================================================================
PROMPT 
PROMPT >>> 3. TOP SQL by Elapsed Time（总耗时最长的SQL）
PROMPT     说明: CPU_RATIO% = CPU占比, 低于50%说明等待时间多
PROMPT 

COL cpu_ratio FORMAT A10

SELECT 
    sql_id,
    executions,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(cpu_time/NULLIF(elapsed_time,0)*100, 1) || '%' cpu_ratio,
    ROUND(elapsed_time/NULLIF(executions,0)/1000, 2) ms_per_exec,
    buffer_gets,
    disk_reads,
    rows_processed,
    parsing_schema_name,
    module
FROM v$sql
WHERE executions > 0
  AND elapsed_time > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
  AND parsing_schema_name NOT IN ('SYS', 'SYSTEM')
ORDER BY elapsed_time DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 4. TOP SQL by 内存消耗（Shared Pool 内存占用）
-- ============================================================================
PROMPT 
PROMPT >>> 4. TOP SQL by 内存消耗（Shared Pool 占用最大的SQL）
PROMPT     说明: sharable_mem 为游标在共享池中占用的内存
PROMPT 

COL sharable_mb FORMAT 999,999.99
COL persistent_mb FORMAT 999,999.99
COL runtime_mb FORMAT 999,999.99

SELECT 
    sql_id,
    ROUND(sharable_mem/1024/1024, 2) sharable_mb,
    ROUND(persistent_mem/1024/1024, 2) persistent_mb,
    ROUND(runtime_mem/1024/1024, 2) runtime_mb,
    -- version_count 在 Oracle 12c+ 可用, 11g 需要移除
    -- version_count,
    loaded_versions,
    executions,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    parsing_schema_name,
    module
FROM v$sql
WHERE sharable_mem > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
  AND parsing_schema_name NOT IN ('SYS', 'SYSTEM')
ORDER BY sharable_mem DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 5. TOP SQL by I/O（物理读写最多）
-- ============================================================================
PROMPT 
PROMPT >>> 5. TOP SQL by I/O（物理读最多的SQL）
PROMPT     说明: 物理读高意味着数据没命中Buffer Cache,可能需要加索引或增大SGA
PROMPT 

COL reads_per_exec FORMAT 999,999,999
COL hit_ratio FORMAT A10

SELECT 
    sql_id,
    executions,
    disk_reads,
    buffer_gets,
    ROUND(disk_reads/NULLIF(executions,0)) reads_per_exec,
    ROUND(buffer_gets/NULLIF(executions,0)) gets_per_exec,
    CASE WHEN buffer_gets > 0 
         THEN ROUND((1 - disk_reads/buffer_gets)*100, 1) || '%'
         ELSE 'N/A' END hit_ratio,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    rows_processed,
    parsing_schema_name,
    module
FROM v$sql
WHERE executions > 0
  AND disk_reads > 0
  AND sql_text NOT LIKE '%v$%'
  AND sql_text NOT LIKE '%dba_%'
  AND parsing_schema_name NOT IN ('SYS', 'SYSTEM')
ORDER BY disk_reads DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 6. 会话级 PGA/Temp/Undo 资源消耗
-- ============================================================================
PROMPT 
PROMPT >>> 6. 会话级资源消耗（PGA内存 + Temp占用 + Undo占用）
PROMPT     说明: PGA高可能有大排序/Hash Join; Temp高可能磁盘排序; Undo高可能大事务
PROMPT 

COL pga_mb FORMAT 999,999.99
COL temp_mb FORMAT 999,999.99

SELECT 
    s.sid,
    s.serial#,
    s.username,
    s.program,
    s.module,
    s.machine,
    s.status,
    s.sql_id,
    ROUND(p.pga_used_mem/1024/1024, 2) pga_mb,
    ROUND(NVL(t.blocks * (SELECT value FROM v$parameter WHERE name = 'db_block_size') / 1024 / 1024, 0), 2) temp_mb,
    ROUND((SYSDATE - s.logon_time) * 24, 2) login_hours
FROM v$session s
JOIN v$process p ON s.paddr = p.addr
LEFT JOIN (
    SELECT session_addr, SUM(blocks) blocks
    FROM v$tempseg_usage
    GROUP BY session_addr
) t ON s.saddr = t.session_addr
WHERE s.username IS NOT NULL
  AND s.type != 'BACKGROUND'
ORDER BY p.pga_used_mem DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 7. 并行查询资源消耗
-- ============================================================================
PROMPT 
PROMPT >>> 7. 当前并行查询资源消耗
PROMPT     说明: 并行查询占用多个CPU核心和PGA内存,可能影响其他会话
PROMPT 

COL req_degree FORMAT 999
COL actual_degree FORMAT 999
COL qc_sid FORMAT 99999

SELECT 
    px.qcsid qc_sid,
    s.username,
    s.sql_id,
    px.req_degree,
    px.degree actual_degree,
    COUNT(*) slave_count,
    ROUND(SUM(p.pga_used_mem)/1024/1024, 2) total_pga_mb,
    s.module,
    SUBSTR(q.sql_text, 1, 60) sql_preview
FROM v$px_session px
JOIN v$session s ON px.qcsid = s.sid
JOIN v$process p ON s.paddr = p.addr
LEFT JOIN v$sql q ON s.sql_id = q.sql_id AND s.sql_child_number = q.child_number
WHERE px.qcsid IS NOT NULL
GROUP BY px.qcsid, s.username, s.sql_id, px.req_degree, px.degree, s.module, q.sql_text
ORDER BY slave_count DESC;

-- ============================================================================
-- 8. 最近活跃高资源SQL（ASH 实时采样）
-- ============================================================================
PROMPT 
PROMPT >>> 8. 最近30分钟内活跃次数最多的SQL（ASH采样）
PROMPT     说明: 采样次数越多说明该SQL占用活跃时间越长
PROMPT 

COL sample_count FORMAT 999,999
COL on_cpu_count FORMAT 999,999
COL wait_count FORMAT 999,999
COL top_event FORMAT A35
COL pct_db_time FORMAT A10

SELECT 
    sql_id,
    COUNT(*) sample_count,
    SUM(CASE WHEN session_state = 'ON CPU' THEN 1 ELSE 0 END) on_cpu_count,
    SUM(CASE WHEN session_state = 'WAITING' THEN 1 ELSE 0 END) wait_count,
    ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM v$active_session_history WHERE sample_time > SYSDATE - INTERVAL '30' MINUTE AND sql_id IS NOT NULL), 1) || '%' pct_db_time,
    MAX(CASE WHEN session_state = 'WAITING' THEN event ELSE NULL END) top_event,
    MAX(module) module,
    MAX(user_id) user_id
FROM v$active_session_history
WHERE sample_time > SYSDATE - INTERVAL '30' MINUTE
  AND sql_id IS NOT NULL
GROUP BY sql_id
ORDER BY sample_count DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 9. 全表扫描大表SQL
-- ============================================================================
PROMPT 
PROMPT >>> 9. 正在执行全表扫描的SQL（大表告警）
PROMPT     说明: 大表全表扫描会消耗大量I/O和CPU,应考虑添加索引
PROMPT 

SELECT DISTINCT
    s.sql_id,
    p.object_owner,
    p.object_name,
    t.num_rows,
    ROUND(t.blocks * (SELECT value FROM v$parameter WHERE name = 'db_block_size') / 1024 / 1024, 2) table_size_mb,
    s.executions,
    ROUND(s.elapsed_time/1000000, 2) elapsed_sec,
    ROUND(s.cpu_time/1000000, 2) cpu_sec,
    s.disk_reads,
    s.buffer_gets,
    s.module
FROM v$sql_plan p
JOIN v$sql s ON p.sql_id = s.sql_id AND p.child_number = s.child_number
JOIN dba_tables t ON p.object_owner = t.owner AND p.object_name = t.table_name
WHERE p.operation = 'TABLE ACCESS'
  AND p.options = 'FULL'
  AND t.num_rows > 100000
  AND p.object_owner NOT IN ('SYS', 'SYSTEM')
  AND s.sql_text NOT LIKE '%v$%'
  AND s.sql_text NOT LIKE '%dba_%'
ORDER BY t.num_rows DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 10. 资源消耗趋势（按小时统计 - 基于AWR/ASH）
-- ============================================================================
PROMPT 
PROMPT >>> 10. 最近24小时资源消耗趋势（按小时统计）
PROMPT     说明: 帮助识别资源消耗高峰时段
PROMPT 

COL hour_slot FORMAT A16
COL active_samples FORMAT 999,999
COL cpu_samples FORMAT 999,999
COL io_samples FORMAT 999,999
COL other_samples FORMAT 999,999

SELECT 
    TO_CHAR(TRUNC(sample_time, 'HH'), 'MM-DD HH24:MI') hour_slot,
    COUNT(*) active_samples,
    SUM(CASE WHEN session_state = 'ON CPU' THEN 1 ELSE 0 END) cpu_samples,
    SUM(CASE WHEN wait_class = 'User I/O' THEN 1 ELSE 0 END) io_samples,
    SUM(CASE WHEN wait_class = 'Concurrency' THEN 1 ELSE 0 END) lock_samples,
    SUM(CASE WHEN session_state = 'WAITING' 
              AND wait_class NOT IN ('User I/O', 'Concurrency', 'Idle') THEN 1 ELSE 0 END) other_samples,
    COUNT(DISTINCT sql_id) unique_sql_count,
    COUNT(DISTINCT session_id) unique_session_count
FROM v$active_session_history
WHERE sample_time > SYSDATE - 1
GROUP BY TRUNC(sample_time, 'HH')
ORDER BY TRUNC(sample_time, 'HH') DESC;

-- ============================================================================
-- 11. 指定SQL详情查看（交互式）
-- ============================================================================
PROMPT 
PROMPT >>> 如需查看某个SQL的完整文本和执行计划，请输入SQL_ID:
ACCEPT hog_sql_id PROMPT 'SQL_ID (直接回车跳过): '

SET TERMOUT OFF
COLUMN has_input NEW_VALUE run_hog_detail
SELECT CASE WHEN '&hog_sql_id' IS NULL OR '&hog_sql_id' = '' 
            THEN 'NO' ELSE 'YES' END has_input 
FROM dual;
SET TERMOUT ON

SET TERMOUT &run_hog_detail

PROMPT 
PROMPT >>> SQL完整文本:
SELECT sql_fulltext FROM v$sql WHERE sql_id = '&hog_sql_id' AND ROWNUM = 1;

PROMPT 
PROMPT >>> SQL执行计划:
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&hog_sql_id', NULL, 'ALLSTATS LAST'));

PROMPT 
PROMPT >>> SQL执行统计详情:
SELECT 
    sql_id,
    child_number,
    plan_hash_value,
    executions,
    ROUND(cpu_time/1000000, 2) cpu_sec,
    ROUND(elapsed_time/1000000, 2) elapsed_sec,
    ROUND(user_io_wait_time/1000000, 2) io_wait_sec,
    ROUND(application_wait_time/1000000, 2) app_wait_sec,
    buffer_gets,
    disk_reads,
    direct_writes,
    rows_processed,
    ROUND(sharable_mem/1024/1024, 2) sharable_mb,
    fetches,
    parse_calls,
    sorts,
    loads,
    invalidations,
    module,
    parsing_schema_name
FROM v$sql
WHERE sql_id = '&hog_sql_id';

SET TERMOUT ON

PROMPT 
PROMPT ============================================================================
PROMPT                     资源消耗SQL定位报告完成
PROMPT 
PROMPT 快速优化指南:
PROMPT ──────────────────────────────────────────────────────────
PROMPT [CPU高]    → 检查执行计划,考虑索引优化或SQL改写
PROMPT [I/O高]    → 检查全表扫描,考虑添加索引或增大Buffer Cache
PROMPT [内存高]   → 检查loaded_versions,可能绑定变量问题或游标泄漏
PROMPT [PGA高]    → 检查大排序/Hash Join,考虑增大PGA_AGGREGATE_TARGET
PROMPT [Temp高]   → 磁盘排序,考虑SQL改写减少排序或增大PGA
PROMPT [Undo高]   → 大事务,考虑拆分批次提交
PROMPT [并行高]   → 过度并行,考虑限制DOP或禁用并行
PROMPT [全表扫描] → 大表扫描,优先添加合适的索引
PROMPT ──────────────────────────────────────────────────────────
PROMPT ============================================================================
PROMPT 

SET FEEDBACK ON
SET VERIFY ON
UNDEFINE hog_sql_id

SPOOL OFF

-- 自动复制一份带时间戳的文件
HOST cp /Users/xiaoqi/Documents/work/yili/ai-spec/skills/db/oracle-dba/output/resource_hog_sql_latest.txt /Users/xiaoqi/Documents/work/yili/ai-spec/skills/db/oracle-dba/output/resource_hog_sql_$(date +\%Y\%m\%d_\%H\%M\%S).txt

PROMPT 
PROMPT 输出已保存到 output 目录
PROMPT 
