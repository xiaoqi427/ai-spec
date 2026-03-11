#!/bin/bash
# ============================================================
# 快速方法搜索: 在新老代码中搜索指定方法名/关键词
# 用法: bash quick-search.sh <关键词> [old|new|all]
# ============================================================

KEYWORD="${1:?用法: bash quick-search.sh <关键词> [old|new|all]}"
SCOPE="${2:-all}"

OLD_BASE="yldc-caiwugongxiangpingtai-fsscYR-master/src"
NEW_BASE="fssc-claim-service"

search_old() {
    echo "=========================================="
    echo "🔍 老代码搜索: ${KEYWORD}"
    echo "=========================================="
    grep -rn --include="*.java" "${KEYWORD}" "${OLD_BASE}" 2>/dev/null | head -30
    echo ""
    count=$(grep -rl --include="*.java" "${KEYWORD}" "${OLD_BASE}" 2>/dev/null | wc -l | tr -d ' ')
    echo "共 ${count} 个文件命中"
}

search_new() {
    echo "=========================================="
    echo "🔍 新代码搜索: ${KEYWORD}"
    echo "=========================================="
    grep -rn --include="*.java" "${KEYWORD}" "${NEW_BASE}" 2>/dev/null | head -30
    echo ""
    count=$(grep -rl --include="*.java" "${KEYWORD}" "${NEW_BASE}" 2>/dev/null | wc -l | tr -d ' ')
    echo "共 ${count} 个文件命中"
}

case "${SCOPE}" in
    old)  search_old ;;
    new)  search_new ;;
    all)  search_old; echo ""; search_new ;;
    *)    echo "❌ 无效范围: ${SCOPE}  (可选: old / new / all)" ;;
esac
