#!/bin/bash
# 快速测试慢SQL分析功能
cd /Users/xiaoqi/Documents/work/yili/ai-spec/skills/db/oracle-dba/scripts
bash analyze_slow_sql.sh "FsscClaim%" slow_sql_test_$(date +%Y%m%d_%H%M%S).txt
