# 步骤8：BPM 回调 (Callback)

## 概述

| 项目 | 内容 |
|------|------|
| **老代码** | `CallBackT{XXX}Service.java` |
| **新代码** | `T{XXX}CallBackClaimServiceImpl.java` |
| **继承基类** | `BaseCallBackClaimService` |
| **接口** | `IT{XXX}CallBackClaimService extends IBaseCallBackClaimService` |
| **核心方法** | 多个 `execute{Action}()` 回调方法 |
| **可重写钩子** | `executeExecute`, `executeEnd`, `executeDrawBack`, `executeUndo`, `executeDelete` 等 |
| **模板文件** | `templates/bpm/interface-callback-template.java`, `templates/bpm/impl-callback-template.java` |

## 迁移策略

### 核心概念：回调动作类型

BPM 流程在不同节点会触发回调，每种动作对应不同的方法：

| 回调方法 | 动作 | 说明 |
|---------|------|------|
| `executeExecuteRoot(data, full)` | 起草提交 | 起草环节提交到下一步 |
| `executeExecute(data, full)` | 审批通过 | 审批环节通过到下一步 |
| `executeEnd(data, full)` | 流程办结 | 流程最终完成 |
| `executeDrawBack(data, full)` | 退回 | 退回到上一步/起草人 |
| `executeUndo(data, full)` | 撤回 | 提交人撤回 |
| `executeDelete(data, full)` | 删除 | 流程中删除 |
| `executeTrun(data, full)` | 转办 | 转给其他人处理 |
| `executeTesong(data, full)` | 特送 | 特殊发送 |
| `executeAgent(data, full)` | 代理 | 代理审批 |

### 第一步：定位老代码

1. 找到 `CallBackT{XXX}Service.java`
2. 记录文件总行数
3. 识别老代码中的回调方法（通常在 switch/if 块中按 actionType 分支）

### 第二步：分析老代码回调逻辑

老代码通常结构：
```java
execute() {
    String actionType = data.getActionType();
    switch (actionType) {
        case "execute":      // → 对应 executeExecute
            // 审批通过逻辑
            break;
        case "end":          // → 对应 executeEnd
            // 办结逻辑（预算冻结、营销写入、收款更新等）
            break;
        case "drawback":     // → 对应 executeDrawBack
            // 退回逻辑（预算解冻等）
            break;
        case "undo":         // → 对应 executeUndo
            // 撤回逻辑
            break;
    }
}
```

### 第三步：对照基类已实现能力

`BaseCallBackClaimService` (515行) 已注入的服务和已实现的公共逻辑：

**已注入的15+ Service:**
```
claimService, writeDataService, moveClaimToHisService,
pmProjectfreezeBudgetService, pmBudgetOperationService,
tpmCallBackApiService, receiptCallBackApiService,
fundCallBackApiService, cxCallBackApiService,
paymentCallBackApiService, fundOperateInfoCallBackApiService,
settleCallBackApiService, ...
```

**统一入口 execute():**
```
execute(callBackBusinessData, consumer)
  ├── integrateBusinessData()           // 整合业务数据
  │   ├── 查报账单完整信息
  │   ├── 设置flowId
  │   └── consumer.accept(full, data)   // 调具体回调方法
  └── claimService.save(full)           // 保存变更
```

**基类已实现的回调方法 (子类可直接调用或重写):**

| 方法 | 默认行为 |
|------|---------|
| `executeExecuteRoot` | 空 |
| `executeExecute` | 空 |
| `executeEnd` | 空 |
| `executeDrawBack` | 空 |
| `executeUndo` | 空 |
| `executeDelete` | 空 |
| `executeTrun` | 空 |
| `executeTesong` | 空 |
| `executeAgent` | 空 |

**基类提供的公共工具方法:**
- `writeClaimData(full)` - 写入ERP数据
- `moveClaimToHis(full)` - 移动到历史表
- `freezeBudget(full)` / `unfreezeBudget(full)` - 预算冻结/解冻
- `writeTpmData(full, flag)` - TPM数据写入
- `receiptCallBack(full)` - 收款回调
- `fundCallBack(full)` - 资金回调

### 第四步：映射老代码到新钩子

逐个回调动作分析：

1. **executeEnd (办结)** - 通常是最复杂的，包含：
   - 写入ERP数据
   - 预算冻结
   - 营销数据写入
   - 收款状态更新
   - 移动到历史表

2. **executeDrawBack (退回)** - 通常包含：
   - 预算解冻
   - 状态回滚

3. **executeExecute (审批通过)** - 通常较简单：
   - 设置审批环节信息
   - 可能更新某些标识

### 第五步：编写新代码

重写需要的回调方法，利用基类提供的公共工具方法：

```java
@Override
public void executeEnd(CallBackBusinessDataDto data, TRmbsClaimPageFullDto full) {
    // 1. 写入ERP数据（基类提供）
    writeClaimData(full);
    
    // 2. 预算冻结（基类提供）
    freezeBudget(full);
    
    // 3. T{XXX}特有的办结逻辑
    // ... 从老代码迁移
    
    // 4. 移动到历史表（基类提供）
    moveClaimToHis(full);
}
```

## 检查清单

### 分析阶段
- [ ] 找到老代码文件
- [ ] 识别老代码中所有回调动作类型
- [ ] 逐个动作分析逻辑
- [ ] 标记基类已提供的公共方法（write/freeze/move等）
- [ ] 标记 T{XXX} 特有的回调逻辑
- [ ] 确认办结(end)的完整逻辑链

### 编码阶段
- [ ] 创建接口 `IT{XXX}CallBackClaimService extends IBaseCallBackClaimService`
- [ ] 创建实现类 `T{XXX}CallBackClaimServiceImpl extends BaseCallBackClaimService`
- [ ] 类上添加 `@Slf4j` 和 `@Service`
- [ ] 重写需要的回调方法（executeEnd、executeDrawBack 等）
- [ ] 利用基类公共方法（writeClaimData、freezeBudget、moveClaimToHis）
- [ ] 每段逻辑标注原代码行数
- [ ] 需要注入的额外Service用 `@Resource` 声明

### 验证阶段
- [ ] 无编译错误
- [ ] 所有回调动作都有对应处理
- [ ] 办结逻辑完整（写入、冻结、移动历史表等）
- [ ] 退回逻辑完整（解冻等）
- [ ] 没有重复基类已提供的公共方法逻辑
- [ ] import语句完整

## 常见坑点

1. **办结逻辑最复杂**: `executeEnd` 通常是最大的方法，包含多步骤的业务处理，需要仔细逐步迁移
2. **执行顺序很重要**: 写入ERP → 预算冻结 → 特有逻辑 → 移动历史表，顺序不能乱
3. **基类公共方法丰富**: 不要重复实现预算冻结、数据写入等逻辑，基类已经封装好了
4. **回调参数**: 所有回调方法的签名是 `(CallBackBusinessDataDto data, TRmbsClaimPageFullDto full)`
5. **data 对象**: `CallBackBusinessDataDto` 包含 flowId、actionType、oldActivityDefId、newActivityDefId 等流程信息
6. **空实现是允许的**: 如果某个回调动作不需要 T{XXX} 特有逻辑，可以不重写（基类默认空实现）

## 参考实现

- T047: `claim-otc/.../t047/bpm/impl/T047CallBackClaimServiceImpl.java`
- 基类: `BaseCallBackClaimService.java` (515行)

## 经验记录区

> 此区域用于记录实际迁移过程中发现的经验和教训。
- TODO需要去检查是否有API可以调用，没有就需要创建
- 迁移完成后需要检查一遍逻辑
- 工作流常用枚举类型ClaimProcessEnum
- 
<!--
格式：
- [T{XXX}] {日期} {经验描述}
示例：
- [T014] 2025-12-28 办结时需要额外处理承兑汇票状态
- [T047] 2025-12-28 T047回调很简单，只需要 executeEnd 中调 writeClaimData + moveClaimToHis
-->
