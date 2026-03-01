#!/bin/bash
################################################################################
# 慢SQL分析Shell脚本
# 功能: 快速分析指定模块的慢SQL和全表扫描
# 作者: sevenxiao
# 日期: 2026-02-28
# 用法: ./analyze_slow_sql.sh [module_pattern] [output_file]
################################################################################

# 设置 Java 21 环境
export JAVA_HOME=/Users/xiaoqi/Library/Java/JavaVirtualMachines/corretto-21.0.9/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 数据库连接信息
DB_USER="yladmin"
DB_PASS='ggcjd4slhtjyx!'
DB_CONN="10.119.254.69:1521/yldb"

# 参数
MODULE_PATTERN=${1:-"Fssc%"}
OUTPUT_FILE=${2:-"slow_sql_report_$(date +%Y%m%d_%H%M%S).txt"}

echo "================================================================================"
echo "                    慢SQL分析工具"
echo "================================================================================"
echo "模块过滤: $MODULE_PATTERN"
echo "输出文件: $OUTPUT_FILE"
echo ""

# 创建临时SQL脚本
TEMP_SQL=$(mktemp /tmp/slow_sql_XXXXXX.sql)

cat > "$TEMP_SQL" <<EOF
SET ECHO OFF
SET FEEDBACK ON
SET HEADING ON
SET LINESIZE 200
SET PAGESIZE 100
SET VERIFY OFF

PROMPT
PROMPT ================================================================================
PROMPT 1. TOP 50 慢SQL - 按平均执行时间排序
PROMPT ================================================================================

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
FROM v\$sqlarea sa
WHERE sa.EXECUTIONS > 0 
  AND sa.MODULE LIKE '$MODULE_PATTERN'
ORDER BY (sa.ELAPSED_TIME / sa.EXECUTIONS) DESC
FETCH FIRST 50 ROWS ONLY;

PROMPT
PROMPT ================================================================================
PROMPT 2. TOP 50 全表扫描SQL - 按平均执行时间排序
PROMPT ================================================================================

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
FROM v\$sql_plan p
JOIN v\$sql s ON p.SQL_ID = s.SQL_ID
JOIN v\$sqlarea a ON s.SQL_ID = a.SQL_ID
WHERE p.OPERATION = 'TABLE ACCESS' 
  AND p.OPTIONS = 'FULL'
  AND a.MODULE LIKE '$MODULE_PATTERN'
  AND s.EXECUTIONS > 0
ORDER BY AVG_ELAPSED DESC
FETCH FIRST 50 ROWS ONLY;

PROMPT
PROMPT ================================================================================
PROMPT 3. SQL性能统计汇总
PROMPT ================================================================================

COLUMN METRIC FORMAT A30 HEADING "指标"
COLUMN VALUE FORMAT A50 HEADING "值"

SELECT '模块过滤条件' AS METRIC, '$MODULE_PATTERN' AS VALUE FROM dual
UNION ALL
SELECT '慢SQL总数', TO_CHAR(COUNT(*)) 
FROM v\$sqlarea 
WHERE EXECUTIONS > 0 AND MODULE LIKE '$MODULE_PATTERN'
UNION ALL
SELECT '全表扫描SQL数量', TO_CHAR(COUNT(DISTINCT p.SQL_ID))
FROM v\$sql_plan p
JOIN v\$sqlarea a ON p.SQL_ID = a.SQL_ID
WHERE p.OPERATION = 'TABLE ACCESS' 
  AND p.OPTIONS = 'FULL'
  AND a.MODULE LIKE '$MODULE_PATTERN';

EXIT;
EOF

# 执行SQL分析
echo "正在分析慢SQL，请稍候..."
sql ${DB_USER}/${DB_PASS}@${DB_CONN} @"$TEMP_SQL" > "$OUTPUT_FILE" 2>&1

# 删除临时文件
rm -f "$TEMP_SQL"

# 检查结果
if [[ -f "$OUTPUT_FILE" ]] && [[ -s "$OUTPUT_FILE" ]]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    LINE_COUNT=$(wc -l < "$OUTPUT_FILE")
    
    echo ""
    echo "✓ 慢SQL分析完成!"
    echo "  文件: $OUTPUT_FILE"
    echo "  大小: $FILE_SIZE"
    echo "  行数: $LINE_COUNT"
    echo ""
    echo "报告摘要:"
    echo "----------------------------------------"
    grep -A 5 "SQL性能统计汇总" "$OUTPUT_FILE" | tail -10
    echo ""
    echo "查看完整报告: cat $OUTPUT_FILE | less"
else
    echo "✗ 慢SQL分析失败"
    exit 1
fi
