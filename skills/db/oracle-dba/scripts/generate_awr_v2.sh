#!/bin/bash
################################################################################
# AWR报告生成脚本 v2
# 解决ORA-06550 PLS-00653错误
# 使用SPOOL方式直接输出，避免CLOB变量问题
################################################################################

# 设置 Java 21 环境
export JAVA_HOME=/Users/xiaoqi/Library/Java/JavaVirtualMachines/corretto-21.0.9/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

# 数据库连接信息
DB_USER="yladmin"
DB_PASS='ggcjd4slhtjyx!'
DB_CONN="10.119.254.69:1521/yldb"

# AWR快照参数
BEGIN_SNAP=${1:-59627}
END_SNAP=${2:-59628}
REPORT_TYPE=${3:-html}

# 输出文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
if [[ "$REPORT_TYPE" == "html" ]]; then
    OUTPUT_FILE="awr_report_v2_${BEGIN_SNAP}_${END_SNAP}_${TIMESTAMP}.html"
else
    OUTPUT_FILE="awr_report_v2_${BEGIN_SNAP}_${END_SNAP}_${TIMESTAMP}.txt"
fi

echo "================================================================================"
echo "                    生成AWR报告 V2"
echo "================================================================================"
echo "开始快照: $BEGIN_SNAP"
echo "结束快照: $END_SNAP"
echo "报告类型: $REPORT_TYPE"
echo "输出文件: $OUTPUT_FILE"
echo ""

# 创建临时SQL脚本
TEMP_SQL=$(mktemp /tmp/awr_gen_XXXXXX.sql)

cat > "$TEMP_SQL" <<EOF
SET ECHO OFF
SET FEEDBACK OFF
SET HEADING OFF
SET PAGESIZE 0
SET LINESIZE 32767
SET LONG 100000000
SET LONGCHUNKSIZE 100000
SET TRIMSPOOL ON
SET TERMOUT OFF
SET VERIFY OFF

SPOOL $OUTPUT_FILE

SELECT output 
FROM TABLE(
    DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_${REPORT_TYPE^^}(
        (SELECT dbid FROM v\$database),
        (SELECT instance_number FROM v\$instance),
        $BEGIN_SNAP,
        $END_SNAP
    )
);

SPOOL OFF

EXIT;
EOF

# 执行SQL脚本
echo "正在生成AWR报告，请稍候..."
sql -S ${DB_USER}/${DB_PASS}@${DB_CONN} @"$TEMP_SQL" 2>&1 | grep -v "^$" | head -20

# 删除临时文件
rm -f "$TEMP_SQL"

# 检查结果
if [[ -f "$OUTPUT_FILE" ]] && [[ -s "$OUTPUT_FILE" ]]; then
    # 检查文件是否包含错误信息
    if grep -q "ORA-" "$OUTPUT_FILE" 2>/dev/null; then
        echo "✗ AWR报告生成失败（包含Oracle错误）"
        echo "  错误信息："
        grep "ORA-" "$OUTPUT_FILE" | head -5
        exit 1
    fi
    
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    LINE_COUNT=$(wc -l < "$OUTPUT_FILE")
    
    echo ""
    echo "✓ AWR报告生成成功!"
    echo "  文件: $OUTPUT_FILE"
    echo "  大小: $FILE_SIZE"
    echo "  行数: $LINE_COUNT"
    echo ""
    echo "下一步操作:"
    if [[ "$REPORT_TYPE" == "html" ]]; then
        echo "  查看报告: open $OUTPUT_FILE"
    else
        echo "  查看报告: cat $OUTPUT_FILE | less"
    fi
    echo "  分析报告: python3 awr_analyzer.py $OUTPUT_FILE"
else
    echo "✗ AWR报告生成失败（文件为空或不存在）"
    exit 1
fi
