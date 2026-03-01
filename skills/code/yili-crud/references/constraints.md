# 核心约束

## 1. DO 类约束
- 只映射数据库表中已存在的字段
- **严禁在 DO 中新增数据库不存在的字段**
- 扩展字段必须在 DTO 中添加
- 每个 DO 必须显式定义 `compId`（`@TableField("COMP_ID")`）
- `TENANT_CODE` 已在 TenantBaseDO 中，不重复定义
- 注解：`@Getter @Setter @ToString @TableName @Schema @KeySequence`

## 2. DTO 类约束
- 主 DTO 继承 DO，可添加额外查询/展示字段
- 导出 DTO 独立定义，不继承 DO
- 删除 DTO 继承 DO，仅含 `List<Long> ids` 字段

## 3. 分层调用规则
```
Controller → Service → Facade → Mapper → Database
```
- Controller 只能调用 Service
- Service 只能调用 Facade（可调用多个 Facade）
- Facade 只能调用 Mapper
- **禁止跨层调用、禁止反向调用**

## 4. Facade 层约束
- **禁止 if 逻辑**（简单的 null check 除外）
- **禁止写 SQL**
- **禁止业务逻辑**
- 只做 Mapper 交互和 DO↔DTO 转换

## 5. 对象转换约束
- 必须使用 MapStruct（`@Mapper(componentModel = "spring")`）
- **禁止使用 BeanUtils.copyProperties 等反射复制**

## 6. 字段命名映射
- `USER_NAME` → `userName`
- `TEAM_ID` → `teamId`
- `COMP_ID` → `compId`
- `ISENABLE` → `isEnable`（无下划线全大写→驼峰）
- `IS_REVIEW_ACCOUNT` → `isReviewAccount`
- `@TableField` 注解中列名必须与数据库完全一致

## 7. 字段类型规范
- 主键/外键 ID：`Long`
- 数值型：`Long`
- 日期时间：`LocalDateTime`
- 年月日：`LocalDate`
- 字符串：`String`
- 布尔值：`Integer`（0=否 1=是）

## 8. 标准 API 路由
- `POST /page` - 分页查询
- `POST /delete-by-ids` - 批量删除
- `POST /get-by-id` - 根据 ID 查询
- `POST /save` - 新增或更新
- `POST /export` - 导出

## 9. 继承关系

```java
// DO
[实体名]Do extends TenantBaseDO

// Mapper
[实体名]DoMapper extends BaseMapperX<[实体名]Do>

// DtoConverter (DO ↔ DTO 双向转换)
[实体名]DtoConverter extends BaseMapperConverter<[实体名]Do, [实体名]Dto>

// Facade 接口
I[实体名]DoService extends IBaseDoXService<[实体名]Dto, [实体名]Do>

// Facade 实现
[实体名]DoServiceImpl extends BaseDoXService<[实体名]Dto, [实体名]Do, [实体名]DoMapper, [实体名]DtoConverter>
    implements I[实体名]DoService

// Service 接口（纯业务接口，不强制继承）
[实体名]Service

// Service 实现（注入 Facade）
[实体名]ServiceImpl implements [实体名]Service

// Controller（注入 Service）
[实体名]Controller
```

## 10. 命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| DO | `[实体名]Do` | `TRmbsInvoiceAuthenticationDo` |
| 主 DTO | `[实体名]Dto` | `TRmbsInvoiceAuthenticationDto` |
| 删除 DTO | `[实体名]DelDto` | `TRmbsInvoiceAuthenticationDelDto` |
| 导出 DTO | `[实体名]ExportDto` | `TRmbsInvoiceAuthenticationExportDto` |
| Mapper | `[实体名]DoMapper` | `TRmbsInvoiceAuthenticationDoMapper` |
| DtoConverter | `[实体名]DtoConverter` | `TRmbsInvoiceAuthenticationDtoConverter` |
| Facade 接口 | `I[实体名]DoService` | `ITRmbsInvoiceAuthenticationDoService` |
| Facade 实现 | `[实体名]DoServiceImpl` | `TRmbsInvoiceAuthenticationDoServiceImpl` |
| Service 接口 | `[实体名]Service` | `TRmbsInvoiceAuthenticationService` |
| Service 实现 | `[实体名]ServiceImpl` | `TRmbsInvoiceAuthenticationServiceImpl` |
| Controller | `[实体名]Controller` | `TRmbsInvoiceAuthenticationController` |

## 11. 生成前检查清单

```
- [ ] 包路径与目标服务一致
- [ ] DO 字段与数据库表字段一一对应，无多余字段
- [ ] compId 字段已显式定义
- [ ] DtoConverter 继承 BaseMapperConverter<Do, Dto>
- [ ] Facade 继承 IBaseDoXService<Dto, Do>
- [ ] Facade 实现继承 BaseDoXService<Dto, Do, Mapper, DtoConverter>
- [ ] Service 注入 Facade（而非 Mapper）
- [ ] Controller 注入 Service（而非 Facade）
- [ ] 所有 import 语句完整，无遗漏
- [ ] 使用 Lombok 注解（@Data, @Getter, @Setter, @Slf4j）
- [ ] 使用 @author sevenxiao
```
