---
trigger: always_on
alwaysApply: true
---
# USER_RULES.MD – 个人开发偏好 (仅本地有效)

> **说明**: 此文件已被加入 `.gitignore`,不会提交到代码库。
> 每个开发者可以在这里配置自己的个人开发偏好,AI 助手会读取并遵守这些规则。

---

## 1. 语言偏好

```yaml
# 回答语言: 中文 / 英文
response_language: 中文

# 代码注释语言: 中文 / 英文 / 混合
code_comment_language: 中文
```

---

## 2. 代码风格偏好

### 2.1 依赖注入方式

```yaml
# 优先使用: @Autowired / @Resource / 构造器注入
preferred_injection: @Autowired
```

### 2.2 Lombok 使用

```yaml
# 是否使用 Lombok: true / false
use_lombok: true

# 偏好的 Lombok 注解
preferred_lombok_annotations:
  - @Slf4j        # 日志
  - @Data         # getter/setter
  - @Builder      # 构建器模式
  - @NoArgsConstructor
  - @AllArgsConstructor
```

### 2.3 日志风格

```yaml
# 日志变量名: log / logger / LOGGER
log_variable_name: log

# 日志方法调用风格
log_style: |
  // 优先使用占位符而非字符串拼接
  log.info("用户ID: {}, 操作: {}", userId, operation);
  
  // 错误日志带异常堆栈
  log.error("处理失败: {}", message, exception);
```
### 2.4 代码设计
复杂逻辑需要遵循设计模式
例如遵守SOLID原则

原则缩写	名称	核心含义	目的
S	单一职责原则	一个类应该只有一个引起它变化的原因	降低类的复杂度，提高可读性
O	开闭原则	对扩展开放，对修改关闭	最重要的原则，让系统易于扩展
L	里氏替换原则	子类对象能够替换其父类对象，且程序逻辑不变	确保继承关系的正确性
I	接口隔离原则	客户端不应依赖它不需要的接口	解耦，降低类之间的依赖程度
D	依赖倒置原则	高层模块不应依赖低层模块，二者都应依赖抽象	通过抽象（接口/抽象类）解耦

---

## 3. 命名偏好

```yaml
# 变量命名风格: 驼峰 / 下划线
variable_naming: 驼峰

# 常量命名: 全大写下划线
constant_naming: UPPER_SNAKE_CASE

# 测试方法命名: should_xxx / test_xxx / xxx_should_xxx
test_method_naming: should_xxx
```

示例:
```java
// 变量
String userName;
List<String> orderIdList;

// 常量
private static final String DEFAULT_ENCODING = "UTF-8";

// 测试方法
@Test
public void should_return_success_when_valid_input() { }
```

---

## 4. 注释偏好

### 4.1 注释详细程度

```yaml
# 注释详细程度: 简洁 / 详细 / 适中
comment_detail_level: 适中
```

### 4.2 注释模板

```java
/**
 * 业务方法说明
 * 
 * @param xxx 参数说明
 * @return 返回值说明
 * @throws XxxException 异常说明
 */
```

---

## 5. 异常处理偏好

```yaml
# 异常处理方式
exception_handling: |
  // 优先使用自定义业务异常
  throw new BusinessException(ErrorCode.INVALID_PARAM, "参数不合法");
  
  // Service 层抛出异常,Controller 层统一处理
  // 不要在 Service 层 catch 后返回 null
```

---

## 6. 单元测试偏好

```yaml
# 测试框架: JUnit4 / JUnit5
test_framework: JUnit5

# Mock 框架: Mockito / PowerMock
mock_framework: Mockito

# 测试覆盖率要求
test_coverage: |
  - Service 层核心业务逻辑: 80%+
  - 工具类方法: 90%+
  - Controller 层: 可选
```

---

## 7. 代码审查偏好

```yaml
# 是否需要 AI 主动指出潜在问题
proactive_code_review: true

# 关注点
review_focus:
  - 空指针风险
  - 线程安全问题
  - 性能瓶颈
  - 资源泄漏 (连接、流未关闭)
  - SQL 注入风险
```

---

## 8. 响应风格偏好

```yaml
# 回答详细程度: 简洁 / 详细 / 适中
response_detail_level: 适中

# 是否需要示例代码
include_code_examples: true

# 是否需要解释原因
explain_reasoning: true
```

---

## 9. 工具类使用偏好

```yaml
# 字符串工具: StringUtils (Apache) / StringUtils (Spring) / Hutool
string_util_preference: Apache Commons StringUtils

# 集合工具: CollectionUtils / Guava / Hutool
collection_util_preference: Apache Commons CollectionUtils

# 日期工具: DateUtil (项目自定义) / LocalDateTime (Java 8) / Hutool
date_util_preference: 项目自定义 DateUtil
```

---

## 10. 数据库操作偏好

```yaml
# ORM 偏好: JPA / MyBatis
orm_preference: MyBatis (复杂查询), JPA (简单 CRUD)

# 分页方式: PageHelper / JPA Pageable
pagination_preference: PageHelper

# SQL 日志
show_sql: false  # 开发时可设为 true
```

---

## 11. 个人代码习惯

```yaml
# 方法长度限制
max_method_lines: 50

# 类长度限制
max_class_lines: 500

# 参数数量限制
max_parameters: 5  # 超过时考虑使用参数对象

# 是否使用流式 API (Stream)
prefer_stream_api: true

# 是否使用 Optional
prefer_optional: true
```

---

## 12. Git 提交偏好

```yaml
# 提交信息格式
commit_message_format: |
  <type>(<scope>): <subject>
  
  <body>
  
  <footer>
  
  # type: feat/fix/docs/style/refactor/test/chore
  # 示例: feat(claim): 新增资产报账单导出功能

# 是否需要 AI 生成提交信息
generate_commit_message: true
```

---

## 13. 文档偏好

```yaml
# API 文档工具: Swagger / OpenAPI / 手写文档
api_doc_tool: Swagger

# README 更新频率: 每次功能更新 / 重大变更时 / 不自动更新
readme_update_frequency: 重大变更时
```

---

## 14. 性能优化偏好

```yaml
# 是否主动提示性能优化建议
suggest_performance_optimization: true

# 关注点
performance_focus:
  - 避免 N+1 查询
  - 合理使用缓存
  - 避免大对象传输
  - 批量操作优化
```

---

## 15. 自定义规则

```yaml
# 在这里添加您的个人规则
custom_rules: |
  1. 所有对外接口必须有参数校验
  2. 涉及金额计算使用 BigDecimal
  3. 时间字段统一使用 LocalDateTime
  4. 布尔类型字段命名用 is/has/can 开头
  5. 禁止使用魔法数字,必须定义常量
```

---

## 使用说明

1. **修改此文件**: 根据您的个人习惯修改上述配置
2. **AI 会自动读取**: Qoder 在处理代码时会优先考虑这些偏好
3. **优先级**: USER_RULES.MD > AGENTS.MD > 系统默认规则
4. **不会提交**: 此文件已加入 `.gitignore`,仅在本地生效

---

## 示例配置 (快速开始)

如果您不确定如何配置,可以直接使用以下推荐配置:

```yaml
response_language: 中文
code_comment_language: 中文
preferred_injection: @Autowired
use_lombok: true
log_variable_name: log
test_framework: JUnit5
orm_preference: MyBatis
response_detail_level: 适中
proactive_code_review: true
```
