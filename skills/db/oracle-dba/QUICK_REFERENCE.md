# Oracle DBA工具 - 快速参考卡

## 🎯 一句话描述
Oracle数据库性能诊断、SQL优化、健康检查的完整工具集

## 📦 包含内容

### SQL脚本（scripts/）
```bash
health_check.sql     # 综合健康检查（14项检查）
top_sql.sql          # TOP SQL分析（6个维度）
lock_tree.sql        # 锁等待树分析
slow_sql_analysis.sql # 慢SQL分析（新增）
analyze_slow_sql.sh   # 慢SQL分析Shell版（新增）
generate_awr.sql     # AWR报告生成（SQL）
generate_awr.sh      # AWR报告生成（Shell）
```

### Python工具（scripts/）
```bash
awr_analyzer.py      # AWR报告自动分析
```

### 参考文档（references/）
```
awr_guide.md         # AWR报告解读完整指南（400+行）
```

### 案例示例（examples/）
```
case_full_scan.md    # 全表扫描优化实战案例
```

## ⚡ 快速使用

### 方式1：在Qoder中对话
```
"帮我分析这个SQL为什么慢"
"检查数据库健康状态"
"数据库有锁等待怎么办"
"表空间使用率超过80%"
```

### 方式2：直接运行脚本
```bash
# 健康检查
sqlplus dba/pass@db @scripts/health_check.sql

# TOP SQL分析
sqlplus dba/pass@db @scripts/top_sql.sql

# 锁分析
sqlplus dba/pass@db @scripts/lock_tree.sql

# 生成AWR报告（交互式）
./scripts/generate_awr.sh

# 生成AWR报告（命令行）
./scripts/generate_awr.sh -u system -p oracle -c localhost:1521/orcl -b 100 -e 110

# AWR分析
python scripts/awr_analyzer.py awr_report.html
```

## 🔍 典型场景速查

| 问题 | 使用方法 | 关键指标 |
|-----|---------|---------|
| **数据库慢** | health_check.sql | TOP等待事件、活动会话 |
| **SQL慢** | top_sql.sql | Gets per Exec、执行计划 |
| **慢SQL分析** | slow_sql_analysis.sql | 平均执行时间、全表扫描 |
| **锁等待** | lock_tree.sql | 阻塞树、持锁时间 |
| **空间满** | health_check.sql | 表空间使用率 |
| **生成AWR报告** | generate_awr.sh | 快照范围、报告格式 |
| **性能趋势** | awr_analyzer.py | DB Time、CPU比例 |

## 💊 常见问题速查

### SQL执行慢
```sql
-- 1. 查看执行计划
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id'));

-- 2. 检查是否全表扫描
--    看到 TABLE ACCESS FULL → 需要索引

-- 3. 检查统计信息
SELECT table_name, last_analyzed, num_rows
FROM dba_tables WHERE table_name = 'XXX';

-- 4. 检查索引
SELECT index_name, column_name FROM dba_ind_columns
WHERE table_name = 'XXX';
```

### 表空间告警
```sql
-- 扩容
ALTER DATABASE DATAFILE '/path/to/file.dbf' RESIZE 20G;

-- 或添加数据文件
ALTER TABLESPACE users ADD DATAFILE '/path/to/new.dbf' SIZE 10G;
```

### 锁等待
```sql
-- 查看阻塞会话
SELECT blocking_session, sid, username, event
FROM v$session WHERE blocking_session IS NOT NULL;

-- 终止会话（谨慎！）
ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;
```

### 慢SQL分析（新增）
```bash
# 交互式SQL分析
sql user/pass@db @scripts/slow_sql_analysis.sql

# Shell脚本分析（自动输出报告）
./scripts/analyze_slow_sql.sh "Fssc%"

# 分析特定模块
./scripts/analyze_slow_sql.sh "FsscClaim%" slow_claim_report.txt
```

## 📊 关键阈值参考

| 指标 | 正常 | 注意 | 告警 |
|-----|------|------|------|
| 表空间使用率 | <70% | 70-80% | >80% |
| Buffer Hit Ratio | >95% | 90-95% | <90% |
| Soft Parse Ratio | >95% | 80-95% | <80% |
| CPU/DB Time | >50% | 30-50% | <30% |
| Gets per Exec | <10K | 10K-100K | >100K |

## 🎓 学习路径

### 入门（1-2周）
1. 阅读 [AWR报告解读指南](references/awr_guide.md)
2. 学习基本SQL：执行计划、等待事件
3. 跑一遍所有脚本熟悉输出

### 进阶（1个月）
1. 分析实际案例：[全表扫描优化](examples/case_full_scan.md)
2. 建立性能基线
3. 掌握索引设计原则

### 精通（持续）
1. 深入理解Oracle内部原理
2. 熟练使用10046 trace、ASH
3. 系统级优化（OS、存储、网络）

## 🚨 安全提醒

### ⚠️ 高风险操作
- KILL SESSION（终止会话）
- FLUSH SHARED_POOL（清空缓存）
- DROP INDEX（删除索引）
- ALTER SYSTEM（修改参数）

### ✅ 安全操作
- SELECT 查询（只读）
- EXPLAIN PLAN（分析执行计划）
- 查看视图（V$, DBA_*）

### 💡 最佳实践
1. 生产环境先在测试环境验证
2. 高峰期只做查询不做修改
3. 记录操作日志便于回滚
4. 重大操作前做好备份

## 📞 紧急情况处理

### 数据库宕机
```
1. 检查Alert Log
2. 检查监听器状态
3. 尝试启动数据库
4. 联系DBA团队
```

### 性能突然下降
```
1. 运行 health_check.sql 快速诊断
2. 查看当前等待事件
3. 识别异常SQL
4. 查看系统资源（CPU/内存/I/O）
5. 对比历史AWR基线
```

### 表空间满
```
1. 立即扩容（紧急）
   ALTER DATABASE DATAFILE '...' RESIZE +10G;

2. 分析增长原因（后续）
   - 大量插入？
   - 未归档数据？
   - 临时表膨胀？
```

## 📚 扩展资源

### 官方文档
- Oracle Performance Tuning Guide
- Oracle Database Reference（V$视图说明）
- Oracle Database SQL Language Reference

### 推荐书籍
- 《Oracle性能诊断艺术》
- 《基于Oracle的SQL优化》
- 《Oracle DBA手记》系列

### 在线资源
- Oracle Support (MOS)
- AskTom
- Oracle-Base.com

## 🎯 Skill功能清单

### ✅ 已实现
- [x] 健康检查（14项）
- [x] TOP SQL分析（6维度）
- [x] 锁等待分析
- [x] AWR报告生成（SQL + Shell）
- [x] AWR自动分析
- [x] AWR解读指南
- [x] 实战案例1个

### 🚧 待扩展
- [ ] 更多案例（索引选择性、执行计划突变等）
- [ ] 更多脚本（表空间报告、会话监控等）
- [ ] 索引失效12种场景详解
- [ ] RMAN备份恢复完整手册
- [ ] 执行计划深度解读

---

**版本**: 1.0  
**更新**: 2025-02-28  
**作者**: sevenxiao  
**适用**: Oracle 11g/12c/19c/21c
