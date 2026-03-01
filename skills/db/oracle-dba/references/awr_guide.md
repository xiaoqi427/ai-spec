# AWR报告解读完整指南

## 概述

AWR (Automatic Workload Repository) 是Oracle数据库自动性能诊断的核心工具，记录了数据库的性能统计信息。

## AWR报告关键部分解读

### 1. Report Summary（报告摘要）

#### DB Time
- **定义**: 数据库在前台会话上花费的总时间（不包括后台进程）
- **单位**: 通常以分钟或秒显示
- **意义**: 反映数据库的整体工作负载
- **优化目标**: 减少DB Time

**分析方法**:
```
DB Time = DB CPU + Wait Time
```

如果 DB Time = 100分钟，实际时钟时间 = 60分钟
说明: 平均有 100/60 ≈ 1.67 个并发会话在工作

#### DB CPU
- **定义**: CPU实际执行时间
- **理想比例**: DB CPU / DB Time > 50%
- **如果过低**: 说明大量时间在等待，需要分析等待事件
- **如果过高**: 说明CPU密集，需要优化SQL执行效率

### 2. Load Profile（负载概况）

关键指标解读：

| 指标 | 说明 | 正常范围 | 告警阈值 |
|-----|------|---------|---------|
| **Redo size** | 每秒生成的重做日志量 | < 10MB/s | > 50MB/s |
| **Logical reads** | 每秒逻辑读（buffer gets） | 依业务而定 | 突增50%+ |
| **Physical reads** | 每秒物理读 | < 逻辑读的10% | > 逻辑读的30% |
| **Executions** | 每秒SQL执行次数 | 依业务而定 | 突增50%+ |
| **Transactions** | 每秒事务数 | 依业务而定 | - |
| **Logons** | 每秒登录数 | < 10 | > 100 |

**分析示例**:
```
Per Second    Per Transaction
-----------   ---------------
Redo size:       2,345,678        456,789

解读: 
- 每秒生成约2.3MB重做日志（适中）
- 每个事务生成约450KB重做日志（需关注大事务）
```

### 3. Instance Efficiency（实例效率）

关键比率解读：

#### Buffer Cache Hit Ratio（缓冲区命中率）
```
公式: (1 - Physical Reads / Logical Reads) * 100%
```
- **理想值**: > 95%
- **警告**: < 90%
- **严重**: < 80%

**如果过低**:
- 增加 `db_cache_size`
- 检查是否有大量全表扫描
- 检查是否有不合理的SQL

#### Library Cache Hit Ratio（库缓存命中率）
```
公式: (1 - Parse Count / Execute Count) * 100%
```
- **理想值**: > 95%
- **警告**: < 90%

**如果过低**:
- 使用绑定变量减少硬解析
- 增加 `shared_pool_size`
- 检查是否有动态SQL

#### Soft Parse Ratio（软解析比例）
```
公式: (Soft Parses / Total Parses) * 100%
```
- **理想值**: > 95%
- **警告**: < 80%

**如果过低**:
- 强烈建议使用绑定变量
- 检查应用是否大量使用字面值SQL

### 4. Top 5 Timed Events（Top等待事件）

#### 常见等待事件及含义

**1. db file sequential read**
- **含义**: 单块读，通常是索引扫描
- **可能原因**:
  - 索引范围扫描过多
  - 索引碎片化
  - 存储I/O慢
- **优化方向**:
  - 检查是否可以用覆盖索引
  - 考虑分区
  - 优化存储

**2. db file scattered read**
- **含义**: 多块读，通常是全表扫描
- **可能原因**:
  - 缺少索引
  - 索引失效（函数、类型转换）
  - 统计信息陈旧导致执行计划错误
- **优化方向**:
  - 添加合适的索引
  - 检查SQL执行计划
  - 更新统计信息

**3. log file sync**
- **含义**: 等待LGWR写重做日志完成（通常是COMMIT）
- **可能原因**:
  - 频繁COMMIT
  - 日志文件存储I/O慢
  - 重做日志文件太小
- **优化方向**:
  - 批量COMMIT而非逐条
  - 使用更快的存储设备存放重做日志
  - 增大重做日志文件大小

**4. log file parallel write**
- **含义**: LGWR进程写重做日志
- **可能原因**:
  - 大量DML操作
  - 日志文件I/O慢
- **优化方向**:
  - 重做日志文件放到最快的存储上
  - 使用多个重做日志组
  - 考虑使用SSD

**5. enq: TX - row lock contention**
- **含义**: 行锁争用
- **可能原因**:
  - 多个会话更新同一行
  - 事务时间过长
  - 热点数据
- **优化方向**:
  - 缩短事务时间
  - 避免在事务中进行长时间操作
  - 考虑业务逻辑优化

**6. latch: cache buffers chains**
- **含义**: Buffer cache争用
- **可能原因**:
  - 热点块（hot block）
  - 不合理的索引设计
- **优化方向**:
  - 使用分区减少热点
  - 使用反向索引（reverse key index）

**7. CPU time**
- **含义**: 不是等待，而是CPU执行时间
- **如果占比高**: 说明主要是CPU密集型操作
- **优化方向**:
  - 优化SQL执行效率
  - 减少逻辑读
  - 检查是否有大量计算

### 5. SQL Statistics（SQL统计）

#### SQL ordered by Elapsed Time（按总耗时排序）
- **关注**: 占用DB Time比例高的SQL
- **优化**: 即使单次快，累计时间多的也需要优化

#### SQL ordered by CPU Time（按CPU时间排序）
- **关注**: CPU密集型SQL
- **优化**: 减少逻辑读、优化算法

#### SQL ordered by Gets（按逻辑读排序）
- **关注**: Buffer gets最多的SQL
- **优化**: 通常是全表扫描，需要添加索引

#### SQL ordered by Reads（按物理读排序）
- **关注**: Disk reads最多的SQL
- **优化**: 可能需要增加buffer cache或优化SQL

#### SQL ordered by Executions（按执行次数排序）
- **关注**: 高频SQL
- **优化**: 即使单次很快，高频执行累计影响大

### 6. 分析SQL的关键指标

| 指标 | 含义 | 优化目标 |
|-----|------|---------|
| **Executions** | 执行次数 | - |
| **Elapsed Time** | 总耗时 | 降低 |
| **CPU Time** | CPU时间 | CPU/Elapsed > 50% |
| **Buffer Gets** | 逻辑读 | 降低 |
| **Disk Reads** | 物理读 | Disk/Buffer < 10% |
| **Rows Processed** | 返回行数 | - |
| **Gets per Exec** | 单次逻辑读 | < 10,000 |
| **Rows per Exec** | 单次返回行 | - |
| **Gets per Row** | 每行逻辑读 | < 100 |

**分析示例**:
```
SQL_ID: 9babjv8yq8ru3
Elapsed Time: 1,234.56s (占DB Time的 15.3%)
CPU Time:     987.65s (占Elapsed的 80%)
Buffer Gets:  123,456,789
Disk Reads:   1,234,567 (占Gets的 1%)
Executions:   10,000
Rows:         50,000

单次分析:
- Gets per Exec = 123,456,789 / 10,000 = 12,346 (适中)
- Rows per Exec = 50,000 / 10,000 = 5 (很少)
- Gets per Row = 123,456,789 / 50,000 = 2,469 (偏高!)

结论: 每返回一行需要2400+次逻辑读，严重低效！
建议: 检查执行计划，可能是嵌套循环导致重复访问
```

## 分析流程

### 标准分析流程

```
1. 查看Report Summary
   ├─ 确定时间范围和负载级别
   └─ 记录DB Time和DB CPU

2. 分析Load Profile
   ├─ 识别异常指标（与历史基线对比）
   └─ 判断负载类型（OLTP/批处理/混合）

3. 查看Instance Efficiency
   ├─ Buffer Hit < 90%? → 检查物理读高的SQL
   ├─ Library Hit < 90%? → 检查硬解析
   └─ Soft Parse < 80%? → 必须使用绑定变量

4. 分析Top 5 Events
   ├─ CPU time占比 > 50%? → 优化SQL效率
   ├─ 等待事件占比 > 20%? → 针对性优化
   └─ 识别主要瓶颈（I/O/锁/解析等）

5. 检查Top SQL
   ├─ 按Elapsed Time → 找影响最大的SQL
   ├─ 按Gets → 找逻辑读高的SQL
   └─ 逐个分析执行计划

6. 深入分析
   ├─ Segment Statistics → 识别热点对象
   ├─ IOStat by Function → 分析I/O分布
   └─ Time Model Statistics → 时间分配

7. 制定优化方案
   ├─ 优先级: 影响大、容易改的
   ├─ 短期方案: SQL优化、索引调整
   └─ 长期方案: 架构调整、硬件升级
```

## 性能基线建立

### 为什么需要基线？

AWR报告的数值**本身没有绝对的好坏**，必须与基线对比：

- **历史基线**: 同一时间段的历史数据
- **正常基线**: 业务正常时的性能表现

### 建立基线步骤

1. **收集正常业务时段的AWR**
   ```sql
   -- 每周一上午10-11点的AWR
   SELECT snap_id, begin_interval_time
   FROM dba_hist_snapshot
   WHERE TO_CHAR(begin_interval_time, 'D') = '2'  -- 周一
     AND TO_CHAR(begin_interval_time, 'HH24') = '10'
   ORDER BY begin_interval_time DESC;
   ```

2. **提取关键指标建立基线表**
   ```sql
   CREATE TABLE perf_baseline AS
   SELECT 
     TRUNC(begin_time) stat_date,
     AVG(db_time) avg_db_time,
     AVG(db_cpu) avg_db_cpu,
     AVG(physical_reads) avg_physical_reads,
     AVG(logical_reads) avg_logical_reads
   FROM dba_hist_sysmetric_summary
   WHERE metric_name IN ('Database Time Per Sec', 
                         'CPU Usage Per Sec',
                         'Physical Reads Per Sec',
                         'Logical Reads Per Sec')
   GROUP BY TRUNC(begin_time);
   ```

3. **对比分析**
   ```sql
   -- 当前值 vs 基线
   SELECT 
     current.metric_value current_val,
     baseline.avg_value baseline_avg,
     ROUND((current.metric_value - baseline.avg_value) / 
           baseline.avg_value * 100, 2) deviation_pct
   FROM current_metrics current
   JOIN perf_baseline baseline 
     ON current.metric_name = baseline.metric_name;
   ```

## 常见问题诊断

### 问题1: 数据库突然变慢

**分析步骤**:
```
1. 对比当前AWR与历史基线
   → 找出变化最大的指标

2. 检查是否有新的Top SQL出现
   → 新SQL可能未优化

3. 检查执行计划是否改变
   → 统计信息陈旧？绑定变量窥探？

4. 检查系统资源
   → CPU/内存/I/O是否达到瓶颈？

5. 检查等待事件变化
   → 新出现的等待事件？
```

### 问题2: Buffer Hit Ratio偏低

**不要盲目增大buffer cache！**

**正确分析**:
```
1. 检查物理读高的SQL
   SELECT sql_id, disk_reads, buffer_gets
   FROM v$sql
   ORDER BY disk_reads DESC;

2. 分析这些SQL是否合理
   - 全表扫描？ → 加索引
   - 大表扫描？ → 考虑分区或改查询
   - 正常大数据量查询？ → 可以增大buffer cache

3. 检查是否有定时批处理
   - 批处理通常不需要缓存
   - 可以忽略批处理时段的命中率
```

### 问题3: 解析比例偏低

**根本原因: 未使用绑定变量**

**检查方法**:
```sql
-- 查找字面值SQL
SELECT sql_text, executions, version_count
FROM v$sql
WHERE executions > 0
  AND version_count > 10  -- 同一SQL有多个版本
ORDER BY version_count DESC;
```

**解决方案**:
- 应用层改造：使用PreparedStatement
- 临时缓解：设置 cursor_sharing=FORCE （不推荐）

## 总结

### AWR分析核心要点

1. **关注相对值而非绝对值**
   - 与历史基线对比
   - 关注趋势而非瞬时值

2. **自顶向下分析**
   - 先看整体（Load Profile、Top Events）
   - 再看细节（Top SQL、执行计划）

3. **抓主要矛盾**
   - 优先优化影响最大的（Top SQL）
   - 优先解决容易改的

4. **理解业务特点**
   - OLTP vs 批处理的正常指标不同
   - 业务高峰期的表现是正常的

5. **持续监控**
   - 建立性能基线
   - 定期生成和分析AWR
   - 趋势分析比点分析更重要

### 快速检查清单

```markdown
□ DB Time突增？
□ DB CPU占比异常？
□ Buffer Hit < 90%?
□ Soft Parse < 80%?
□ 新的Top Event?
□ 新的Top SQL?
□ 执行计划改变？
□ 统计信息陈旧？
□ 表空间使用率？
□ 归档日志增长？
```
