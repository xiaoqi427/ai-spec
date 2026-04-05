# 修复完成检查清单

## 修复前检查

- [ ] 已读取 Bug 完整描述和所有评论
- [ ] 已识别出模板编号 (T{XXX})
- [ ] 已识别出涉及的功能 (New/Save/Delete/Load/Submit/Callback)
- [ ] 已定位老代码基线文件和关键行号
- [ ] 已定位新代码对应文件
- [ ] 已输出分析报告并等待用户确认

## 代码修复检查

### 逻辑完整性
- [ ] 老代码的所有分支条件已在新代码中保留
- [ ] 默认值与老代码一致
- [ ] 状态流转逻辑完整
- [ ] 过滤条件没有遗漏
- [ ] 特殊处理（模板特有逻辑）已保留
- [ ] SQL 查询条件一致
- [ ] 参数传递完整

### 架构规范
- [ ] 没有跨层调用 (Controller→Business→DOService→Mapper)
- [ ] DO Service 中没有 if 逻辑
- [ ] DO Service 中没有 SQL 语句
- [ ] DO Service 中没有业务逻辑
- [ ] Controller 只调用 Business 层
- [ ] Business 层处理核心业务逻辑

### 技术规范
- [ ] 使用 `@Resource` 注入，非 `@Autowired`
- [ ] 使用 `@Slf4j` 注解，非手动声明 Logger
- [ ] 使用 Lombok 注解 (`@Data`, `@Builder` 等)
- [ ] 使用 MapStruct 转换，禁止反射复制
- [ ] 金额字段使用 BigDecimal
- [ ] 时间字段使用 LocalDateTime
- [ ] 没有魔法数字，使用常量或枚举
- [ ] 布尔字段使用 is/has/can 开头

### 事务管理
- [ ] `@Transactional(rollbackFor = Exception.class)` 在 Business 层
- [ ] 没有在 Controller 层使用 @Transactional
- [ ] 检查事务传播行为是否正确

### 代码注释
- [ ] 修复方法标注了老代码文件路径和行号
- [ ] 修复方法标注了对应的 Bug ID
- [ ] 方法有 Javadoc 注释
- [ ] 关键逻辑有行内注释

### 编译验证
- [ ] JDK 版本为 21（`java -version` 确认，项目强制 Java 21）
- [ ] `mvn compile -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository` 编译通过
- [ ] import 语句完整，无遗漏
- [ ] 没有类型不匹配错误
- [ ] 没有方法签名不一致

## 修复后输出

- [ ] 输出修复报告（修改了哪些文件、修改内容）
- [ ] 标注前端 Bug（如有）
- [ ] 提供编译验证结果
