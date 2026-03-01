-- ============================================================================
-- 锁等待分析脚本
-- 功能: 分析数据库锁等待情况，显示锁等待树
-- 使用: sqlplus user/pass@db @lock_tree.sql
-- 作者: sevenxiao
-- 日期: 2025-02-28
-- ============================================================================

SET LINESIZE 200
SET PAGESIZE 1000
SET FEEDBACK OFF
SET VERIFY OFF

PROMPT ============================================================================
PROMPT                        数据库锁等待分析
PROMPT ============================================================================
PROMPT 

-- 当前锁等待概况
PROMPT >>> 1. 锁等待概况
PROMPT 
SELECT 
    COUNT(DISTINCT blocking_session) blocking_sessions,
    COUNT(*) waiting_sessions,
    MAX(seconds_in_wait) max_wait_seconds
FROM v$session
WHERE blocking_session IS NOT NULL;

-- 详细的锁等待信息
PROMPT 
PROMPT >>> 2. 锁等待详细信息
PROMPT 
COL waiting_sid FORMAT 9999
COL waiting_user FORMAT A15
COL waiting_program FORMAT A30
COL holding_sid FORMAT 9999
COL holding_user FORMAT A15
COL holding_program FORMAT A30
COL object_name FORMAT A30
COL lock_type FORMAT A10
COL wait_min FORMAT 999.99

SELECT 
    ws.sid waiting_sid,
    ws.username waiting_user,
    ws.program waiting_program,
    ws.blocking_session holding_sid,
    hs.username holding_user,
    hs.program holding_program,
    o.object_name,
    o.object_type,
    wl.type lock_type,
    wl.lmode current_mode,
    wl.request requested_mode,
    ROUND(ws.seconds_in_wait/60, 2) wait_min,
    ws.sql_id waiting_sql_id,
    hs.sql_id holding_sql_id
FROM v$session ws
JOIN v$session hs ON ws.blocking_session = hs.sid
LEFT JOIN v$lock wl ON ws.sid = wl.sid AND wl.request > 0
LEFT JOIN dba_objects o ON wl.id1 = o.object_id
WHERE ws.blocking_session IS NOT NULL
ORDER BY ws.seconds_in_wait DESC;

-- 锁等待树（层级关系）
PROMPT 
PROMPT >>> 3. 锁等待树（显示阻塞链）
PROMPT 
COL tree_level FORMAT 999
COL sid FORMAT 9999
COL username FORMAT A15
COL program FORMAT A30
COL status FORMAT A10
COL wait_event FORMAT A30
COL seconds_waiting FORMAT 999,999

WITH lock_tree AS (
  -- 顶级阻塞会话（没有被其他会话阻塞）
  SELECT 
    sid,
    blocking_session,
    username,
    program,
    status,
    event,
    seconds_in_wait,
    sql_id,
    1 AS tree_level,
    TO_CHAR(sid) AS path
  FROM v$session
  WHERE blocking_session IS NULL
    AND sid IN (SELECT blocking_session FROM v$session WHERE blocking_session IS NOT NULL)
  
  UNION ALL
  
  -- 递归查找被阻塞的会话
  SELECT 
    s.sid,
    s.blocking_session,
    s.username,
    s.program,
    s.status,
    s.event,
    s.seconds_in_wait,
    s.sql_id,
    lt.tree_level + 1,
    lt.path || ' -> ' || TO_CHAR(s.sid)
  FROM v$session s
  JOIN lock_tree lt ON s.blocking_session = lt.sid
  WHERE s.blocking_session IS NOT NULL
)
SELECT 
  tree_level,
  LPAD(' ', (tree_level-1)*2) || sid AS sid,
  username,
  program,
  status,
  event wait_event,
  seconds_in_wait seconds_waiting,
  sql_id,
  path blocking_chain
FROM lock_tree
ORDER BY path, tree_level;

-- 阻塞会话的SQL
PROMPT 
PROMPT >>> 4. 阻塞会话正在执行的SQL
PROMPT 
SELECT DISTINCT
    hs.sid,
    hs.username,
    hs.sql_id,
    sq.sql_text,
    ROUND((SYSDATE - hs.sql_exec_start) * 24 * 60, 2) runtime_min
FROM v$session ws
JOIN v$session hs ON ws.blocking_session = hs.sid
LEFT JOIN v$sql sq ON hs.sql_id = sq.sql_id
WHERE ws.blocking_session IS NOT NULL
  AND hs.sql_id IS NOT NULL;

-- 被阻塞会话的SQL
PROMPT 
PROMPT >>> 5. 被阻塞会话等待执行的SQL
PROMPT 
SELECT 
    ws.sid,
    ws.username,
    ws.sql_id,
    sq.sql_text,
    ROUND(ws.seconds_in_wait/60, 2) wait_min
FROM v$session ws
LEFT JOIN v$sql sq ON ws.sql_id = sq.sql_id
WHERE ws.blocking_session IS NOT NULL
  AND ws.sql_id IS NOT NULL
ORDER BY ws.seconds_in_wait DESC;

-- 锁类型统计
PROMPT 
PROMPT >>> 6. 当前锁类型统计
PROMPT 
SELECT 
    type lock_type,
    DECODE(type,
        'MR', 'Media Recovery',
        'RT', 'Redo Thread',
        'UN', 'User Name',
        'TX', 'Transaction',
        'TM', 'DML',
        'UL', 'PL/SQL User Lock',
        'DX', 'Distributed Xaction',
        'CF', 'Control File',
        'IS', 'Instance State',
        'FS', 'File Set',
        'IR', 'Instance Recovery',
        'ST', 'Disk Space Transaction',
        'TS', 'Temp Segment',
        'IV', 'Library Cache Invalidation',
        'LS', 'Log Start/Switch',
        'RW', 'Row Wait',
        'SQ', 'Sequence Number',
        'TE', 'Extend Table',
        'TT', 'Temp Table',
        type) lock_type_desc,
    COUNT(*) lock_count,
    SUM(CASE WHEN block = 1 THEN 1 ELSE 0 END) blocking_count,
    SUM(CASE WHEN request > 0 THEN 1 ELSE 0 END) waiting_count
FROM v$lock
GROUP BY type
ORDER BY lock_count DESC;

PROMPT 
PROMPT >>> 7. 锁等待解决建议
PROMPT 
PROMPT 解决步骤:
PROMPT 1. 识别顶级阻塞会话（锁等待树中tree_level=1的会话）
PROMPT 2. 检查该会话的SQL（见上面"阻塞会话正在执行的SQL"）
PROMPT 3. 联系应用方确认该事务是否应该提交或回滚
PROMPT 4. 如果会话已挂死，可以考虑强制终止:
PROMPT    ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;
PROMPT 
PROMPT 预防措施:
PROMPT - 缩短事务时间，尽快提交或回滚
PROMPT - 避免在事务中进行长时间计算或等待
PROMPT - 合理使用行级锁而非表锁
PROMPT - 设置合理的锁超时时间
PROMPT 
PROMPT 注意: 强制终止会话可能导致事务回滚，请谨慎操作！
PROMPT 

-- 提供快速kill session的命令
PROMPT >>> 8. 快速终止会话命令（仅供参考）
PROMPT 
SELECT 
    'ALTER SYSTEM KILL SESSION ''' || hs.sid || ',' || hs.serial# || ''' IMMEDIATE;' kill_cmd,
    hs.sid,
    hs.username,
    hs.program,
    COUNT(DISTINCT ws.sid) blocked_sessions_count
FROM v$session ws
JOIN v$session hs ON ws.blocking_session = hs.sid
WHERE ws.blocking_session IS NOT NULL
GROUP BY hs.sid, hs.serial#, hs.username, hs.program
ORDER BY blocked_sessions_count DESC;

PROMPT 
PROMPT ============================================================================
PROMPT                        锁等待分析完成
PROMPT ============================================================================
PROMPT 

SET FEEDBACK ON
SET VERIFY ON
