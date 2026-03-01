--------------------------------------------------------------------------------
-- 慢SQL分析脚本
-- 功能: 分析执行时间最长的SQL语句
-- 作者: sevenxiao
-- 日期: 2026-02-28
-- 用法: sql user/pass@db @slow_sql_analysis.sql
--------------------------------------------------------------------------------

SET ECHO OFF
SET FEEDBACK ON
SET HEADING ON
SET LINESIZE 200
SET PAGESIZE 100
SET VERIFY OFF

PROMPT
PROMPT ================================================================================
PROMPT                 慢SQL分析工具
PROMPT ================================================================================
PROMPT

-- 接受用户输入模块名称
ACCEPT module_pattern CHAR PROMPT '请输入模块名称模式 (如: Fssc% 或直接回车查询所有): ' DEFAULT '%'

PROMPT
PROMPT ================================================================================
PROMPT 1. TOP 50 慢SQL - 按平均执行时间排序
PROMPT ================================================================================
PROMPT

COLUMN MODULE FORMAT A30 HEADING "模块名称"
COLUMN SQL_TEXT FORMAT A80 HEADING "执行SQL"
COLUMN EXECUTIONS FORMAT 999,999,999 HEADING "执行次数"
COLUMN TOTAL_TIME FORMAT 999,999.99 HEADING "总执行时间(秒)"
COLUMN AVG_TIME FORMAT 999,999.99 HEADING "平均执行时间(秒)"
COLUMN HASH_VALUE FORMAT 9999999999 HEADING "哈希值"

SELECT 
    sa.MODULE,
    SUBSTR(sa.SQL_TEXT, 1, 80) AS SQL_TEXT,
    sa.EXECUTIONS,
    ROUND(sa.ELAPSED_TIME / 1000000, 2) AS TOTAL_TIME,
    ROUND(sa.ELAPSED_TIME / 1000000 / sa.EXECUTIONS, 2) AS AVG_TIME,
    sa.HASH_VALUE
FROM v$sqlarea sa
WHERE sa.EXECUTIONS > 0 
  AND sa.MODULE LIKE '&module_pattern'
ORDER BY (sa.ELAPSED_TIME / sa.EXECUTIONS) DESC
FETCH FIRST 50 ROWS ONLY;

PROMPT
PROMPT ================================================================================
PROMPT 2. TOP 50 全表扫描SQL - 按平均执行时间排序
PROMPT ================================================================================
PROMPT

COLUMN SQL_ID FORMAT A15 HEADING "SQL ID"
COLUMN SQL_TEXT FORMAT A60 HEADING "SQL文本"
COLUMN ACCESS_TYPE FORMAT A30 HEADING "访问类型"
COLUMN MODULE FORMAT A20 HEADING "模块"
COLUMN LAST_ACTIVE FORMAT A20 HEADING "最近执行时间"
COLUMN TOTAL_ELAPSED FORMAT 999,999.99 HEADING "总耗时(秒)"
COLUMN EXEC_COUNT FORMAT 999,999 HEADING "执行次数"
COLUMN AVG_ELAPSED FORMAT 999.9999 HEADING "平均耗时(秒)"

SELECT  
    p.SQL_ID, 
    SUBSTR(s.SQL_TEXT, 1, 60) AS SQL_TEXT,
    p.OPERATION || ' ' || p.OPTIONS AS ACCESS_TYPE,
    a.MODULE,
    TO_CHAR(s.LAST_ACTIVE_TIME, 'YYYY-MM-DD HH24:MI:SS') AS LAST_ACTIVE,
    ROUND(s.ELAPSED_TIME / 1000000, 2) AS TOTAL_ELAPSED,
    s.EXECUTIONS AS EXEC_COUNT,
    ROUND((s.ELAPSED_TIME / NULLIF(s.EXECUTIONS, 0)) / 1000000, 4) AS AVG_ELAPSED
FROM v$sql_plan p
JOIN v$sql s ON p.SQL_ID = s.SQL_ID
JOIN v$sqlarea a ON s.SQL_ID = a.SQL_ID
WHERE p.OPERATION = 'TABLE ACCESS' 
  AND p.OPTIONS = 'FULL'
  AND a.MODULE LIKE '&module_pattern'
  AND s.EXECUTIONS > 0
ORDER BY AVG_ELAPSED DESC
FETCH FIRST 50 ROWS ONLY;

PROMPT
PROMPT ================================================================================
PROMPT 3. 详细全表扫描SQL分析 (包含完整SQL文本)
PROMPT ================================================================================
PROMPT

-- 提示用户是否需要查看完整SQL
ACCEPT show_full CHAR PROMPT '是否显示完整SQL文本? (y/n, 默认: n): ' DEFAULT 'n'

SET LONG 100000
SET LONGCHUNKSIZE 100000

COLUMN SQL_ID FORMAT A15 HEADING "SQL ID"
COLUMN SQL_TEXT FORMAT A100 HEADING "SQL摘要"
COLUMN SQL_FULLTEXT FORMAT A100 HEADING "完整SQL"
COLUMN ACCESS_TYPE FORMAT A30 HEADING "访问类型"
COLUMN MODULE FORMAT A20 HEADING "模块"
COLUMN AVG_ELAPSED FORMAT 999.9999 HEADING "平均耗时(秒)"

SELECT  
    p.SQL_ID, 
    SUBSTR(s.SQL_TEXT, 1, 100) AS SQL_TEXT,
    CASE WHEN '&show_full' = 'y' THEN s.SQL_FULLTEXT ELSE NULL END AS SQL_FULLTEXT,
    p.OPERATION || ' ' || p.OPTIONS AS ACCESS_TYPE,
    a.MODULE,
    ROUND((s.ELAPSED_TIME / NULLIF(s.EXECUTIONS, 0)) / 1000000, 4) AS AVG_ELAPSED
FROM v$sql_plan p
JOIN v$sql s ON p.SQL_ID = s.SQL_ID
JOIN v$sqlarea a ON s.SQL_ID = a.SQL_ID
WHERE p.OPERATION = 'TABLE ACCESS' 
  AND p.OPTIONS = 'FULL'
  AND a.MODULE LIKE '&module_pattern'
  AND s.EXECUTIONS > 0
ORDER BY AVG_ELAPSED DESC
FETCH FIRST 100 ROWS ONLY;

PROMPT
PROMPT ================================================================================
PROMPT 4. SQL性能统计汇总
PROMPT ================================================================================
PROMPT

COLUMN METRIC FORMAT A30 HEADING "指标"
COLUMN VALUE FORMAT A50 HEADING "值"

SELECT '模块过滤条件' AS METRIC, '&module_pattern' AS VALUE FROM dual
UNION ALL
SELECT '慢SQL总数', TO_CHAR(COUNT(*)) 
FROM v$sqlarea 
WHERE EXECUTIONS > 0 AND MODULE LIKE '&module_pattern'
UNION ALL
SELECT '全表扫描SQL数量', TO_CHAR(COUNT(DISTINCT p.SQL_ID))
FROM v$sql_plan p
JOIN v$sqlarea a ON p.SQL_ID = a.SQL_ID
WHERE p.OPERATION = 'TABLE ACCESS' 
  AND p.OPTIONS = 'FULL'
  AND a.MODULE LIKE '&module_pattern'
UNION ALL
SELECT '平均执行时间最长的SQL_ID', 
       (SELECT SQL_ID FROM (
           SELECT SQL_ID 
           FROM v$sqlarea 
           WHERE EXECUTIONS > 0 AND MODULE LIKE '&module_pattern'
           ORDER BY (ELAPSED_TIME / EXECUTIONS) DESC 
           FETCH FIRST 1 ROWS ONLY
       ))
FROM dual;

PROMPT
PROMPT ================================================================================
PROMPT 分析完成! 
PROMPT ================================================================================
PROMPT
PROMPT 后续操作建议:
PROMPT 1. 对于慢SQL，使用以下命令查看执行计划:
PROMPT    SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('SQL_ID'));
PROMPT
PROMPT 2. 对于全表扫描，检查是否缺少索引:
PROMPT    - 分析WHERE条件中的列
PROMPT    - 检查现有索引: SELECT * FROM dba_indexes WHERE table_name = 'XXX';
PROMPT
PROMPT 3. 收集统计信息:
PROMPT    EXEC DBMS_STATS.GATHER_TABLE_STATS('SCHEMA', 'TABLE_NAME');
PROMPT
PROMPT 4. 查看更详细的TOP SQL分析，运行:
PROMPT    @top_sql.sql
PROMPT ================================================================================

-- 清理变量
UNDEFINE module_pattern
UNDEFINE show_full

SET ECHO ON
SET VERIFY ON
