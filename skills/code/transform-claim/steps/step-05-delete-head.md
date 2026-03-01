# 步骤5：删除报账单头 (Delete Claim Head)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `DeleteT{XXX}ClaimService.java` |
| **新代码** | `T{XXX}DeleteClaimServiceImpl.java` |
| **继承基类** | `BaseDeleteClaimService` |
| **接口** | `IT{XXX}DeleteClaimService extends IBaseDeleteClaimService` |
| **核心方法** | `delete(Long claimId)` |
| **可重写钩子** | `preExecute(TRmbsClaimPageDto claimDto, UserObjectFullDto user)` |
| **模板文件** | `templates/head/interface-delete-template.java`, `templates/head/impl-delete-template.java` |

## 迁移策略

### 重要提醒：基类已处理大量 itemId 分支

`BaseDeleteClaimService.delete()` 是一个**巨大的方法**（1185行），内部已包含了几乎所有 T{XXX} 的删除逻辑。子类通常只需要在 `preExecute()` 中做前置处理。

### 第一步：定位老代码

1. 找到 `DeleteT{XXX}ClaimService.java`
2. 记录文件总行数

### 第二步：分析老代码 execute() 方法

老代码的 `execute()` 方法通常包含两大部分：
1. **删除前的特殊处理**（T{XXX}独有）→ 可能需要迁移
2. **通用删除逻辑**（清理关联表、移历史表等）→ 基类已处理

### 第三步：对照基类已实现能力

`BaseDeleteClaimService.delete(Long claimId)` 已实现的完整流程：

```
delete(claimId)
  ├── 查报账单信息
  ├── preExecute(claimDto, user)                    // ★ 空钩子 → 子类重写点
  ├── validataClaim(claimDto)                       // 删除前校验
  ├── [T041特殊处理]
  ├── [T042特殊处理] - 调写转结果接口
  ├── removeAppInvoiceAssData()                     // 删除发票关联
  ├── claimInvoiceRecordLibraryApiService.release() // 还原发票池
  ├── removeLibrary()                               // 释放防重库
  ├── removeOcrCallbackOcrinvoice()                 // 释放OCR识别
  ├── 删除税金表
  ├── [T034] 牛奶T027子报账单删除
  ├── [T034] 优然保理核销
  ├── 删除付款计划表
  ├── [T027/T030] 无票行信息释放
  ├── [T012/T027] TMS/TW接口回传
  ├── [T044] 承兑汇票释放
  ├── [T014] 承兑汇票释放(T014版)
  ├── [T049/T069] CVT记录+差额删除
  ├── [T900] 采购方销售方关联释放
  ├── [T038/T069] 金德瑞影像夹清空
  ├── claimHisService.moveToHis()                   // 移动到历史表
  ├── 消除待办
  ├── 删除流程表数据
  ├── [T034] 对账单状态+牛奶+PO关联+开票系统
  ├── [T039/T034] PO关联+结算单封锁
  ├── [T046] AR余额删除
  ├── [T047] 承兑汇票更新+附件删除
  ├── [T001] 关联表记录+出行信息
  ├── TPM释放
  ├── 资金台账释放
  ├── [T040/T023等] 发票核销删除
  ├── [T051/T052] 关联表删除
  ├── [T053/T054/T056] OA接口
  ├── [T030+SRM] SRM状态回传
  ├── 发票认证状态更新
  ├── T008出行平台状态回传
  ├── 承兑签收释放
  ├── 资产变更页签删除
  ├── [T059] 租赁台账状态更新
  ├── T064/T065/T066处理
  ├── OA流程关联删除
  ├── [T031+保利] 保利T031删除
  ├── [SK] 司库状态回传
  ├── 报告删除
  ├── TPM影像删除
  └── claimDoService.delete()                       // 最终删除
```

### 第四步：确定需要迁移的逻辑

大部分 T{XXX} 的 DeleteClaimService **已被基类覆盖**。子类通常只需要：
1. 在 `preExecute()` 中做删除前的数据准备
2. 如果有基类未覆盖的清理逻辑，在 `preExecute()` 中处理

**判断标准**: 老代码中的逻辑如果在基类的 `if("T{XXX}".equals(itemId))` 分支中已存在，则不需要迁移。

## 检查清单

### 分析阶段
- [ ] 找到老代码文件
- [ ] 逐行分析 execute() 方法
- [ ] **重点**: 逐个 `if("T{XXX}".equals(itemId))` 检查基类是否已覆盖
- [ ] 标记基类未覆盖的逻辑（通常很少）
- [ ] 确认 preExecute() 的调用时机（在所有删除操作之前）

### 编码阶段
- [ ] 创建接口 `IT{XXX}DeleteClaimService extends IBaseDeleteClaimService`
- [ ] 创建实现类 `T{XXX}DeleteClaimServiceImpl extends BaseDeleteClaimService`
- [ ] 类上添加 `@Slf4j` 和 `@Service`
- [ ] 如有前置逻辑：重写 `preExecute(TRmbsClaimPageDto claimDto, UserObjectFullDto user)`
- [ ] 注释标注原代码行数

### 验证阶段
- [ ] 无编译错误
- [ ] 确认基类已覆盖该 T{XXX} 的所有 itemId 分支
- [ ] 没有重复基类已实现的逻辑
- [ ] import语句完整

## 常见坑点

1. **基类覆盖面极广**: `BaseDeleteClaimService` 已经包含了绝大多数 T{XXX} 的删除逻辑，**仔细搜索基类代码中的 itemId 分支**
2. **空实现是常见的**: 很多 T{XXX} 的删除在基类中完全覆盖，子类只需空实现
3. **preExecute 时机**: 在所有基类删除逻辑之前执行，适合做数据准备或状态校验
4. **@Transactional**: 基类 delete 方法未标注事务注解，注意子类是否需要
5. **不要重写 delete()**: 通常不需要重写 `delete()` 方法，基类的流程已经很完整

## 参考实现

- T047: `claim-otc/.../t047/head/impl/T047DeleteClaimServiceImpl.java` - 参考基类中 T047 分支
- 基类: `BaseDeleteClaimService.java` (1185行) - 需搜索 T{XXX} 相关的 itemId 判断

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
<!--
格式：
- [T{XXX}] {日期} {经验描述}
-->
