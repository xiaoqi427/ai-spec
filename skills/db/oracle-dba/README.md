# Oracle高级DBA工具集

## 📖 简介

这是一个为Oracle数据库管理员（DBA）设计的综合工具集，提供性能诊断、SQL优化、健康检查、备份恢复等专业能力。

## 🚀 快速开始

### 基本使用

在Qoder中，当你遇到Oracle数据库相关问题时，直接描述问题即可自动应用此skill：

```
"帮我分析这个慢SQL"
"检查数据库健康状态"
"这个表空间快满了怎么办"
```

### 使用诊断脚本

所有SQL脚本位于 `scripts/` 目录：

```bash
# 综合健康检查
sql user/pass@db @scripts/health_check.sql

# TOP SQL分析
sql user/pass@db @scripts/top_sql.sql

# 锁等待分析
sql user/pass@db @scripts/lock_tree.sql

# 生成AWR报告
sql user/pass@db @scripts/generate_awr.sql

# 慢SQL分析（新增）
sql user/pass@db @scripts/slow_sql_analysis.sql
```

### 生成AWR报告

#### 方式1: 使用SQL脚本（交互式）

```bash
# 进入数据库后执行
sql user/pass@db @scripts/generate_awr.sql

# 按提示输入:
# - 开始快照ID
# - 结束快照ID
# - 报告格式(html/text)
```

#### 方式2: 使用Shell脚本（推荐）

```bash
# 交互式模式
./scripts/generate_awr.sh

# 命令行模式
./scripts/generate_awr.sh -u system -p oracle -c localhost:1521/orcl -b 100 -e 110

# 生成HTML并自动分析
./scripts/generate_awr.sh -u system -p oracle -c localhost:1521/orcl -b 100 -e 110 -a

# 指定输出目录
./scripts/generate_awr.sh -u system -p oracle -c localhost:1521/orcl -b 100 -e 110 -o /tmp/awr_reports
```

### Python工具使用

```bash
# AWR报告分析
python scripts/awr_analyzer.py awr_report.html

# 生成分析报告到文件
python scripts/awr_analyzer.py awr_report.html -o analysis.txt
```

## 📂 目录结构

```
oracle-dba/
├── skill.md                    # Skill主文件（AI使用）
├── README.md                   # 本文件
├── scripts/                    # 可执行脚本
│   ├── health_check.sql        # 数据库健康检查
│   ├── top_sql.sql             # TOP SQL分析
│   ├── lock_tree.sql           # 锁等待分析
│   ├── slow_sql_analysis.sql   # 慢SQL分析（新增）
│   ├── analyze_slow_sql.sh     # 慢SQL分析Shell版（新增）
│   ├── generate_awr.sql        # AWR报告生成（SQL）
│   ├── generate_awr.sh         # AWR报告生成（Shell）
│   └── awr_analyzer.py         # AWR报告分析工具
├── references/                 # 参考文档
│   └── awr_guide.md            # AWR报告解读指南
└── examples/                   # 案例示例
    └── case_full_scan.md       # 全表扫描优化案例
```

## 🛠️ 功能特性

### 1. 性能诊断
- ✅ AWR报告分析与解读
- ✅ 等待事件分析
- ✅ Top SQL识别与分析
- ✅ 执行计划分析

### 2. SQL优化
- ✅ 执行计划解读
- ✅ 索引建议
- ✅ SQL改写建议
- ✅ 统计信息管理

### 3. 健康检查
- ✅ 表空间监控
- ✅ 会话监控
- ✅ 锁/死锁检测
- ✅ Alert Log分析

### 4. 备份恢复
- ✅ RMAN备份状态检查
- ✅ 归档日志监控
- ✅ 备份策略建议

## 📊 使用场景示例

### 场景1：发现慢查询

**问题**: 某个查询突然变慢

**使用方式**:
```
你: "这个SQL很慢，帮我分析一下：SELECT * FROM orders WHERE order_no = ?"

AI会:
1. 提供诊断SQL获取执行计划
2. 分析是否全表扫描
3. 检查索引情况
4. 给出优化建议
```

### 场景2：数据库健康检查

**问题**: 需要日常巡检

**使用方式**:
```bash
# 运行健康检查脚本
sql dba/pass@prod @scripts/health_check.sql > health_report.txt
```

**输出内容**:
- 数据库基本信息
- 表空间使用率（高亮告警）
- 归档日志生成情况
- 备份状态
- 会话统计
- TOP等待事件
- 当前锁等待
- 无效对象
- 陈旧统计信息
- Alert Log错误

### 场景3：锁等待问题

**问题**: 事务被阻塞

**使用方式**:
```
你: "数据库有锁等待，帮我查一下"

或直接运行:
sql dba/pass@prod @scripts/lock_tree.sql
```

**AI会**:
1. 显示锁等待树（阻塞链）
2. 识别顶级阻塞会话
3. 显示阻塞SQL和等待SQL
4. 提供kill session命令（供参考）

### 场景3.5：慢SQL分析（新增）

**问题**: 需要定位系统中执行最慢的SQL和全表扫描

**使用方式**:
```bash
# 交互式SQL分析
sql dba/pass@prod @scripts/slow_sql_analysis.sql
# 按提示输入模块名称（如: Fssc% 或 FsscClaim%）

# Shell脚本分析（自动输出报告）
./scripts/analyze_slow_sql.sh "Fssc%"

# 分析特定模块
./scripts/analyze_slow_sql.sh "FsscClaim%" slow_claim_20260228.txt
```

**AI会**:
1. 显示TOP 50慢SQL（按平均执行时间排序）
2. 显示TOP 50全表扫描SQL
3. 提供完整SQL文本（可选）
4. 统计性能汇总数据
5. 给出优化建议

### 场景4：AWR报告生成与分析

**问题**: 需要分析性能趋势或定位历史性能问题

**使用方式**:
```bash
# 方式1: 使用Shell脚本（推荐）
./scripts/generate_awr.sh -u dba -p pass -c prod:1521/orcl -b 100 -e 110 -a

# 方式2: 使用SQL脚本
sql dba/pass@prod @scripts/generate_awr.sql

# 生成后手动分析
python scripts/awr_analyzer.py awr_20250228.html
```

**AI会**:
1. 生成指定快照范围的AWR报告
2. 自动分析报告关键指标
3. 识别性能瓶颈
4. 提供优化建议

## 📚 参考文档

### AWR报告解读

详见 [references/awr_guide.md](references/awr_guide.md)

包含:
- AWR各部分详细解读
- 关键指标含义和阈值
- 常见等待事件及优化建议
- 分析流程和方法
- 性能基线建立

### 实际案例

详见 [examples/case_full_scan.md](examples/case_full_scan.md)

实际案例:
- 问题发现
- 诊断过程（详细步骤）
- 根本原因分析
- 优化方案及效果
- 经验总结

## ⚠️ 注意事项

### 权限要求

| 操作 | 所需权限 |
|-----|---------|
| 健康检查脚本 | SELECT_CATALOG_ROLE |
| AWR查询 | SELECT on DBA_HIST_* 视图 |
| 执行计划查询 | SELECT on V$SQL, V$SQL_PLAN |
| KILL SESSION | ALTER SYSTEM |
| RMAN操作 | SYSDBA |

### 安全警告

⚠️ **生产环境操作请谨慎**

1. **KILL SESSION** 会导致事务回滚
2. **FLUSH SHARED_POOL** 会清空SQL缓存，影响性能
3. **统计信息收集** 应在业务低峰期进行
4. **索引重建** 需要评估锁的影响

### License要求

部分功能需要Oracle诊断包授权:
- AWR报告生成
- ADDM分析
- SQL Tuning Advisor

如未授权，可使用:
- Statspack（免费的性能统计工具）
- V$视图直接查询
- 手动分析

## 🔧 环境要求

### SQL脚本
- Oracle 11g 或更高版本
- SQLcl（推荐）或 SQL*Plus

### Python工具
- Python 3.6+
- 无额外依赖（仅使用标准库）

## 💡 最佳实践

### 日常巡检

建议每天执行:
```bash
# 早上上班后执行健康检查
sql dba/pass@prod @scripts/health_check.sql | tee daily_check_$(date +%Y%m%d).log

# 检查关键指标
- 表空间使用率 > 80%
- 备份是否成功
- 是否有锁等待
- Alert Log是否有错误
```

### 性能问题诊断

标准流程:
```
1. 现象确认
   └─ 用户报告 or 监控告警

2. 快速定位
   ├─ 查看当前活动会话
   ├─ 查看TOP等待事件
   └─ 识别问题SQL

3. 深入分析
   ├─ 执行计划分析
   ├─ 统计信息检查
   └─ AWR历史数据

4. 优化实施
   ├─ SQL优化
   ├─ 索引调整
   └─ 参数优化

5. 效果验证
   └─ 对比优化前后指标
```

## 🤝 贡献指南

欢迎补充：
- 新的诊断脚本
- 优化案例
- 参考文档
- 工具改进

## 📝 更新日志

### 2025-02-28 - v1.0
- ✅ 初始版本发布
- ✅ 健康检查脚本
- ✅ TOP SQL分析脚本
- ✅ 锁等待分析脚本
- ✅ AWR分析工具（Python）
- ✅ AWR解读指南
- ✅ 全表扫描优化案例

## 📧 联系方式

作者: sevenxiao
适用项目: YILI财务共享服务中心
