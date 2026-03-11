# 老代码 → 新代码 方法映射关系

> 本文件记录老代码 Service 方法到新框架 Override 方法的标准映射规则
> AI 在执行 --file-migrate / --method-migrate 时参考此映射

---

## 1. 老代码文件 → 新代码文件映射

| 老代码类名模式 | 新代码类名模式 | 说明 |
|--------------|-------------|------|
| `NewT{XXX}ClaimService` | `T{XXX}NewClaimServiceImpl` | 新建报账单头 |
| `NewT{XXX}ClaimLineService` | `T{XXX}NewClaimLineServiceImpl` | 新建报账单行 |
| `InsertT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` | 新增保存头（合并到 Save） |
| `UpdateT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` | 更新保存头（合并到 Save） |
| `InsertT{XXX}ClaimLineService` | `T{XXX}SaveClaimLineServiceImpl` | 新增保存行（合并到 Save） |
| `UpdateT{XXX}ClaimLineService` | `T{XXX}UpdateClaimLineServiceImpl` | 更新保存行 |
| `DeleteT{XXX}ClaimService` | `T{XXX}DeleteClaimServiceImpl` | 删除报账单头 |
| `DeleteT{XXX}ClaimLinesService` | `T{XXX}DeleteClaimLineServiceImpl` | 删除报账单行 |
| `LoadAllT{XXX}Service` | `T{XXX}LoadClaimServiceImpl` | 加载报账单（多 View 合并） |
| `ViewT{XXX}ClaimService` | `T{XXX}LoadClaimServiceImpl` | 合并到 Load |
| `ViewT{XXX}ClaimLineService` | `T{XXX}LoadClaimLineServiceImpl` | 加载报账单行 |
| `CallBackT{XXX}Service` | `T{XXX}CallBackClaimServiceImpl` | 回调 |
| `SubmitT{XXX}Service` | `T{XXX}SubmitClaimServiceImpl` | 提交 |
| `ListAllT{XXX}ClaimLinesService` | `T{XXX}LoadClaimLineServiceImpl` | 加载行列表 |

---

## 2. 老代码方法 → 新代码方法映射

### New（新建头/行）
| 老方法 | 新方法 | 基类 |
|-------|-------|------|
| `execute(MessageObject)` | `newClaim(TRmbsClaimPageFullDto)` | `BaseNewClaimService` |
| `preExecute()` | `before(TRmbsClaimPageFullDto)` | `BaseNewClaimService` |

### Save（保存头/行，Insert+Update 合并）
| 老方法 | 新方法 | 基类 |
|-------|-------|------|
| `execute(MessageObject)` / `preExecute()` | `saveClaimHead(TRmbsClaimPageFullDto)` | `BaseSaveOrUpdateClaimService` |
| `insertClaimLineFromClaim()` | `updateClaimLineFromClaim(TRmbsClaimPageFullDto)` | `BaseSaveOrUpdateClaimService` |
| `validate()` / `validateField()` | `validation(TRmbsClaimPageFullDto, Map)` | `BaseSaveOrUpdateClaimService` |
| `setClaimNo()` | `before(TRmbsClaimPageFullDto)` | `BaseSaveOrUpdateClaimService` |

### Delete（删除头/行）
| 老方法 | 新方法 | 基类 |
|-------|-------|------|
| `execute(MessageObject)` | `deleteClaimHead(TRmbsClaimPageFullDto)` | `BaseDeleteClaimService` |
| `preExecute()` | `before(TRmbsClaimPageFullDto)` | `BaseDeleteClaimService` |

### Load（加载）
| 老方法 | 新方法 | 基类 |
|-------|-------|------|
| `execute(MessageObject)` / 多 View 合并 | `load(String claimId)` | `BaseLoadClaimService` |

### Callback（回调）
| 老方法 | 新方法 | 基类 |
|-------|-------|------|
| `execute(MessageObject)` | `executeEnd(...)` | `BaseCallBackClaimService` |
| `preExecute()` | `before(...)` | `BaseCallBackClaimService` |

### Submit（提交）
| 老方法 | 新方法 | 基类 |
|-------|-------|------|
| `execute(MessageObject)` | `validate(TRmbsClaimPageFullDto, Map)` | `BaseSubmitClaimService` |
| `preExecute()` | `preResult(Map)` | `BaseSubmitClaimService` |
| `validateXxx()` | `validate(TRmbsClaimPageFullDto, Map)` 内调用 ChainValidator | `BaseSubmitClaimService` |

---

## 3. 不迁移的内容

| 类型 | 标记 | 说明 |
|------|------|------|
| `gd/Gd*` 前缀文件 | 🔕 | gd 相关旧逻辑不迁移 |
| 老代码已注释代码块 | 🔕 | 已注释的不迁移，仅标注 |
| `TBaseService/` 基类方法 | ✅基类 | 新框架已有对应基类实现 |
