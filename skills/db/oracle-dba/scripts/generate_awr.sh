#!/bin/bash
################################################################################
# AWR报告生成Shell脚本
# 功能: 快速生成AWR报告（支持交互式和非交互式）
# 作者: sevenxiao
# 日期: 2025-02-28
# 用法: ./generate_awr.sh [options]
################################################################################

# 设置 Java 21 环境
export JAVA_HOME=/Users/xiaoqi/Library/Java/JavaVirtualMachines/corretto-21.0.9/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 默认值
REPORT_TYPE="html"
DB_USER=""
DB_PASS=""
DB_CONN=""
BEGIN_SNAP=""
END_SNAP=""
OUTPUT_DIR="."
AUTO_ANALYZE=false

# 打印使用说明
usage() {
    cat << EOF
用法: $0 [选项]

AWR报告生成工具 - 支持交互式和命令行模式

选项:
    -u, --user USER         数据库用户名
    -p, --password PASS     数据库密码
    -c, --connect CONN      数据库连接串 (如: localhost:1521/orcl)
    -b, --begin SNAP_ID     开始快照ID
    -e, --end SNAP_ID       结束快照ID
    -t, --type TYPE         报告类型 [html|text] (默认: html)
    -o, --output DIR        输出目录 (默认: 当前目录)
    -a, --analyze           生成后自动分析报告
    -h, --help              显示此帮助信息

示例:
    # 交互式模式
    $0

    # 命令行模式
    $0 -u system -p oracle -c localhost:1521/orcl -b 100 -e 110

    # 生成TEXT格式并自动分析
    $0 -u system -p oracle -c localhost:1521/orcl -b 100 -e 110 -t text -a

    # 指定输出目录
    $0 -u system -p oracle -c localhost:1521/orcl -b 100 -e 110 -o /tmp/awr_reports

EOF
    exit 1
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--user)
            DB_USER="$2"
            shift 2
            ;;
        -p|--password)
            DB_PASS="$2"
            shift 2
            ;;
        -c|--connect)
            DB_CONN="$2"
            shift 2
            ;;
        -b|--begin)
            BEGIN_SNAP="$2"
            shift 2
            ;;
        -e|--end)
            END_SNAP="$2"
            shift 2
            ;;
        -t|--type)
            REPORT_TYPE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -a|--analyze)
            AUTO_ANALYZE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}错误: 未知参数 '$1'${NC}"
            usage
            ;;
    esac
done

# 打印标题
echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}                    Oracle AWR报告生成工具${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

# 检查SQLcl是否安装
if ! command -v sql &> /dev/null; then
    echo -e "${RED}错误: 未找到SQLcl命令${NC}"
    echo "请确保已安装SQLcl并添加到PATH环境变量"
    echo "下载地址: https://www.oracle.com/database/sqldeveloper/technologies/sqlcl/"
    exit 1
fi

# 交互式输入（如果未通过参数提供）
if [[ -z "$DB_USER" ]]; then
    read -p "数据库用户名: " DB_USER
fi

if [[ -z "$DB_PASS" ]]; then
    read -sp "数据库密码: " DB_PASS
    echo ""
fi

if [[ -z "$DB_CONN" ]]; then
    read -p "数据库连接串 (如: localhost:1521/orcl): " DB_CONN
fi

# 构建连接字符串
CONNECTION="${DB_USER}/${DB_PASS}@${DB_CONN}"

# 测试数据库连接
echo -e "\n${YELLOW}测试数据库连接...${NC}"
TEST_RESULT=$(sql -S "$CONNECTION" <<EOF
SET HEADING OFF
SET FEEDBACK OFF
SET PAGESIZE 0
SELECT 'CONNECTION_OK' FROM dual;
EXIT;
EOF
)

if [[ ! "$TEST_RESULT" =~ "CONNECTION_OK" ]]; then
    echo -e "${RED}错误: 无法连接到数据库${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 数据库连接成功${NC}"

# 如果未提供快照ID，显示最近的快照
if [[ -z "$BEGIN_SNAP" ]] || [[ -z "$END_SNAP" ]]; then
    echo -e "\n${YELLOW}最近20个AWR快照:${NC}"
    sql -S "$CONNECTION" <<EOF
SET PAGESIZE 100
SET LINESIZE 120
COLUMN snap_id FORMAT 99999 HEADING "Snap ID"
COLUMN begin_time FORMAT A20 HEADING "开始时间"
COLUMN end_time FORMAT A20 HEADING "结束时间"
COLUMN duration FORMAT A10 HEADING "持续时间"

SELECT 
    snap_id,
    TO_CHAR(begin_interval_time, 'YYYY-MM-DD HH24:MI') AS begin_time,
    TO_CHAR(end_interval_time, 'YYYY-MM-DD HH24:MI') AS end_time,
    LPAD(EXTRACT(HOUR FROM (end_interval_time - begin_interval_time)), 2, '0') || ':' ||
    LPAD(EXTRACT(MINUTE FROM (end_interval_time - begin_interval_time)), 2, '0') AS duration
FROM 
    dba_hist_snapshot
WHERE 
    instance_number = (SELECT instance_number FROM v\$instance)
ORDER BY 
    snap_id DESC
FETCH FIRST 20 ROWS ONLY;
EXIT;
EOF

    if [[ -z "$BEGIN_SNAP" ]]; then
        read -p "输入开始快照ID: " BEGIN_SNAP
    fi

    if [[ -z "$END_SNAP" ]]; then
        read -p "输入结束快照ID: " END_SNAP
    fi
fi

# 验证快照ID
if [[ ! "$BEGIN_SNAP" =~ ^[0-9]+$ ]] || [[ ! "$END_SNAP" =~ ^[0-9]+$ ]]; then
    echo -e "${RED}错误: 快照ID必须是数字${NC}"
    exit 1
fi

if [[ "$BEGIN_SNAP" -ge "$END_SNAP" ]]; then
    echo -e "${RED}错误: 开始快照ID必须小于结束快照ID${NC}"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR" || exit 1

# 生成报告文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
INSTANCE_NAME=$(sql -S "$CONNECTION" <<EOF | grep -v "^$" | tail -1
SET HEADING OFF
SET FEEDBACK OFF
SET PAGESIZE 0
SELECT instance_name FROM v\$instance;
EXIT;
EOF
)
INSTANCE_NAME=$(echo "$INSTANCE_NAME" | tr -d '[:space:]')

if [[ "$REPORT_TYPE" == "text" ]]; then
    REPORT_FILE="awr_${INSTANCE_NAME}_${BEGIN_SNAP}_${END_SNAP}_${TIMESTAMP}.txt"
else
    REPORT_FILE="awr_${INSTANCE_NAME}_${BEGIN_SNAP}_${END_SNAP}_${TIMESTAMP}.html"
fi

# 生成AWR报告
echo -e "\n${YELLOW}正在生成AWR报告...${NC}"
echo "  开始快照: $BEGIN_SNAP"
echo "  结束快照: $END_SNAP"
echo "  报告格式: $REPORT_TYPE"
echo "  输出文件: $REPORT_FILE"

sql -S "$CONNECTION" <<EOF > "$REPORT_FILE"
SET ECHO OFF
SET FEEDBACK OFF
SET HEADING OFF
SET PAGESIZE 0
SET LINESIZE 32767
SET LONG 1000000
SET LONGCHUNKSIZE 1000000
SET TRIMSPOOL ON

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

# 检查报告是否生成成功
if [[ -f "$REPORT_FILE" ]] && [[ -s "$REPORT_FILE" ]]; then
    FILE_SIZE=$(du -h "$REPORT_FILE" | cut -f1)
    echo -e "${GREEN}✓ AWR报告生成成功!${NC}"
    echo "  文件路径: $(pwd)/$REPORT_FILE"
    echo "  文件大小: $FILE_SIZE"
    
    # 自动分析报告（如果启用）
    if [[ "$AUTO_ANALYZE" == true ]]; then
        echo -e "\n${YELLOW}正在分析AWR报告...${NC}"
        
        if [[ -f "$SCRIPT_DIR/awr_analyzer.py" ]]; then
            python3 "$SCRIPT_DIR/awr_analyzer.py" "$REPORT_FILE"
        else
            echo -e "${YELLOW}警告: 未找到awr_analyzer.py脚本${NC}"
        fi
    fi
    
    # 后续操作提示
    echo -e "\n${BLUE}================================================================================${NC}"
    echo -e "${BLUE}下一步操作:${NC}"
    echo "  1. 查看报告:"
    if [[ "$REPORT_TYPE" == "html" ]]; then
        echo "     open $REPORT_FILE  (Mac)"
        echo "     xdg-open $REPORT_FILE  (Linux)"
    else
        echo "     cat $REPORT_FILE | less"
    fi
    echo "  2. 分析报告:"
    echo "     python3 $SCRIPT_DIR/awr_analyzer.py $REPORT_FILE"
    echo "  3. 参考指南:"
    echo "     cat $SCRIPT_DIR/../references/awr_guide.md"
    echo -e "${BLUE}================================================================================${NC}"
else
    echo -e "${RED}✗ AWR报告生成失败${NC}"
    exit 1
fi
