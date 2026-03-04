# 步骤10：加载明细行 (Load Claim Line)

## 📋 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `ListAllT{XXX}ClaimLinesService.java` |
| **新代码** | `T{XXX}LoadClaimLineServiceImpl.java` |
| **继承基类** | `BaseLoadClaimLineService` |
| **接口** | `IBaseLoadClaimLineService`（通常不需要独立接口） |
| **核心方法** | `load(TRmbsClaimPageFullDto full)` |
| **可重写钩子** | `preResult(pageLine, full)`, `addPreLine(pageLine, full, loadParams)` |
| **特殊要求** | Bean命名: `@Service(value = "listAllT{XXX}ClaimLinesService")` |
| **模板文件** | `templates/line/impl-load-line-template.java` |

## 迁移策略

### 关键特殊性

1. **Bean 命名必须正确**: 框架通过 `@Service(value = "listAllT{XXX}ClaimLinesService")` 动态查找
2. **通常是空实现**: 大部分 T{XXX} 的行加载逻辑完全被基类覆盖
3. **事件链模式**: 基类使用 `Consumer<TRmbsClaimLineDto>` 链式处理每一行

### 第一步：定位老代码

1. 找到 `ListAllT{XXX}ClaimLinesService.java`
2. 记录文件总行数

### 第二步：分析老代码 execute() 方法

老代码通常包含：
```
execute() {
    // 模块A: 查行列表 → 基类已处理
    // 模块B: 遍历每行设置金额 → 基类已处理
    // 模块C: 设调整金额(adjustAmount) → 基类已处理
    // 模块D: 设借款金额(loanAmount) → 基类已处理
    // 模块E: 设外币申请金额(foreignApplyAmount) → 基类已处理
    // 模块F: 设CVT行IDs → 基类已处理
    // 模块G: 设借贷方向(dcType) → 基类已处理
    // 模块H: 设可编辑事项(isEditMatter) → 基类已处理
    // 模块I: T{XXX}特有的行处理 → 需要迁移到 addPreLine 或 preResult
}
```

### 第三步：对照基类已实现能力

`BaseLoadClaimLineService.load()` 已实现的完整流程 (354行)：

```
load(full)
  ├── 查行列表: findByClaimId()
  ├── 构建 LineLoadParams(full, pageLine, itemId)
  ├── 遍历每一行，执行事件链:
  │   ├── amount()              // 设金额 (amountCNY, claimLineAmount)
  │   ├── adjustAmount()        // 设调整金额 (lineDiffAmount)
  │   ├── loanAmount()          // 设借款金额
  │   ├── foreignApplyAmount()  // 设外币申请金额
  │   ├── addCvtLineIds()       // 设CVT行IDs
  │   ├── dcType()              // 设借贷方向
  │   ├── isEditMatter()        // 设可编辑事项标识
  │   └── addPreLine(...)       // ★ 空钩子 → 子类扩展点
  ├── preResult(pageLine, full)  // ★ 空钩子 → 子类重写点
  └── return pageLine
```

**LineLoadParams 内置工具方法**:
- `isT057()` - 判断是否为 T057
- `isT049OrT069()` - 判断是否为 T049 或 T069
- `full()` / `pageLine()` / `itemId()` - 获取上下文

### 第四步：两个扩展点的区别

| 扩展点 | 执行时机 | 适用场景 |
|--------|---------|---------|
| `addPreLine()` | 在每一行的事件链中执行 | 需要对每一行做额外处理 |
| `preResult()` | 所有行处理完成后执行 | 需要对整体结果做后处理 |

**addPreLine 用法**:
```java
@Override
protected List<Consumer<TRmbsClaimLineDto>> addPreLine(
        TRmbsClaimLinePageDto pageLine,
        TRmbsClaimPageFullDto full,
        LineLoadParams loadParams) {
    List<Consumer<TRmbsClaimLineDto>> consumers = new ArrayList<>();
    consumers.add(line -> {
        // 对每一行的额外处理
        line.setSomeField(someValue);
    });
    return consumers;
}
```

**preResult 用法**:
```java
@Override
public void preResult(TRmbsClaimLinePageDto pageLine, TRmbsClaimPageFullDto full) {
    // 所有行处理完后的后处理
    // 如：统计、排序、过滤等
}
```

### 第五步：编写新代码

大多数情况下只需要：

```java
@Slf4j
@Service(value = "listAllT{XXX}ClaimLinesService")
public class T{XXX}LoadClaimLineServiceImpl extends BaseLoadClaimLineService {
    // 空实现 - 基类已满足
}
```

## 检查清单

### 分析阶段
- [ ] 找到老代码文件
- [ ] 逐行分析 execute() 方法
- [ ] 对照 BaseLoadClaimLineService (354行)
- [ ] 标记基类已覆盖的行处理逻辑
- [ ] 确认是否有 T{XXX} 特有的行级处理
- [ ] 确认是否需要 addPreLine 或 preResult

### 编码阶段
- [ ] 创建实现类 `T{XXX}LoadClaimLineServiceImpl extends BaseLoadClaimLineService`
- [ ] **关键**: 类上添加 `@Service(value = "listAllT{XXX}ClaimLinesService")` 命名
- [ ] 如有行级处理：重写 `addPreLine()`
- [ ] 如有后处理：重写 `preResult(pageLine, full)`
- [ ] 如为空实现：保持类体为空
- [ ] 注释标注原代码行数

### 验证阶段
- [ ] 无编译错误
- [ ] **Bean 命名正确**: `listAllT{XXX}ClaimLinesService` 格式
- [ ] 没有重复基类的金额/方向/CVT处理
- [ ] import语句完整

## 常见坑点

1. **Bean 命名是硬性要求**: 必须是 `@Service(value = "listAllT{XXX}ClaimLinesService")`，否则框架找不到
2. **空实现很常见**: 参考 T047，基类已覆盖所有行加载逻辑，子类是空的
3. **不需要独立接口**: LoadClaimLine 通常不需要创建独立的接口，直接 extends `BaseLoadClaimLineService`
4. **事件链顺序**: `addPreLine` 返回的 Consumer 会在基类事件链末尾执行，在金额/方向等处理之后
5. **preResult 时机**: 在所有行都处理完后执行，适合做汇总统计

## 参考实现

- T047: `T047LoadClaimLineService.java` (20行) - 空实现，只有 @Service 命名
- 基类: `BaseLoadClaimLineService.java` (354行)

## 经验记录区
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
> 此区域用于记录实际迁移过程中发现的经验和教训。

<!--
格式：
- [T{XXX}] {日期} {经验描述}
-->
