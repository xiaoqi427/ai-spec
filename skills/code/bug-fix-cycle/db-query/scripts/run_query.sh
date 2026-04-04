#!/bin/bash
# ============================================================================
# DB Query - 通用数据库查询脚本
# 功能: 连接 Oracle 执行 SQL 查询，结果自动保存带时间戳
# 使用:
#   ./run_query.sh "SELECT * FROM T_RMBS_CLAIM WHERE ROWNUM <= 5"
#   ./run_query.sh @scripts/common_queries.sql
#   ./run_query.sh --env sit "SELECT ..."
# 作者: sevenxiao
# 日期: 2026-04-04
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config/db-connection.yaml"
OUTPUT_DIR="$SKILL_DIR/output"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LATEST_FILE="$OUTPUT_DIR/query_latest.txt"
OUTPUT_FILE="$OUTPUT_DIR/query_${TIMESTAMP}.txt"

# 默认环境
ENV="local"

# ============================================================================
# 解析参数
# ============================================================================
usage() {
    echo "用法: $0 [--env <local|sit>] <SQL语句 | @SQL文件>"
    echo ""
    echo "参数:"
    echo "  --env <env>     指定环境 (local/sit)，默认 local"
    echo "  <SQL>           SQL 查询语句（字符串）"
    echo "  @<file>         SQL 文件路径"
    echo ""
    echo "示例:"
    echo "  $0 \"SELECT * FROM T_RMBS_CLAIM WHERE ROWNUM <= 5\""
    echo "  $0 @scripts/common_queries.sql"
    echo "  $0 --env sit \"SELECT * FROM SYS_USER WHERE ROWNUM <= 3\""
    exit 1
}

# 解析 --env 参数
while [[ "$1" == --* ]]; do
    case "$1" in
        --env)
            ENV="$2"
            shift 2
            ;;
        --help|-h)
            usage
            ;;
        *)
            echo "未知参数: $1"
            usage
            ;;
    esac
done

# 获取 SQL 输入
SQL_INPUT="$1"
if [ -z "$SQL_INPUT" ]; then
    echo "错误: 请提供 SQL 语句或 SQL 文件"
    usage
fi

# ============================================================================
# 读取连接配置
# ============================================================================
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 连接配置文件不存在: $CONFIG_FILE"
    echo "请先复制模板并填写密码:"
    echo "  cp $SKILL_DIR/config/db-connection.yaml.example $CONFIG_FILE"
    exit 1
fi

# 使用 python3 解析 YAML（避免安装额外依赖）
read_config() {
    local env="$1"
    local field="$2"
    python3 -c "
import yaml, sys
with open('$CONFIG_FILE') as f:
    cfg = yaml.safe_load(f)
env_cfg = cfg.get('environments', {}).get('$env', {})
print(env_cfg.get('$field', ''))
" 2>/dev/null
}

DB_HOST=$(read_config "$ENV" "host")
DB_PORT=$(read_config "$ENV" "port")
DB_SID=$(read_config "$ENV" "sid")
DB_USER=$(read_config "$ENV" "username")
DB_PASS=$(read_config "$ENV" "password")
DB_TOOL=$(read_config "$ENV" "tool")

if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ]; then
    echo "错误: 环境 '$ENV' 的连接信息不完整"
    echo "请检查配置文件: $CONFIG_FILE"
    exit 1
fi

# 默认使用 sql (SQLcl)
DB_TOOL="${DB_TOOL:-sql}"

# 构建连接字符串
CONN_STR="${DB_USER}/${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_SID}"

# ============================================================================
# 准备输出目录
# ============================================================================
mkdir -p "$OUTPUT_DIR"
rm -f "$LATEST_FILE"

echo ">>> 环境: $ENV ($DB_HOST:$DB_PORT/$DB_SID)"
echo ">>> 用户: $DB_USER"
echo ""

# ============================================================================
# 执行查询
# ============================================================================
if [[ "$SQL_INPUT" == @* ]]; then
    # 执行 SQL 文件
    SQL_FILE="${SQL_INPUT#@}"

    # 如果是相对路径，从 SKILL_DIR 解析
    if [[ ! "$SQL_FILE" == /* ]]; then
        SQL_FILE="$SKILL_DIR/$SQL_FILE"
    fi

    if [ ! -f "$SQL_FILE" ]; then
        echo "错误: SQL 文件不存在: $SQL_FILE"
        exit 1
    fi

    echo ">>> 执行 SQL 文件: $SQL_FILE"
    echo ""

    $DB_TOOL "$CONN_STR" @"$SQL_FILE"
else
    # 执行内联 SQL
    echo ">>> 执行 SQL: $SQL_INPUT"
    echo ""

    # 生成临时 SQL 文件
    TMP_SQL="/tmp/db_query_${TIMESTAMP}.sql"
    cat > "$TMP_SQL" << EOSQL
SET LINESIZE 300
SET PAGESIZE 1000
SET FEEDBACK ON
SET VERIFY OFF
SET LONG 10000
SET TRIMSPOOL ON
SET COLSEP ' | '

SPOOL $LATEST_FILE

PROMPT >>> 查询时间:
SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') query_time FROM dual;

PROMPT
PROMPT >>> 查询结果:
$SQL_INPUT;

SPOOL OFF
EXIT
EOSQL

    $DB_TOOL "$CONN_STR" @"$TMP_SQL"

    # 清理临时文件
    rm -f "$TMP_SQL"
fi

# ============================================================================
# 保存结果
# ============================================================================
if [ -f "$LATEST_FILE" ] && [ -s "$LATEST_FILE" ]; then
    cp "$LATEST_FILE" "$OUTPUT_FILE"
    echo ""
    echo ">>> 查询完成，结果已保存到:"
    echo "    $OUTPUT_FILE"
    echo ""
    echo ">>> 结果预览:"
    head -50 "$LATEST_FILE"
else
    echo ""
    echo ">>> 查询完成（结果可能为空或直接输出到终端）"
fi
