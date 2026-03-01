#!/bin/bash
export JAVA_HOME=/Users/xiaoqi/Library/Java/JavaVirtualMachines/corretto-21.0.9/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

cd /Users/xiaoqi/Documents/work/yili/ai-spec/skills/db/oracle-dba/scripts

echo "开始生成AWR报告..."
bash quick_awr.sh 59627 59628 html
