#!/bin/bash
# ============================================================================
# 资源消耗SQL诊断 - 启动脚本
# 功能: 连接Oracle执行诊断脚本，输出结果自动带时间戳
# 使用: ./run_resource_hog.sh
# 作者: sevenxiao
# 日期: 2026-03-10
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../output"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LATEST_FILE="$OUTPUT_DIR/resource_hog_sql_latest.txt"
OUTPUT_FILE="$OUTPUT_DIR/resource_hog_sql_${TIMESTAMP}.txt"

mkdir -p "$OUTPUT_DIR"

# 清理上次的 latest 文件
rm -f "$LATEST_FILE"

echo ">>> 开始执行资源诊断脚本..."
echo ""

# 执行 SQL 脚本（SPOOL 在 SQL 内部写入 latest 文件）
sql 'yladmin/ggcjd4slhtjyx!'@10.119.254.69:1521/yldb @"$SCRIPT_DIR/resource_hog_sql.sql"

# 执行完成后，重命名加时间戳
if [ -f "$LATEST_FILE" ] && [ -s "$LATEST_FILE" ]; then
    cp "$LATEST_FILE" "$OUTPUT_FILE"
    echo ""
    echo ">>> 诊断完成，结果已保存到:"
    echo "    $OUTPUT_FILE"
else
    echo ""
    echo ">>> 警告: 输出文件为空或不存在，请检查数据库连接"
fi
