# 步骤7：加载报账单 (Load Claim)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `LoadAllT{XXX}Service.java`（通常有多个 LoadAll） |
| **新代码** | `T{XXX}LoadClaimServiceImpl.java`（合并多个 LoadAll） |
| **继承基类** | `BaseLoadClaimService` |
| **接口** | `IT{XXX}LoadClaimService extends IBaseLoadClaimService` |
| **核心方法** | `load(TRmbsClaimPageDto params, UserObjectFullDto user)` |
| **可重写钩子** | `preResult(claimPageFull, user)` |
| **特殊要求** | Bean命名: `@Service("loadAllT{XXX}ClaimService")` 或通过 `ClaimProcessEnum` |
| **模板文件** | `templates/head/interface-load-template.java`, `templates/head/impl-load-template.java` |

## 迁移策略

### 关键变更：多个 LoadAll 合并为一个

**老框架**: 一个 T{XXX} 通常有多个 LoadAll Service（按 processStateEng 区分）：
- `LoadAllT{XXX}Service.java` (起草环节)
- `LoadAllT{XXX}Service2.java` (会计审批环节)
- `LoadAll2T{XXX}Service.java` (其他环节)

**新框架**: 合并为一个 `T{XXX}LoadClaimServiceImpl`，在 `preResult()` 中通过 `processStateEng` 判断环节差异。

### 第一步：定位老代码

1. 搜索所有 `LoadAllT{XXX}*.java` 和 `LoadAll*T{XXX}*.java` 文件
2. 记录每个文件的行数和对应环节
3. **注意**: 可能有 2-3 个甚至更多的 LoadAll 文件

### 第二步：分析老代码 execute() 方法

老代码的 `execute()` 通常包含：

```
execute() {
    // 模块A: 查报账单信息 → 基类已处理
    // 模块B: 大类/小类信息加载 → 基类 loadCommonInfo 已处理
    // 模块C: 合同信息加载 → 基类 loadCommonInfo 已处理
    // 模块D: 明细行加载 → 基类 loadCommonInfo 已处理
    // 模块E: 银行信息加载 → 基类 loadCommonInfo 已处理
    // 模块F: 附件/影像加载 → 基类 loadCommonInfo 已处理
    // 模块G: 权限校验 → 基类 permissionValidation 已处理
    // 模块H: 黑名单信息 → 基类 loadAllBlacklist 已处理
    // 模块I: 8段信息(viewBrInfo/viewCrInfo) → 需要迁移到 preResult
    // 模块J: T{XXX}特有的数据加载 → 需要迁移到 preResult
    // 模块K: 环节特有的数据加载 → 需要迁移到 preResult（判断 processStateEng）
}
```

### 第三步：对照基类已实现能力

`BaseLoadClaimService.load()` 已实现的完整流程 (262行)：

```
load(params, user)
  ├── claimService.loadToFullByClaimId(claimId) // 查报账单完整信息
  ├── Assert.notNull(claimPageFull)              // 存在性校验
  ├── claimPageFull.setOldClaim(params)           // 保存前端参数
  ├── permissionValidation()                     // 权限校验
  ├── loadCommonInfo():                          // 公共信息加载
  │   ├── findItemLevel2()                       //   大类信息
  │   ├── findItemLevel3()                       //   小类信息
  │   ├── loadCmContract()                       //   合同信息
  │   ├── loadAllLine()                          //   行信息
  │   │   ├── findLines()                        //     明细行
  │   │   ├── findClaimTaxLines()                //     税金行
  │   │   ├── findPayLists()                     //     计划付款行
  │   │   ├── findClaimRel()                     //     借款核销
  │   │   └── findPayLines()                     //     发票核销
  │   ├── loadAllBankList()                      //   银行信息
  │   ├── findAttachment()                       //   附件列表
  │   ├── findImage()                            //   电子影像
  │   └── bt()                                   //   按钮权限
  ├── preResult(claimPageFull, user)             // ★ 空钩子 → 子类重写点
  ├── loadAllBlacklist()                         // 黑名单
  ├── compensateMissingData()                    // 数据补偿
  └── recordFinanceStartTime()                   // 记录会计审批开始时间
```

**基类额外提供的工具方法**:
- `viewBrCrInfoLine(full, user)` - 借贷方8段值处理
- `viewCrInfo(full, user)` - 贷方8段
- `viewBrInfo(full, user)` - 借方8段
- `viewClaimBrInfo(full, user)` - 报账单借方信息

### 第四步：合并多个 LoadAll 到 preResult

在 `preResult()` 中通过环节判断实现差异化加载：

```java
@Override
protected TRmbsClaimPageFullDto preResult(TRmbsClaimPageFullDto full, UserObjectFullDto user) {
    String processStateEng = full.getClaim().getProcessStateEng();
    
    // 所有环节通用的加载
    viewBrCrInfoLine(full, user);  // 8段信息
    // ... 其他通用逻辑
    
    // 起草环节特有
    if (ClaimProcessEnum.isDrafterActivity(processStateEng)) {
        // LoadAllT{XXX}Service 的特有逻辑
    }
    
    // 会计审批环节特有
    if (ClaimProcessEnum.isFinanceActivity(processStateEng)) {
        // LoadAllT{XXX}Service2 的特有逻辑
    }
    
    return full;
}
```

### 第五步：Bean 命名

Load 服务需要特殊的 Bean 命名，以便框架通过 `SpringUtil.bean()` 动态获取：

```java
@Service("loadAllT{XXX}ClaimService")  // 或按 ClaimProcessEnum 配置
```

**注意**: 具体命名规则需查看 `ClaimProcessEnum` 枚举中的配置。

## 检查清单

### 分析阶段
- [ ] 搜索所有 `LoadAllT{XXX}` 相关文件（可能有多个）
- [ ] 列出每个 LoadAll 对应的环节（processStateEng）
- [ ] 逐行分析每个 LoadAll 的 execute() 方法
- [ ] 标记每个环节的通用逻辑和特有逻辑
- [ ] 对照 BaseLoadClaimService (262行) 的 loadCommonInfo
- [ ] 确认 8段信息的加载方式
- [ ] 确认 Bean 命名规则

### 编码阶段
- [ ] 创建接口 `IT{XXX}LoadClaimService extends IBaseLoadClaimService`
- [ ] 创建实现类 `T{XXX}LoadClaimServiceImpl extends BaseLoadClaimService`
- [ ] 类上添加 `@Slf4j` 和正确的 `@Service("loadAllT{XXX}ClaimService")` 命名
- [ ] 重写 `preResult(TRmbsClaimPageFullDto claimPageFull, UserObjectFullDto user)`
- [ ] 在 preResult 中合并多个老 LoadAll 的逻辑
- [ ] 通过 `ClaimProcessEnum` 判断环节差异
- [ ] 每段逻辑标注来源文件和行数

### 验证阶段
- [ ] 无编译错误
- [ ] 所有老 LoadAll 文件的逻辑都已迁移
- [ ] Bean 命名正确（可被框架发现）
- [ ] 基类已加载的信息没有重复
- [ ] 环节判断逻辑正确
- [ ] import语句完整

## 常见坑点

1. **遗漏 LoadAll 文件**: 一个 T{XXX} 可能有多个 LoadAll，务必搜索完整
2. **8段信息**: 基类有 `viewBrCrInfoLine/viewBrInfo/viewCrInfo` 方法，但默认不调用，需要在 `preResult()` 中显式调用
3. **Bean 命名关键**: 如果命名不对，框架无法通过 `SpringUtil.bean()` 找到对应的 Load 服务
4. **环节合并**: 不同环节的 LoadAll 逻辑差异可能很大，合并时要用 `ClaimProcessEnum` 正确判断
5. **preResult 返回值**: 必须返回 `claimPageFull`
6. **loadCommonInfo 已很全面**: 基类 `loadCommonInfo` 已加载了大类、小类、合同、行、银行、附件、影像等，不要重复

## 参考实现

- T047: `claim-otc/.../t047/head/impl/T047LoadClaimServiceImpl.java`
- 基类: `BaseLoadClaimService.java` (262行)

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
<!--
格式：
- [T{XXX}] {日期} {经验描述}
示例：
- [T047] 2025-12-25 T047只有一个LoadAll，preResult中不需要环节判断
- [T056] 2025-12-26 T056有3个LoadAll，分别对应起草/业务记账/会计审批环节
-->
