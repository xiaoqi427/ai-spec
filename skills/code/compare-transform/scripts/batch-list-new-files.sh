#!/bin/bash
# ============================================================
# 批量对比脚本: 查找指定模板在新代码中的迁移文件
# 用法: bash batch-list-new-files.sh t044 otc
# 参数1: 模板编号（小写，如 t044）
# 参数2: 模块名（tr/ptp/otc/eer/fa/rtr）
# ============================================================

TEMPLATE_ID="${1:?用法: bash batch-list-new-files.sh <模板编号，如 t044> <模块名，如 otc>}"
MODULE="${2:?请指定模块名: tr/ptp/otc/eer/fa/rtr}"

# 新代码根路径
NEW_BASE="fssc-claim-service/claim-${MODULE}/claim-${MODULE}-service/src/main/java/com/yili/claim/${MODULE}/claim/${TEMPLATE_ID}"

echo "=========================================="
echo "新代码文件清单: ${TEMPLATE_ID} (${MODULE} 模块)"
echo "路径: ${NEW_BASE}/"
echo "=========================================="

if [ -d "${NEW_BASE}" ]; then
    echo ""
    echo "--- head/ (报账单头) ---"
    find "${NEW_BASE}/head" -name "*.java" 2>/dev/null | sort | while read -r f; do
        lines=$(wc -l < "$f" | tr -d ' ')
        echo "  ${f}  (${lines} 行)"
    done

    echo ""
    echo "--- line/ (报账单行) ---"
    find "${NEW_BASE}/line" -name "*.java" 2>/dev/null | sort | while read -r f; do
        lines=$(wc -l < "$f" | tr -d ' ')
        echo "  ${f}  (${lines} 行)"
    done

    echo ""
    echo "--- submit/ (提交) ---"
    find "${NEW_BASE}/submit" -name "*.java" 2>/dev/null | sort | while read -r f; do
        lines=$(wc -l < "$f" | tr -d ' ')
        echo "  ${f}  (${lines} 行)"
    done

    echo ""
    echo "--- callback/ (回调) ---"
    find "${NEW_BASE}/callback" -name "*.java" 2>/dev/null | sort | while read -r f; do
        lines=$(wc -l < "$f" | tr -d ' ')
        echo "  ${f}  (${lines} 行)"
    done

    echo ""
    total=$(find "${NEW_BASE}" -name "*.java" | wc -l | tr -d ' ')
    echo "共 ${total} 个文件"
else
    echo "❌ 目录不存在: ${NEW_BASE}"
    echo "提示: 可能该模板尚未迁移，或模块名/模板编号不正确"
fi
