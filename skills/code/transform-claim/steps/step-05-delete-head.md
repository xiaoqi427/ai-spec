# 步骤5：删除报账单头 (Delete Claim Head)

## 📋 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `DeleteT{XXX}ClaimService.java` |
| **新代码** | `T{XXX}DeleteClaimServiceImpl.java` |
| **继承基类** | `BaseDeleteClaimService` |
| **接口** | `IT{XXX}DeleteClaimService extends IBaseDeleteClaimService` |
| **核心方法** | `delete(Long claimId)` |
| **可重写钩子** | `preExecute(TRmbsClaimPageDto claimDto, UserObjectFullDto user)` |
| **模板文件** | `templates/head/interface-delete-template.java`, `templates/head/impl-delete-template.java` |

---

## 🔄 迁移策略

### ⚠️ 重要提醒：基类已处理大量逻辑

`BaseDeleteClaimService.delete()` 是一个**巨大的方法**（1185行），内部已包含几乎所有 T{XXX} 的删除逻辑。**子类通常只需在 preExecute() 做前置处理**。

### 1. 定位老代码

- 路径: `DeleteT{XXX}ClaimService.java`
- 记录文件总行数

### 2. 分析老代码

老代码通常包含两大部分：

| 部分 | 内容 | 迁移方式 |
|------|------|----------|
| 删除前处理 | T{XXX}特有的前置逻辑 | 🔧 迁移到 preExecute |
| 通用删除 | 清理关联表、移历史等 | ✅ 基类已处理 |

### 3. 基类能力速查

`BaseDeleteClaimService.delete()` (1185行):

```
delete(claimId)
  ├── 查报账单信息
  ├── preExecute(claimDto, user)                 // ★ 子类重写点
  ├── validataClaim(claimDto)                    // 删除前校验
  ├── [多个T{XXX}特殊处理 - 基类已包含]
  ├── 删除发票关联 → 还原发票池 → 释放防重库
  ├── 删除税金表 → 付款计划表
  ├── [各种T{XXX}的特殊释放逻辑]
  ├── moveToHis()                                // 移动到历史表
  ├── 消除待办 → 删除流程数据
  └── 删除报账单本身
```

**基类已覆盖**（无需迁移）：
- T041/T042/T034/T027/T030/T012/T044/T014/T049/T069/T900/T038等的特殊处理
- 发票关联、防重库、OCR、税金、付款计划、无票行、承兑汇票等清理

### 4. 提取需迁移的逻辑

**常见需迁移逻辑**：
- T{XXX}特有的删除前校验
- 基类未包含的特殊清理逻辑
- **大多数情况下preExecute为空**

### 5. 编写新代码

1. 基于模板创建接口和实现类
2. 通常只需继承，不需重写
3. 如有特殊逻辑，在 preExecute() 中实现

---

## ✅ 关键检查点

### 分析阶段
- [ ] 老代码已定位，记录行数
- [ ] 识别删除前的特殊处理
- [ ] 确认基类是否已包含该T{XXX}的处理

### 编码阶段
- [ ] 接口和实现类已创建
- [ ] 类上有 `@Slf4j` 和 `@Service`
- [ ] 大多数情况下无需重写方法

### 验证阶段
- [ ] 无编译错误
- [ ] 删除功能正常
- [ ] 无重复实现基类逻辑

---

## ⚠️ 常见坑点

1. **重复实现删除逻辑** - 基类的1185行代码已包含大量T{XXX}分支
2. **遗漏查看基类** - 必须仔细阅读基类，确认是否已有该T{XXX}的处理
3. **空实现是正常的** - 大多数T{XXX}的DeleteService都是空实现

---

## 📚 参考实现

- **T047**: `T047DeleteClaimServiceImpl.java` - 空实现
- **基类**: `BaseDeleteClaimService.java` (1185行) - 必须仔细阅读

---

## 📝 经验记录区

> 每次迁移后补充实战经验

<!-- 格式: [T{XXX}] {日期} {经验描述} -->
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
