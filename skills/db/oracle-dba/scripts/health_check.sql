-- ============================================================================
-- Oracle数据库健康检查脚本
-- 功能: 综合检查数据库健康状态
-- 使用: sqlplus user/pass@db @health_check.sql
-- 作者: sevenxiao
-- 日期: 2025-02-28
-- ============================================================================

SET LINESIZE 200
SET PAGESIZE 1000
SET FEEDBACK OFF
SET VERIFY OFF

PROMPT ============================================================================
PROMPT                     Oracle数据库健康检查报告
PROMPT ============================================================================
PROMPT 

-- 数据库基本信息
PROMPT >>> 1. 数据库基本信息
PROMPT 
SELECT 
    name db_name,
    db_unique_name,
    database_role,
    open_mode,
    log_mode,
    created,
    ROUND((SYSDATE - created)) db_age_days
FROM v$database;

PROMPT 
PROMPT >>> 2. 实例信息
PROMPT 
SELECT 
    instance_name,
    host_name,
    version,
    startup_time,
    status,
    database_status,
    ROUND((SYSDATE - startup_time)) uptime_days
FROM v$instance;

-- 表空间使用情况
PROMPT 
PROMPT >>> 3. 表空间使用情况（使用率>70%告警）
PROMPT 
SELECT 
    tablespace_name,
    ROUND(total_mb, 2) total_mb,
    ROUND(used_mb, 2) used_mb,
    ROUND(free_mb, 2) free_mb,
    ROUND(used_pct, 2) used_pct,
    CASE 
        WHEN used_pct >= 90 THEN '❌ 严重'
        WHEN used_pct >= 80 THEN '⚠️  警告'
        WHEN used_pct >= 70 THEN '⚡ 注意'
        ELSE '✅ 正常'
    END AS status
FROM (
    SELECT 
        df.tablespace_name,
        df.total_mb,
        df.total_mb - NVL(fs.free_mb, 0) used_mb,
        NVL(fs.free_mb, 0) free_mb,
        ROUND((df.total_mb - NVL(fs.free_mb, 0)) / df.total_mb * 100, 2) used_pct
    FROM
        (SELECT tablespace_name, SUM(bytes)/1024/1024 total_mb
         FROM dba_data_files
         GROUP BY tablespace_name) df
    LEFT JOIN
        (SELECT tablespace_name, SUM(bytes)/1024/1024 free_mb
         FROM dba_free_space
         GROUP BY tablespace_name) fs
    ON df.tablespace_name = fs.tablespace_name
)
ORDER BY used_pct DESC;

-- 临时表空间
PROMPT 
PROMPT >>> 4. 临时表空间使用情况
PROMPT 
SELECT 
    tablespace_name,
    ROUND(tablespace_size/1024/1024, 2) total_mb,
    ROUND(used_space/1024/1024, 2) used_mb,
    ROUND(free_space/1024/1024, 2) free_mb,
    ROUND(used_space/tablespace_size*100, 2) used_pct
FROM dba_temp_free_space
ORDER BY used_pct DESC;

-- 归档日志情况
PROMPT 
PROMPT >>> 5. 归档日志生成情况（最近7天）
PROMPT 
SELECT 
    TRUNC(first_time) log_date,
    COUNT(*) archives_count,
    ROUND(SUM(blocks * block_size)/1024/1024/1024, 2) total_gb,
    ROUND(AVG(blocks * block_size)/1024/1024, 2) avg_mb_per_archive
FROM v$archived_log
WHERE first_time > SYSDATE - 7
  AND dest_id = 1
GROUP BY TRUNC(first_time)
ORDER BY log_date DESC;

-- RMAN备份状态
PROMPT 
PROMPT >>> 6. 最近备份情况（最近7天）
PROMPT 
SELECT 
    TO_CHAR(start_time, 'YYYY-MM-DD HH24:MI') backup_time,
    input_type,
    status,
    ROUND(elapsed_seconds/60, 2) elapsed_min,
    ROUND(input_bytes/1024/1024/1024, 2) input_gb,
    ROUND(output_bytes/1024/1024/1024, 2) output_gb,
    ROUND(output_bytes/input_bytes*100, 2) compression_ratio
FROM v$rman_backup_job_details
WHERE start_time > SYSDATE - 7
ORDER BY start_time DESC;

-- 当前会话数
PROMPT 
PROMPT >>> 7. 会话统计
PROMPT 
SELECT 
    status,
    COUNT(*) session_count,
    ROUND(COUNT(*) * 100 / SUM(COUNT(*)) OVER(), 2) percentage
FROM v$session
GROUP BY status
ORDER BY session_count DESC;

PROMPT 
SELECT 
    program,
    COUNT(*) connection_count
FROM v$session
WHERE username IS NOT NULL
GROUP BY program
ORDER BY connection_count DESC
FETCH FIRST 10 ROWS ONLY;

-- TOP等待事件
PROMPT 
PROMPT >>> 8. TOP等待事件（排除空闲等待）
PROMPT 
SELECT 
    event,
    total_waits,
    ROUND(time_waited_micro/1000000, 2) time_waited_sec,
    ROUND(average_wait, 2) avg_wait_ms,
    wait_class
FROM v$system_event
WHERE wait_class != 'Idle'
  AND time_waited_micro > 0
ORDER BY time_waited_micro DESC
FETCH FIRST 15 ROWS ONLY;

-- 活动会话
PROMPT 
PROMPT >>> 9. 当前活动会话（非后台进程）
PROMPT 
SELECT 
    s.sid,
    s.serial#,
    s.username,
    s.status,
    s.program,
    s.last_call_et seconds_since_last_call,
    sw.event current_wait_event,
    sw.seconds_in_wait
FROM v$session s
LEFT JOIN v$session_wait sw ON s.sid = sw.sid
WHERE s.username IS NOT NULL
  AND s.status = 'ACTIVE'
ORDER BY s.last_call_et DESC;

-- 锁等待
PROMPT 
PROMPT >>> 10. 当前锁等待情况
PROMPT 
SELECT 
    l1.sid waiting_sid,
    s1.username waiting_user,
    s1.program waiting_program,
    l2.sid holding_sid,
    s2.username holding_user,
    s2.program holding_program,
    o.object_name,
    o.object_type,
    l1.type lock_type,
    ROUND((SYSDATE - s1.logon_time) * 24 * 60, 2) waiting_minutes
FROM v$lock l1
JOIN v$session s1 ON l1.sid = s1.sid
JOIN v$lock l2 ON l1.id1 = l2.id1 AND l1.id2 = l2.id2
JOIN v$session s2 ON l2.sid = s2.sid
LEFT JOIN dba_objects o ON l1.id1 = o.object_id
WHERE l1.block = 0
  AND l2.block = 1
  AND l1.request > 0;

-- 无效对象
PROMPT 
PROMPT >>> 11. 无效对象（排除系统用户）
PROMPT 
SELECT 
    owner,
    object_type,
    COUNT(*) invalid_count
FROM dba_objects
WHERE status = 'INVALID'
  AND owner NOT IN ('SYS', 'SYSTEM', 'XDB', 'MDSYS', 'CTXSYS', 'ORDSYS')
GROUP BY owner, object_type
ORDER BY invalid_count DESC;

-- 陈旧统计信息
PROMPT 
PROMPT >>> 12. 陈旧统计信息（>7天未更新且行数>1000）
PROMPT 
SELECT 
    owner,
    table_name,
    num_rows,
    TO_CHAR(last_analyzed, 'YYYY-MM-DD HH24:MI:SS') last_analyzed,
    TRUNC(SYSDATE - last_analyzed) days_old,
    stattype_locked
FROM dba_tab_statistics
WHERE owner NOT IN ('SYS', 'SYSTEM', 'XDB', 'MDSYS', 'CTXSYS', 'ORDSYS')
  AND (last_analyzed IS NULL OR last_analyzed < SYSDATE - 7)
  AND num_rows > 1000
ORDER BY days_old DESC NULLS FIRST
FETCH FIRST 20 ROWS ONLY;

-- Alert Log最近错误
PROMPT 
PROMPT >>> 13. Alert Log最近错误（最近24小时）
PROMPT 
SELECT 
    originating_timestamp,
    message_text
FROM v$diag_alert_ext
WHERE originating_timestamp > SYSDATE - 1
  AND (message_text LIKE '%ORA-%' 
       OR message_text LIKE '%ERROR%'
       OR message_text LIKE '%WARNING%')
ORDER BY originating_timestamp DESC
FETCH FIRST 20 ROWS ONLY;

-- 长时间运行的SQL
PROMPT 
PROMPT >>> 14. 长时间运行的SQL（>5分钟）
PROMPT 
SELECT 
    s.sid,
    s.serial#,
    s.username,
    s.sql_id,
    ROUND((SYSDATE - s.sql_exec_start) * 24 * 60, 2) runtime_min,
    SUBSTR(sq.sql_text, 1, 100) sql_text_preview
FROM v$session s
LEFT JOIN v$sql sq ON s.sql_id = sq.sql_id
WHERE s.sql_exec_start IS NOT NULL
  AND (SYSDATE - s.sql_exec_start) * 24 * 60 > 5
ORDER BY runtime_min DESC;

PROMPT 
PROMPT ============================================================================
PROMPT                        健康检查完成
PROMPT ============================================================================
PROMPT 

SET FEEDBACK ON
SET VERIFY ON
