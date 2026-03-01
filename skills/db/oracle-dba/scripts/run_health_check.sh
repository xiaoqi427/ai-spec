#!/bin/bash

# 设置 Java 21 环境
export JAVA_HOME=/Users/xiaoqi/Library/Java/JavaVirtualMachines/corretto-21.0.9/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

echo "使用 Java 版本:"
java -version

# 执行健康检查脚本
echo "\n开始执行数据库健康检查..."

# 默认输出到当前目录
OUTPUT_FILE="${1:-health_report_$(date +%Y%m%d_%H%M%S).txt}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sql yladmin/ggcjd4slhtjyx!@10.119.254.69:1521/yldb <<EOF > "$OUTPUT_FILE"
@${SCRIPT_DIR}/health_check.sql
exit
EOF

echo "\n健康检查报告已生成: $OUTPUT_FILE"
