#!/bin/bash
# ============================================================
# 批量对比脚本: 对指定模板的所有老代码文件列出清单
# 用法: bash batch-list-old-files.sh T044
# ============================================================

TEMPLATE_ID="${1:?用法: bash batch-list-old-files.sh <模板编号，如 T044>}"

# 老代码根路径
OLD_BASE="yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim"

# 查找老代码文件
echo "=========================================="
echo "老代码文件清单: ${TEMPLATE_ID}"
echo "路径: ${OLD_BASE}/${TEMPLATE_ID}/"
echo "=========================================="

if [ -d "${OLD_BASE}/${TEMPLATE_ID}" ]; then
    echo ""
    echo "--- Java 文件 ---"
    find "${OLD_BASE}/${TEMPLATE_ID}" -name "*.java" -not -path "*/gd/*" | sort | while read -r f; do
        lines=$(wc -l < "$f" | tr -d ' ')
        echo "  ${f}  (${lines} 行)"
    done

    echo ""
    echo "--- gd 前缀文件 (不迁移) ---"
    find "${OLD_BASE}/${TEMPLATE_ID}" -path "*/gd/*.java" | sort | while read -r f; do
        echo "  🔕 ${f}"
    done

    echo ""
    total=$(find "${OLD_BASE}/${TEMPLATE_ID}" -name "*.java" -not -path "*/gd/*" | wc -l | tr -d ' ')
    echo "共 ${total} 个需迁移文件"
else
    echo "❌ 目录不存在: ${OLD_BASE}/${TEMPLATE_ID}"
    echo "提示: 请确认模板编号是否正确（大写，如 T044）"
fi
