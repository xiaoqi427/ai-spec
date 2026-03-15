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
老代码逻辑全部不用搬过来，在大load里面实现了

## 经验记录区
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
> 此区域用于记录实际迁移过程中发现的经验和教训。

<!--
格式：
- [T{XXX}] {日期} {经验描述}
-->
