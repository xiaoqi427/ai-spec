# 基类 API 速查

## BaseDoXService 继承的方法

```java
// 已自动注入
protected M mapper;    // Mapper 实例
protected C converter; // DtoConverter 实例

// 基础 CRUD（操作 DTO）
T save(T bean);                        // 新增或更新
T update(T bean);                      // 更新
T selectById(Serializable id);         // 按ID查询（返回DTO）
List<T> selectByIds(Collection ids);   // 按ID批列表查询
List<T> selectAll();                   // 查询全部
int deleteById(Serializable id);       // 按ID删除
int deleteByIds(Collection ids);       // 按ID批量删除
List<BatchResult> saveAll(Collection<T> list); // 批量保存

// 条件查询
T selectFirst(Object... params);       // 条件查询第一条
List<T> select(Object... params);      // 条件查询列表
Long selectCount(Object... params);    // 条件计数

// 分页
Page<T> page(PageParam<P, T> page);    // 分页查询

// 转换
E reverseConvert(T dto);              // DTO → DO
T convert(E entity);                   // DO → DTO
List<T> convertList(List<E> list);     // DO列表 → DTO列表
```

## BaseMapperX 扩展方法

```java
// 分页（自动 DO→DTO 转换）
<D> Page<D> page(BaseMapperConverter<T, D> converter, PageParam<D, D> pageParam);

// 批量删除
int deleteByIds(Collection<?> idList);
```

## BaseMapperConverter 方法

```java
// DO → DTO
Target convert(Source source);
List<Target> convertList(List<Source> sources);

// DTO → DO
Source reverseConvert(Target target);
List<Source> reverseConvertList(List<Target> targets);
```
