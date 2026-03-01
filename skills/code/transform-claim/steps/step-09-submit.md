# 步骤9：提交校验 (Submit)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `SubmitT{XXX}ClaimService.java` / `SubmitClaimService.java` 中的 T{XXX} 分支 |
| **新代码** | `T{XXX}SubmitClaimServiceImpl.java` |
| **继承基类** | `BaseSubmitClaimService` |
| **接口** | `IT{XXX}SubmitClaimService extends IBaseSubmitClaimService` |
| **核心方法** | `submit(P params)` |
| **可重写钩子** | `preResult(full)`, `validate(full, params)`, `loadAll(fullDto, params)` |
| **模板文件** | `templates/bpm/interface-submit-template.java`, `templates/bpm/impl-submit-template.java` |

## 迁移策略

### 核心概念：提交三阶段

新框架的提交流程分为三个阶段：

```
submit(params)
  └── before(full, params)
      ├── preResult(full)              // 阶段1: 数据预处理（抛异常直接中断）
      ├── validate(full, params)       // 阶段2: 链式校验（收集所有错误）
      │   ├── validateCommon()         //   通用校验
      │   ├── loadAll(fullDto, params) //   加载完整数据
      │   └── claimValidationOrchestrator.validate() // 编排器执行
      └── return chainValidator        // 返回校验结果
```

**三个阶段的区别**:

| 阶段 | 方法 | 错误处理 | 适用场景 |
|------|------|---------|---------|
| 预处理 | `preResult()` | 抛异常直接中断 | 致命错误、数据修正 |
| 校验 | `validate()` | ChainValidator 收集 | 业务规则校验 |
| 数据加载 | `loadAll()` | 在 validate 内调用 | 校验前加载必要数据 |

### 第一步：定位老代码

1. 找到 `SubmitT{XXX}ClaimService.java`（如果存在）
2. 在通用 `SubmitClaimService.java` 中搜索 T{XXX} 相关分支
3. 记录行数和逻辑模块

### 第二步：分析老代码校验逻辑

老代码通常包含两类校验：

**A. 前置校验（对应 preResult）**:
- 数据完整性检查（必填字段）
- 数据修正（自动填充默认值）
- 致命错误判断（直接阻断提交）

**B. 业务校验（对应 validate 中的 Validator）**:
- 金额校验（合计、借贷平衡）
- 发票校验
- 预算校验
- 承兑汇票校验
- 资产相关校验
- 其他 T{XXX} 特有业务规则

### 第三步：对照基类已实现能力

`BaseSubmitClaimService` (178行) 已实现：

```
submit(params)
  ├── 查报账单完整信息
  └── before(full, params):
      ├── preResult(full)                    // ★ 空钩子 → 子类重写
      └── validate(full, params):
          ├── validateCommon(full, params)    // 通用校验
          ├── loadAll(fullDto, params)        // ★ 加载数据（默认通过 SpringUtil.bean 找 Load 服务）
          ├── buildValidationContext()        // 构建校验上下文
          └── claimValidationOrchestrator.validate(context)  // 编排器执行所有 Validator
```

**基类已注入**:
- `claimService` - 报账单服务
- `claimValidationOrchestrator` - 校验编排器（自动发现和执行所有注册的 Validator）

**loadAll 默认实现**:
```java
protected void loadAll(TRmbsClaimPageFullDto fullDto, P params) {
    String itemId = params.getItemId();
    IBaseLoadClaimService loadService = SpringUtil.bean("loadAll", itemId, "ClaimService");
    if (loadService != null) {
        TRmbsClaimPageFullDto pageFullDto = loadService.load(params, user);
        BeanUtil.copyProperties(pageFullDto, fullDto);
    }
}
```

### 第四步：校验器架构

新框架使用 **校验编排器** 模式，每个校验规则是一个独立的 Validator：

```
ClaimValidationOrchestrator
  ├── CommonAmountValidator       // 金额通用校验
  ├── InvoiceValidator            // 发票校验
  ├── BudgetValidator             // 预算校验
  ├── AssetLineAmountValidator    // 资产金额校验
  └── T{XXX}SpecificValidator     // T{XXX}特有校验
```

**如果需要新增 T{XXX} 特有的校验规则**:
1. 创建新的 Validator 类，继承 `AbstractClaimValidator`
2. 通过注解注册到编排器
3. 编排器会自动发现并执行

### 第五步：选择正确的重写方式

**场景1**: 只需要数据预处理（无特殊校验）
```java
@Override
protected void preResult(TRmbsClaimPageFullDto full) {
    // 数据修正或前置检查
}
```

**场景2**: 需要额外校验规则
```java
@Override
public <P extends TRmbsClaimPageDto> ChainValidator validate(TRmbsClaimPageFullDto full, P params) {
    // 调用基类校验
    ChainValidator validator = super.validate(full, params);
    // 追加 T{XXX} 特有校验
    // ...
    return validator;
}
```

**场景3**: 需要自定义数据加载（性能优化）
```java
@Override
protected <P extends TRmbsClaimPageDto> void loadAll(TRmbsClaimPageFullDto fullDto, P params) {
    // 自定义加载逻辑（如提前加载某些数据避免N+1查询）
    super.loadAll(fullDto, params);
}
```

## 检查清单

### 分析阶段
- [ ] 找到老代码中 T{XXX} 的提交校验逻辑
- [ ] 区分"前置校验"和"业务校验"
- [ ] 标记哪些校验已被通用 Validator 覆盖
- [ ] 标记需要新增的 T{XXX} 特有校验
- [ ] 确认 loadAll 是否需要自定义（性能问题）

### 编码阶段
- [ ] 创建接口 `IT{XXX}SubmitClaimService extends IBaseSubmitClaimService`
- [ ] 创建实现类 `T{XXX}SubmitClaimServiceImpl extends BaseSubmitClaimService`
- [ ] 类上添加 `@Slf4j` 和 `@Service`
- [ ] 如有前置处理：重写 `preResult(TRmbsClaimPageFullDto full)`
- [ ] 如有额外校验：重写 `validate()` 或创建新的 Validator
- [ ] 如需性能优化：重写 `loadAll()`
- [ ] 注释标注原代码行数

### 验证阶段
- [ ] 无编译错误
- [ ] 所有老代码的校验规则都有对应处理
- [ ] preResult 中的错误抛异常（直接中断）
- [ ] validate 中的错误走 ChainValidator（收集所有错误）
- [ ] 没有重复已有 Validator 的校验逻辑
- [ ] import语句完整

## 常见坑点

1. **preResult vs validate 区分**: `preResult` 中抛异常会直接中断提交；`validate` 中通过 `ChainValidator` 收集所有错误后统一返回
2. **校验编排器**: 新框架通过 `ClaimValidationOrchestrator` 自动发现所有注册的 Validator，不需要在 Submit 中手动调用每个校验
3. **loadAll 性能**: 默认的 loadAll 会通过 SpringUtil.bean 找到 Load 服务加载全量数据，如果数据量大需要优化
4. **ChainValidator**: 使用 `ChainValidator` 而不是直接抛异常，这样前端可以一次看到所有校验错误
5. **不要在 preResult 中做业务校验**: preResult 适合数据修正和致命检查，业务规则校验应该走 Validator

## 参考实现

- T047: `claim-otc/.../t047/bpm/impl/T047SubmitClaimServiceImpl.java` - 含 preResult + validate 重写
- 基类: `BaseSubmitClaimService.java` (178行)

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
- 工作流常用枚举类型ClaimProcessEnum
<!--
格式：
- [T{XXX}] {日期} {经验描述}
示例：
- [T047] 2025-12-28 T047的承兑汇票校验需要新建独立的Validator
- [T014] 2025-12-28 T014的preResult中需要修正isTransMode字段
-->
