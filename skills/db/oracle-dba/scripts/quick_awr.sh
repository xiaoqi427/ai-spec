#!/bin/bash

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
    OUTPUT_FILE="awr_report_${BEGIN_SNAP}_${END_SNAP}_${TIMESTAMP}.html"
else
    OUTPUT_FILE="awr_report_${BEGIN_SNAP}_${END_SNAP}_${TIMESTAMP}.txt"
fi

echo "================================================================================"
echo "                    生成AWR报告"
echo "================================================================================"
echo "开始快照: $BEGIN_SNAP"
echo "结束快照: $END_SNAP"
echo "报告类型: $REPORT_TYPE"
echo "输出文件: $OUTPUT_FILE"
echo ""

# 生成AWR报告
sql -S ${DB_USER}/${DB_PASS}@${DB_CONN} <<EOF > "$OUTPUT_FILE"
SET ECHO OFF
SET FEEDBACK OFF
SET HEADING OFF
SET PAGESIZE 0
SET LINESIZE 32767
SET LONG 1000000000
SET LONGCHUNKSIZE 1000000
SET TRIMSPOOL ON
SET TERMOUT OFF

VARIABLE l_report CLOB;

DECLARE
    l_dbid NUMBER;
    l_inst_num NUMBER;
BEGIN
    SELECT dbid INTO l_dbid FROM v\$database;
    SELECT instance_number INTO l_inst_num FROM v\$instance;
    
    IF LOWER('$REPORT_TYPE') = 'text' THEN
        :l_report := DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_TEXT(
            l_dbid     => l_dbid,
            l_inst_num => l_inst_num,
            l_bid      => $BEGIN_SNAP,
            l_eid      => $END_SNAP
        );
    ELSE
        :l_report := DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(
            l_dbid     => l_dbid,
            l_inst_num => l_inst_num,
            l_bid      => $BEGIN_SNAP,
            l_eid      => $END_SNAP
        );
    END IF;
END;
/

PRINT l_report

EXIT;
EOF

# 检查结果
if [[ -f "$OUTPUT_FILE" ]] && [[ -s "$OUTPUT_FILE" ]]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "✓ AWR报告生成成功!"
    echo "  文件: $OUTPUT_FILE"
    echo "  大小: $FILE_SIZE"
    echo ""
    echo "下一步操作:"
    if [[ "$REPORT_TYPE" == "html" ]]; then
        echo "  查看报告: open $OUTPUT_FILE"
    else
        echo "  查看报告: cat $OUTPUT_FILE | less"
    fi
    echo "  分析报告: python3 awr_analyzer.py $OUTPUT_FILE"
else
    echo "✗ AWR报告生成失败"
    exit 1
fi
