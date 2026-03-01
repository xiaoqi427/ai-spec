# AWR报告生成 - 使用示例

## 快速开始

### 1. 交互式生成（推荐新手）

最简单的方式，脚本会自动引导你完成所有步骤：

```bash
./scripts/generate_awr.sh
```

**步骤说明**：
1. 输入数据库用户名（如：system）
2. 输入密码
3. 输入连接串（如：localhost:1521/orcl）
4. 查看最近20个快照列表
5. 输入开始快照ID和结束快照ID
6. 等待报告生成完成

**示例输出**：
```
================================================================================
                    Oracle AWR报告生成工具
================================================================================

数据库用户名: system
数据库密码: ****
数据库连接串 (如: localhost:1521/orcl): prod:1521/orcl

测试数据库连接...
✓ 数据库连接成功

最近20个AWR快照:
Snap ID  开始时间              结束时间              持续时间
------- ------------------- ------------------- ----------
    110 2025-02-28 10:00    2025-02-28 11:00    01:00
    109 2025-02-28 09:00    2025-02-28 10:00    01:00
    108 2025-02-28 08:00    2025-02-28 09:00    01:00
    ...

输入开始快照ID: 108
输入结束快照ID: 110

正在生成AWR报告...
  开始快照: 108
  结束快照: 110
  报告格式: html
  输出文件: awr_ORCL_108_110_20250228_143022.html

✓ AWR报告生成成功!
  文件路径: /current/dir/awr_ORCL_108_110_20250228_143022.html
  文件大小: 2.3M

================================================================================
下一步操作:
  1. 查看报告:
     open awr_ORCL_108_110_20250228_143022.html  (Mac)
  2. 分析报告:
     python3 scripts/awr_analyzer.py awr_ORCL_108_110_20250228_143022.html
================================================================================
```

---

### 2. 命令行模式（推荐熟练用户）

适合写到监控脚本或自动化任务中：

```bash
./scripts/generate_awr.sh \
  -u system \
  -p oracle \
  -c prod:1521/orcl \
  -b 108 \
  -e 110
```

**参数说明**：
- `-u`: 数据库用户名
- `-p`: 数据库密码
- `-c`: 数据库连接串
- `-b`: 开始快照ID
- `-e`: 结束快照ID

---

### 3. 生成并自动分析

生成HTML报告后立即进行自动分析：

```bash
./scripts/generate_awr.sh \
  -u system \
  -p oracle \
  -c prod:1521/orcl \
  -b 108 \
  -e 110 \
  -a
```

**效果**：
- 生成AWR HTML报告
- 自动调用Python分析工具
- 输出关键指标和优化建议

---

### 4. 生成TEXT格式

适合通过邮件或日志查看：

```bash
./scripts/generate_awr.sh \
  -u system \
  -p oracle \
  -c prod:1521/orcl \
  -b 108 \
  -e 110 \
  -t text
```

**优点**：
- 文件更小（通常100-200KB）
- 便于grep搜索
- 适合邮件附件

---

### 5. 指定输出目录

将报告保存到指定位置：

```bash
./scripts/generate_awr.sh \
  -u system \
  -p oracle \
  -c prod:1521/orcl \
  -b 108 \
  -e 110 \
  -o /data/awr_reports/$(date +%Y%m)
```

**用途**：
- 按月归档AWR报告
- 统一管理历史报告
- 便于批量分析

---

## 高级用法

### 定时生成每日AWR报告

创建cron任务每天早上生成昨天的AWR报告：

```bash
# 添加到crontab
0 8 * * * /path/to/generate_awr.sh \
  -u system \
  -p oracle \
  -c prod:1521/orcl \
  -b $(date -d "yesterday 08:00" +\%s) \
  -e $(date -d "today 08:00" +\%s) \
  -o /data/awr_reports/$(date +\%Y\%m) \
  -a \
  >> /var/log/awr_daily.log 2>&1
```

---

### 批量生成历史报告

生成过去一周的每日AWR报告：

```bash
#!/bin/bash
# batch_generate_awr.sh

for i in {1..7}; do
    DATE=$(date -d "$i days ago" +%Y%m%d)
    
    # 计算快照ID（假设每小时一个快照）
    BEGIN_SNAP=$((1000 - i * 24))
    END_SNAP=$((BEGIN_SNAP + 24))
    
    echo "生成 $DATE 的AWR报告 (Snap: $BEGIN_SNAP-$END_SNAP)"
    
    ./scripts/generate_awr.sh \
      -u system \
      -p oracle \
      -c prod:1521/orcl \
      -b $BEGIN_SNAP \
      -e $END_SNAP \
      -o /data/awr_reports/${DATE:0:6}
done
```

---

### 性能对比分析

生成两个时间段的AWR报告进行对比：

```bash
# 高峰期报告（10:00-12:00）
./scripts/generate_awr.sh \
  -u system -p oracle -c prod:1521/orcl \
  -b 110 -e 112 \
  -o /tmp/compare \
  -a > peak_analysis.txt

# 低峰期报告（02:00-04:00）
./scripts/generate_awr.sh \
  -u system -p oracle -c prod:1521/orcl \
  -b 102 -e 104 \
  -o /tmp/compare \
  -a > offpeak_analysis.txt

# 对比两个报告
diff peak_analysis.txt offpeak_analysis.txt
```

---

## 常见问题

### Q1: 提示"无法连接到数据库"

**检查项**：
1. 数据库监听器是否启动
2. 用户名密码是否正确
3. 连接串格式是否正确（host:port/service_name）
4. 网络是否可达

**测试命令**：
```bash
sqlplus system/oracle@prod:1521/orcl
```

---

### Q2: 提示"快照不存在"

**原因**：
- 输入的快照ID不存在
- 快照已被清理

**解决**：
1. 运行交互式模式查看可用快照
2. 或查询快照表：
```sql
SELECT snap_id, begin_interval_time 
FROM dba_hist_snapshot 
ORDER BY snap_id DESC 
FETCH FIRST 20 ROWS ONLY;
```

---

### Q3: 报告生成很慢

**正常情况**：
- 跨度大的报告（如24小时）需要3-5分钟
- 繁忙系统的报告会更大

**加速技巧**：
- 缩小快照范围（如只生成2小时）
- 使用TEXT格式而非HTML
- 避免在高峰期生成

---

### Q4: 没有权限生成AWR报告

**错误信息**：
```
ORA-20200: Insufficient privileges
```

**解决方案**：
```sql
-- 授予AWR相关权限
GRANT SELECT_CATALOG_ROLE TO your_user;
GRANT EXECUTE ON DBMS_WORKLOAD_REPOSITORY TO your_user;
```

或使用有DBA权限的用户（如system）。

---

### Q5: 报告文件太大无法打开

**情况**：
- 跨度24小时的HTML报告可能达到10MB+
- 浏览器可能卡顿

**解决方案**：
1. 使用TEXT格式：
```bash
./scripts/generate_awr.sh ... -t text
```

2. 或缩小快照范围：
```bash
# 只生成2小时的报告
./scripts/generate_awr.sh ... -b 108 -e 110
```

3. 使用Python分析工具直接提取关键信息：
```bash
python scripts/awr_analyzer.py large_awr.html -o summary.txt
```

---

## 参考资料

- [AWR报告解读指南](../references/awr_guide.md)
- [健康检查脚本](health_check.sql)
- [TOP SQL分析](top_sql.sql)
- [全表扫描优化案例](../examples/case_full_scan.md)

---

**提示**：如果还有问题，可以在Qoder中直接询问：

```
"生成AWR报告时遇到XXX错误"
"如何生成过去24小时的AWR报告"
"AWR报告太大怎么办"
```
