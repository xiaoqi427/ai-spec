--------------------------------------------------------------------------------
-- AWR报告生成脚本
-- 功能: 自动生成AWR报告（HTML或TEXT格式）
-- 作者: sevenxiao
-- 日期: 2025-02-28
-- 用法: sql user/pass@db @generate_awr.sql
--------------------------------------------------------------------------------

SET ECHO OFF
SET FEEDBACK OFF
SET HEADING ON
SET LINESIZE 200
SET PAGESIZE 1000
SET VERIFY OFF
SET TERMOUT ON

PROMPT
PROMPT ================================================================================
PROMPT               Oracle AWR报告生成工具
PROMPT ================================================================================
PROMPT

-- 检查数据库是否有AWR授权
DECLARE
    v_control_management_pack VARCHAR2(100);
BEGIN
    SELECT value INTO v_control_management_pack
    FROM v$parameter
    WHERE name = 'control_management_pack_access';
    
    IF v_control_management_pack = 'NONE' THEN
        DBMS_OUTPUT.PUT_LINE('警告: 数据库未启用诊断包授权(control_management_pack_access=NONE)');
        DBMS_OUTPUT.PUT_LINE('如果没有相应License，使用AWR可能违反Oracle授权协议');
        DBMS_OUTPUT.PUT_LINE('');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        NULL;
END;
/

-- 显示当前数据库信息
PROMPT
PROMPT 当前数据库信息:
PROMPT ================================================================================
SELECT 
    d.dbid,
    d.name AS db_name,
    i.instance_number AS inst_num,
    i.instance_name AS inst_name,
    i.version,
    i.host_name
FROM 
    v$database d,
    v$instance i;

-- 显示最近的AWR快照
PROMPT
PROMPT 最近20个AWR快照:
PROMPT ================================================================================
COLUMN snap_id FORMAT 99999 HEADING "Snap ID"
COLUMN begin_time FORMAT A20 HEADING "开始时间"
COLUMN end_time FORMAT A20 HEADING "结束时间"
COLUMN snap_level FORMAT 9 HEADING "级别"
COLUMN duration FORMAT A10 HEADING "持续时间"

SELECT 
    snap_id,
    TO_CHAR(begin_interval_time, 'YYYY-MM-DD HH24:MI') AS begin_time,
    TO_CHAR(end_interval_time, 'YYYY-MM-DD HH24:MI') AS end_time,
    snap_level,
    LPAD(EXTRACT(HOUR FROM (end_interval_time - begin_interval_time)), 2, '0') || ':' ||
    LPAD(EXTRACT(MINUTE FROM (end_interval_time - begin_interval_time)), 2, '0') AS duration
FROM 
    dba_hist_snapshot
WHERE 
    instance_number = (SELECT instance_number FROM v$instance)
ORDER BY 
    snap_id DESC
FETCH FIRST 20 ROWS ONLY;

PROMPT
PROMPT ================================================================================
PROMPT 请根据上述快照信息输入参数
PROMPT ================================================================================
PROMPT

-- 接受用户输入
ACCEPT begin_snap NUMBER PROMPT '输入开始快照ID (Begin Snap): '
ACCEPT end_snap NUMBER PROMPT '输入结束快照ID (End Snap): '
ACCEPT report_type CHAR PROMPT '选择报告格式 [html/text] (默认html): ' DEFAULT 'html'

-- 设置输出文件名
COLUMN report_name NEW_VALUE report_file
SELECT 
    'awr_' || 
    (SELECT instance_name FROM v$instance) || '_' ||
    '&begin_snap' || '_' || 
    '&end_snap' || '_' ||
    TO_CHAR(SYSDATE, 'YYYYMMDD_HH24MISS') || 
    DECODE(LOWER('&report_type'), 'text', '.txt', '.html') AS report_name
FROM dual;

-- 设置输出
SET TERMOUT OFF
SPOOL &report_file

-- 根据格式生成报告
BEGIN
    IF LOWER('&report_type') = 'text' THEN
        -- 生成TEXT格式报告
        FOR cur IN (
            SELECT output FROM TABLE(
                DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_TEXT(
                    l_dbid      => (SELECT dbid FROM v$database),
                    l_inst_num  => (SELECT instance_number FROM v$instance),
                    l_bid       => &begin_snap,
                    l_eid       => &end_snap
                )
            )
        ) LOOP
            DBMS_OUTPUT.PUT_LINE(cur.output);
        END LOOP;
    ELSE
        -- 生成HTML格式报告
        FOR cur IN (
            SELECT output FROM TABLE(
                DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(
                    l_dbid      => (SELECT dbid FROM v$database),
                    l_inst_num  => (SELECT instance_number FROM v$instance),
                    l_bid       => &begin_snap,
                    l_eid       => &end_snap
                )
            )
        ) LOOP
            DBMS_OUTPUT.PUT_LINE(cur.output);
        END LOOP;
    END IF;
END;
/

SPOOL OFF
SET TERMOUT ON

PROMPT
PROMPT ================================================================================
PROMPT AWR报告生成完成!
PROMPT ================================================================================
PROMPT 报告文件: &report_file
PROMPT 开始快照: &begin_snap
PROMPT 结束快照: &end_snap
PROMPT 报告格式: &report_type
PROMPT
PROMPT 下一步操作:
PROMPT 1. 查看报告文件: cat &report_file (如果是HTML,用浏览器打开)
PROMPT 2. 分析报告: python scripts/awr_analyzer.py &report_file
PROMPT 3. 参考指南: references/awr_guide.md
PROMPT ================================================================================
PROMPT

-- 清理
UNDEFINE begin_snap
UNDEFINE end_snap
UNDEFINE report_type
UNDEFINE report_file

SET ECHO ON
SET FEEDBACK ON
SET VERIFY ON
