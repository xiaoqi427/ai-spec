#!/bin/bash

# 设置 Java 21 环境
export JAVA_HOME=/Users/xiaoqi/Library/Java/JavaVirtualMachines/corretto-21.0.9/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

echo "================================================================================"
echo "                    测试AWR报告生成"
echo "================================================================================"
echo ""

# 数据库连接信息
DB_USER="yladmin"
DB_PASS='ggcjd4slhtjyx!'
DB_CONN="10.119.254.69:1521/yldb"

echo "1. 查询最近的AWR快照..."
echo ""

sql -S ${DB_USER}/${DB_PASS}@${DB_CONN} <<'EOF'
SET PAGESIZE 50
SET LINESIZE 120
COLUMN snap_id FORMAT 99999 HEADING "快照ID"
COLUMN begin_time FORMAT A20 HEADING "开始时间"
COLUMN end_time FORMAT A20 HEADING "结束时间"

SELECT 
    snap_id,
    TO_CHAR(begin_interval_time, 'YYYY-MM-DD HH24:MI') AS begin_time,
    TO_CHAR(end_interval_time, 'YYYY-MM-DD HH24:MI') AS end_time
FROM 
    dba_hist_snapshot
WHERE 
    instance_number = (SELECT instance_number FROM v$instance)
ORDER BY 
    snap_id DESC
FETCH FIRST 10 ROWS ONLY;

EXIT;
EOF

echo ""
echo "================================================================================"
echo "请根据上面的快照信息，选择要生成报告的快照范围"
echo "然后运行: ./generate_awr.sh -u yladmin -p 'ggcjd4slhtjyx!' -c 10.119.254.69:1521/yldb -b <开始ID> -e <结束ID>"
echo "================================================================================"
