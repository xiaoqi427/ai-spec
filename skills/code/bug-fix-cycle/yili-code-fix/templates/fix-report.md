# Bug 修复报告模板

## Bug #{bug_id}: {bug_title}

### 基本信息

| 字段 | 值 |
|------|-----|
| Bug ID | #{bug_id} |
| 模板编号 | T{XXX} |
| 业务模块 | {module} |
| 问题现象 | {description} |
| Bug 类型 | 后端 / 前端 / 前后端混合 |

### 老代码基线

| 文件 | 方法 | 行号 | 逻辑描述 |
|------|------|------|---------|
| `{old_file_path}` | `{method_name}` | L{start}-L{end} | {logic_description} |

### 新代码位置

| 文件 | 方法 | 行号 |
|------|------|------|
| `{new_file_path}` | `{method_name}` | L{start}-L{end} |

### 遗漏分析

| 编号 | 老代码位置 | 逻辑描述 | 类型 | 处理方式 |
|------|-----------|---------|------|---------|
| 1 | `{file}` L{line} | {description} | 后端 | 已修复 |
| 2 | `{file}` L{line} | {description} | 前端 | 已标注 |

### 修复内容 (后端)

**修改文件**: `{modified_file_path}`

**修改说明**:
{modification_description}

**代码变更**:
```java
// 老代码: {old_file} L{line}-L{line}
// Bug修复: #{bug_id}
{code_snippet}
```

### 前端标注 (如有)

```
【】前端问题
对应老代码: {old_frontend_file} L{line}
遗漏逻辑: {description}
新框架不修改, 需前端开发处理
```

### 检查清单

- [x] 老代码基线标注 (文件路径+行号)
- [x] 逻辑与老代码一致
- [x] 无跨层调用
- [x] DO Service 无 if/SQL/业务逻辑
- [x] 事务注解正确
- [x] import 完整
- [x] 使用 @Resource
- [x] 使用 Lombok
- [x] 编译通过

### 编译结果

```
{compile_output}
```

### SIT 测试 (如已执行)

| 测试项 | 结果 | 截图 |
|--------|------|------|
| {test_scenario} | 通过/失败 | {screenshot_path} |
