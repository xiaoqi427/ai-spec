-- ============================================================================
-- 常用业务查询模板
-- 功能: 预置常用的报账单、配置、系统数据查询
-- 使用: sql user/pass@db @common_queries.sql
-- 作者: sevenxiao
-- 日期: 2026-04-04
-- ============================================================================
-- 交互式使用: 脚本会提示输入查询参数
-- 非交互式: 通过 DEFINE 预定义变量，如:
--   DEFINE claim_no = 'RMBS2025001234'
-- ============================================================================

SET LINESIZE 300
SET PAGESIZE 200
SET FEEDBACK ON
SET VERIFY OFF
SET LONG 10000
SET TRIMSPOOL ON

-- 输出目录
HOST mkdir -p /Users/xiaoqi/Documents/work/yili/ai-spec/skills/code/bug-fix-cycle/db-query/output
SPOOL /Users/xiaoqi/Documents/work/yili/ai-spec/skills/code/bug-fix-cycle/db-query/output/query_latest.txt

COL CLAIM_NO FORMAT A25
COL TEMPLATE_ID FORMAT A12
COL STATUS FORMAT A10
COL CREATOR FORMAT A20
COL MODIFIER FORMAT A20
COL ITEM_CODE FORMAT A15
COL ITEM_NAME FORMAT A30
COL PAYLIST_NO FORMAT A25
COL USER_NAME FORMAT A20
COL TEAM_NAME FORMAT A30

PROMPT ============================================================================
PROMPT              FSSC 常用业务查询模板
PROMPT ============================================================================
PROMPT 报告时间:
SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') query_time FROM dual;
PROMPT

-- ============================================================================
-- 1. 按报账单号查头信息
-- ============================================================================
PROMPT >>> 请输入报账单号 (直接回车跳过此查询):
ACCEPT p_claim_no PROMPT '报账单号: '

SET TERMOUT OFF
COLUMN has_claim NEW_VALUE run_claim_query
SELECT CASE WHEN '&p_claim_no' IS NULL OR '&p_claim_no' = ''
            THEN 'NO' ELSE 'YES' END has_claim
FROM dual;
SET TERMOUT ON

PROMPT
PROMPT >>> 1. 报账单头信息
SELECT
    CLAIM_NO,
    TEMPLATE_ID,
    STATUS,
    TOTAL_AMOUNT,
    CURRENCY_CODE,
    OU_CODE,
    COMPANY_CODE,
    CREATOR,
    TO_CHAR(CREATE_TIME, 'YYYY-MM-DD HH24:MI:SS') CREATE_TIME,
    MODIFIER,
    TO_CHAR(MODIFY_TIME, 'YYYY-MM-DD HH24:MI:SS') MODIFY_TIME
FROM T_RMBS_CLAIM
WHERE CLAIM_NO = '&p_claim_no'
  AND '&p_claim_no' IS NOT NULL
  AND '&p_claim_no' != '';

PROMPT
PROMPT >>> 2. 报账单行信息
SELECT
    CLAIM_NO,
    LINE_NO,
    ITEM_CODE,
    ITEM_NAME,
    AMOUNT,
    CURRENCY_CODE,
    TAX_AMOUNT
FROM T_RMBS_CLAIM_ITEM
WHERE CLAIM_NO = '&p_claim_no'
  AND '&p_claim_no' IS NOT NULL
  AND '&p_claim_no' != ''
ORDER BY LINE_NO;

PROMPT
PROMPT >>> 3. 支付单信息
SELECT
    PAYLIST_NO,
    CLAIM_NO,
    PAY_STATUS,
    PAY_AMOUNT,
    CURRENCY_CODE,
    PAYEE_NAME,
    BANK_ACCOUNT,
    TO_CHAR(CREATE_TIME, 'YYYY-MM-DD HH24:MI:SS') CREATE_TIME
FROM T_RMBS_PAYLIST
WHERE CLAIM_NO = '&p_claim_no'
  AND '&p_claim_no' IS NOT NULL
  AND '&p_claim_no' != '';

-- ============================================================================
-- 4. 按模板编号查最近报账单
-- ============================================================================
PROMPT
PROMPT >>> 请输入模板编号 (如 T044, 直接回车跳过):
ACCEPT p_template PROMPT '模板编号: '

PROMPT
PROMPT >>> 4. 最近 20 笔报账单 (按模板)
SELECT
    CLAIM_NO,
    TEMPLATE_ID,
    STATUS,
    TOTAL_AMOUNT,
    CREATOR,
    TO_CHAR(CREATE_TIME, 'YYYY-MM-DD HH24:MI:SS') CREATE_TIME
FROM T_RMBS_CLAIM
WHERE TEMPLATE_ID = '&p_template'
  AND '&p_template' IS NOT NULL
  AND '&p_template' != ''
ORDER BY CREATE_TIME DESC
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 5. 查配置表 - 会计分组
-- ============================================================================
PROMPT
PROMPT >>> 请输入会计分组名称关键字 (直接回车跳过):
ACCEPT p_team_name PROMPT '分组关键字: '

PROMPT
PROMPT >>> 5. 会计分组信息
SELECT
    TEAM_ID,
    TEAM_NAME,
    TEAM_CODE,
    STATUS,
    OU_CODE,
    TO_CHAR(MODIFY_TIME, 'YYYY-MM-DD HH24:MI:SS') MODIFY_TIME,
    MODIFIER_ID
FROM T_PROC_ACCOUNTANTTEAM
WHERE TEAM_NAME LIKE '%' || '&p_team_name' || '%'
  AND '&p_team_name' IS NOT NULL
  AND '&p_team_name' != ''
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================
-- 6. 查系统用户
-- ============================================================================
PROMPT
PROMPT >>> 请输入用户ID或用户名 (直接回车跳过):
ACCEPT p_user PROMPT '用户ID/名: '

PROMPT
PROMPT >>> 6. 系统用户信息
SELECT
    USER_ID,
    USER_NAME,
    STATUS,
    EMAIL,
    PHONE,
    TO_CHAR(CREATE_TIME, 'YYYY-MM-DD HH24:MI:SS') CREATE_TIME
FROM SYS_USER
WHERE (USER_ID = '&p_user' OR USER_NAME LIKE '%' || '&p_user' || '%')
  AND '&p_user' IS NOT NULL
  AND '&p_user' != ''
FETCH FIRST 10 ROWS ONLY;

-- ============================================================================
-- 7. 通用表查询 (指定表名和条件)
-- ============================================================================
PROMPT
PROMPT >>> 自定义查询 (输入完整 SQL, 直接回车跳过):
ACCEPT p_custom_sql PROMPT 'SQL> '

SET TERMOUT OFF
COLUMN has_custom NEW_VALUE run_custom_query
SELECT CASE WHEN '&p_custom_sql' IS NULL OR '&p_custom_sql' = ''
            THEN 'NO' ELSE 'YES' END has_custom
FROM dual;
SET TERMOUT ON

PROMPT
PROMPT >>> 7. 自定义查询结果
&p_custom_sql;

-- ============================================================================
PROMPT
PROMPT ============================================================================
PROMPT                    查询完成
PROMPT ============================================================================

SET FEEDBACK ON
SET VERIFY ON
UNDEFINE p_claim_no
UNDEFINE p_template
UNDEFINE p_team_name
UNDEFINE p_user
UNDEFINE p_custom_sql

SPOOL OFF
