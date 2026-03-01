---
name: yili-crud
description: 快速生成 YILI 财务共享服务中心项目的标准 CRUD 代码，基于 MyBatis-Plus 和多层架构设计。当用户需要生成增删改查代码、创建新模块的 CRUD 接口、生成标准 MyBatis-Plus CRUD 或创建新实体的完整调用链路时使用此技能。
---

# YILI CRUD 代码生成器

## 使用方式

### 完整生成（推荐）

```bash
# 生成某个表的完整 CRUD 代码（提供 DDL 文件）
/skill yili-crud <服务名> <模块名> --ddl <DDL文件路径>

# 生成某个表的完整 CRUD 代码（手动提供信息）
/skill yili-crud <服务名> <模块名> <实体名>
```

**示例**:
```bash
# 为 config 服务的 common 模块生成认证权限配置的 CRUD
/skill yili-crud config common TRmbsInvoiceAuthentication

# 为 config 服务生成，并提供 DDL 文件
/skill yili-crud config common --ddl ./T_RMBS_INVOICE_AUTHENTICATION.sql

# 为 claim-ptp 服务生成
/skill yili-crud claim.ptp rmbs TClaimRmbs

# 为 fund 服务生成
/skill yili-crud fund common TFundPayment
```

### 单层生成

```bash
# 只生成某一层的代码
/skill yili-crud <服务名> <模块名> <实体名> --step <序号>
```

**示例**:
```bash
# 只生成 DO 实体类（步骤 1）
/skill yili-crud config common TRmbsInvoiceAuthentication --step 1

# 只生成 Controller（步骤 12）
/skill yili-crud config common TRmbsInvoiceAuthentication --step 12
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 服务名 | ✅ | 目标服务，对应包路径中 `com.yili.[服务名]` | `config`, `claim.ptp`, `fund` |
| 模块名 | ✅ | 功能模块子包名 | `common`, `accountteam` |
| 实体名 | ❓ | PascalCase 实体类名（有 DDL 时可省略） | `TRmbsInvoiceAuthentication` |
| --ddl | ❌ | DDL 文件路径，自动提取表名、字段 | `./create_table.sql` |
| --step | ❌ | 指定只生成某一层(1-12) | `1`, `8`, `12` |

## 执行流程

### 第一步：确认信息

AI 会根据命令参数和 DDL 自动提取以下信息，缺少的会询问用户：

| 信息项 | 来源 | 示例 |
|--------|------|------|
| 服务名 | 命令参数 | `config`, `claim.ptp` |
| 模块名 | 命令参数 | `common`, `accountteam` |
| 实体名 | 命令参数 / DDL 提取 | `TRmbsInvoiceAuthentication` |
| 数据库表名 | DDL 提取 / 询问用户 | `T_RMBS_INVOICE_AUTHENTICATION` |
| 序列名 | DDL 提取 / 询问用户 | `SEQ_INVOICE_AUTHENTICATION` |
| 业务描述 | 询问用户 | "认证权限配置" |
| 菜单路径 | 询问用户 | "系统运维/基础数据配置/认证权限配置" |
| 字段列表 | DDL 提取 / 询问用户 | 字段名、类型、说明 |

### 第二步：确定包路径

根据目标服务确定包路径模式，详见 [references/package-rules.md](references/package-rules.md)。

### 第三步：按顺序生成代码

**严格按以下顺序生成，每步确认后再进行下一步：**

| 序号 | 层级 | 模板文件 | 说明 |
|------|------|----------|------|
| 1 | DO 实体类 | [templates/do-template.java](templates/do-template.java) | 数据库表映射 |
| 2 | Mapper 接口 | [templates/mapper-template.java](templates/mapper-template.java) | 数据访问层 |
| 3 | Mapper XML | [templates/mapper-xml-template.xml](templates/mapper-xml-template.xml) | MyBatis XML |
| 4 | 主 DTO | [templates/dto-template.java](templates/dto-template.java) | 数据传输对象 |
| 5 | 删除 DTO | [templates/dto-del-template.java](templates/dto-del-template.java) | 批量删除参数 |
| 6 | 导出 DTO | [templates/dto-export-template.java](templates/dto-export-template.java) | Excel 导出 |
| 7 | DtoConverter | [templates/converter-template.java](templates/converter-template.java) | DO↔DTO 转换 |
| 8 | Facade 接口 | [templates/facade-interface-template.java](templates/facade-interface-template.java) | I[实体名]DoService |
| 9 | Facade 实现 | [templates/facade-impl-template.java](templates/facade-impl-template.java) | [实体名]DoServiceImpl |
| 10 | Service 接口 | [templates/service-interface-template.java](templates/service-interface-template.java) | 业务服务接口 |
| 11 | Service 实现 | [templates/service-impl-template.java](templates/service-impl-template.java) | 业务服务实现 |
| 12 | Controller | [templates/controller-template.java](templates/controller-template.java) | 前端控制器 |

## 参考文档

| 文档 | 内容 |
|------|------|
| [references/package-rules.md](references/package-rules.md) | 各服务的包路径规则和文件位置速查 |
| [references/constraints.md](references/constraints.md) | 核心约束、命名规范、继承关系、检查清单 |
| [references/base-api.md](references/base-api.md) | 基类 API 速查（BaseDoXService/BaseMapperX） |
| [examples/examples.md](examples/examples.md) | 完整示例（认证权限配置 CRUD） |
