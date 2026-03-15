---
name: compare-transform
description: 报账单老新代码对比分析器。对比老代码（yldc-caiwugongxiangpingtai-fsscYR-master）与新框架代码（fssc-claim-service），输出对比报告、检测迁移Bug、定位代码上下文、提供省钱策略，支持文件级/方法级迁移分析和逻辑深度对比。当用户需要对比老新代码差异、检查迁移是否有遗漏/Bug、或者想找某个功能在新代码中的位置时使用。
---
# Compare Transform Skill（报账单老新代码对比分析器）
@author: sevenxiao

## 📋 概述

此 skill 专注于**对比老代码与新框架迁移代码**，提供8大核心能力：

1. **`--compare`** 输出老新代码对比 Markdown 报告
2. **`--bug-check`** 检查新代码流程明显 Bug / 迁移遗漏
3. **`--save-cost`** 省钱策略（减少 Token 消耗的最优搜索路径）
4. **`--locate`** 输入新代码上下文，快速定位相关文件和逻辑
5. **`--file-migrate`** 文件级别迁移分析：分析老文件，输出新文件应如何实现（新文件可能不存在）
6. **`--method-migrate`** 方法级别迁移分析：分析老方法，输出新方法应如何实现（新文件可能不存在）
7. **`--logic-diff`** 两个已存在文件之间的逻辑深度对比分析
8. **`--method-diff`** 两个已存在方法之间的逻辑深度对比分析

---

## 💻 使用方式

```bash
# 功能1: 输出对比报告
/skill compare-transform <模板编号> --compare [--step <步骤号>]

# 功能2: Bug 检查
/skill compare-transform <模板编号> --bug-check [--step <步骤号>]

# 功能3: 省钱策略（先看这个再搜索）
/skill compare-transform <模板编号> --save-cost

# 功能4: 上下文定位
/skill compare-transform --locate <关键词/类名/方法名>

# 功能5: 文件级别迁移分析（新文件可能不存在，输出迁移指导）
/skill compare-transform --file-migrate <老文件路径> [<新文件路径>]

# 功能6: 方法级别迁移分析（新文件可能不存在，输出迁移指导）
/skill compare-transform --method-migrate <老文件路径>#<方法名> [<新文件路径>#<方法名>]

# 功能7: 两文件逻辑深度对比
/skill compare-transform --logic-diff <文件路径A> <文件路径B>

# 功能8: 两方法逻辑深度对比
/skill compare-transform --method-diff <文件路径A>#<方法名> <文件路径B>#<方法名>
```

**示例**:
```bash
# 对比 T044 的所有步骤
/skill compare-transform T044 --compare

# 只检查 T044 的 Submit（步骤9）是否有 Bug
/skill compare-transform T044 --bug-check --step 9

# 快速找省钱路径（先调用此命令，再搜索）
/skill compare-transform T044 --save-cost

# 找 "updateClaimLineFromClaim" 方法在新代码哪里
/skill compare-transform --locate updateClaimLineFromClaim

# 文件级别迁移分析：分析老文件，新文件不存在时直接给迁移方案
/skill compare-transform --file-migrate \
  yldc-caiwugongxiangpingtai-fsscYR-master/.../InsertT044ClaimService.java

# 文件级别迁移分析：新文件已存在时，对比并补全遗漏
/skill compare-transform --file-migrate \
  yldc-caiwugongxiangpingtai-fsscYR-master/.../InsertT044ClaimService.java \
  fssc-claim-service/claim-otc-service/.../T044SaveClaimServiceImpl.java

# 方法级别迁移分析：只提供老方法，输出新方法迁移方案
/skill compare-transform --method-migrate \
  yldc-caiwugongxiangpingtai-fsscYR-master/.../InsertT044ClaimService.java#execute

# 方法级别迁移分析：提供新旧方法，检查迁移是否完整
/skill compare-transform --method-migrate \
  yldc-caiwugongxiangpingtai-fsscYR-master/.../InsertT044ClaimService.java#execute \
  fssc-claim-service/claim-otc-service/.../T044SaveClaimServiceImpl.java#saveClaimHead

# 两文件逻辑对比
/skill compare-transform --logic-diff \
  fssc-claim-service/claim-otc-service/.../T044SaveClaimServiceImpl.java \
  fssc-claim-service/claim-tr-service/.../T001SaveClaimServiceImpl.java

# 两方法逻辑对比
/skill compare-transform --method-diff \
  fssc-claim-service/claim-otc-service/.../T044SubmitClaimServiceImpl.java#validate \
  fssc-claim-service/claim-tr-service/.../T001SubmitClaimServiceImpl.java#validate
```

---

## 🔄 功能1: 对比报告 (`--compare`)

### 执行流程

**Step 1: 定位老代码文件**

根据模板编号 `T{XXX}`，在以下路径查找：
```
yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{XXX}/
```

收集老代码文件列表（参考 [老代码结构](references/old-code-structure.md)）:
- `NewT{XXX}ClaimService.java`
- `InsertT{XXX}ClaimService.java` + `UpdateT{XXX}ClaimService.java`
- `DeleteT{XXX}ClaimService.java` + `DeleteT{XXX}ClaimLinesService.java`
- `LoadAllT{XXX}Service.java` + `ViewT{XXX}*.java`
- `CallBackT{XXX}Service.java`
- `SubmitT{XXX}Service.java`
- `ListAllT{XXX}ClaimLinesService.java`

**Step 2: 定位新代码文件**

根据模块（tr/ptp/otc/eer/fa/rtr）在以下路径查找：
```
fssc-claim-service/claim-{module}-service/src/main/java/com/yili/claim/{module}/claim/t{xxx}/
```

**Step 3: 逐步骤对比并输出 Markdown**

对每个步骤，必须输出以下标准格式：

```markdown
## 步骤X: {功能名} 对比

### 📄 老代码
- 文件: `{老代码路径}`
- 行数: {XX} 行
- 核心逻辑:
  - 行 XX-XX: {逻辑描述}
  - 行 XX-XX: {逻辑描述}

### 🆕 新代码
- 文件: `{新代码路径}`
- 行数: {XX} 行
- 实现方式: extends {基类名}
- 重写方法:
  - `{方法名}()` → 对应老代码行 XX-XX

### ✅ 已迁移逻辑
| 老代码行 | 逻辑描述 | 新代码位置 |
|---------|---------|---------|
| XX-XX | {描述} | {方法名} L{行号} |

### ⚠️ 差异/疑似遗漏
| 老代码行 | 逻辑描述 | 状态 | 说明 |
|---------|---------|------|------|
| XX-XX | {描述} | ❓遗漏/🔕已注释/✅基类实现 | {说明} |
```

### 对比完成后输出汇总

```markdown
## 📊 对比汇总

| 步骤 | 老代码行数 | 新代码行数 | 迁移状态 | 疑似问题数 |
|------|----------|----------|---------|-----------|
| 1.New头 | XX | XX | ✅完整 | 0 |
| 2.New行 | XX | XX | ✅完整 | 0 |
| 3.Save头 | XX | XX | ⚠️有疑问 | 2 |
| ... | ... | ... | ... | ... |

**总评**: {整体迁移完整度评估}
```

---

## 🐛 功能2: Bug 检查 (`--bug-check`)

### Bug 检查清单（每个步骤必须检查以下所有项）

#### 2.1 通用 Bug 检查
- [ ] **import 完整性**: 所有使用的类都有 import，没有 `xxx.yyy.ZZZ.method()` 全路径写法
- [ ] **方法签名匹配**: Override 方法的参数类型与基类完全一致（尤其是泛型）
- [ ] **非 null 访问**: 对可能为 null 的对象调用方法前有判空
- [ ] **ClaimTemplateEnum 使用**: itemId 判断使用了 `ClaimTemplateEnum.TXXX.getCode()` 而非字符串字面量
- [ ] **BigDecimal 精度**: 金额计算使用了 `BigDecimal` 而非 `double/float`
- [ ] **@Resource 注入**: 依赖注入使用了 `@Resource`，且被注入的 Bean 存在

#### 2.2 Save（步骤3）专项检查
- [ ] `claimId == null` 判断在基类中，子类不重复实现新增/更新分支
- [ ] `updateClaimLineFromClaim()` 方法已实现（即使是空实现）
- [ ] `validation()` 方法的返回值正确：`super.validation(...)` 调用链完整

#### 2.3 Submit（步骤9）专项检查
- [ ] `preResult()` 方法：加载报账单数据的逻辑（查询 `TRmbsClaimPageFullDto`）
- [ ] `validate()` 方法：先调用 `super.validate(full, params)` 获取基础校验结果
- [ ] 校验器（Validator）通过 `@Resource` 注入，不是 `new` 出来的
- [ ] `ChainValidator.add()` 的 lambda 没有捕获外部可变状态
- [ ] 金额重算：涉及金额的提交逻辑是否调用了 `IClaimAmountService`
- [ ] **submit 流程是否完整**：`before()` → `preResult()` → `validate()` 调用链

#### 2.4 Callback（步骤8）专项检查
- [ ] `executeEnd()` 没有被重写（T045 等模板禁止重写）
- [ ] 回调中是否有更新报账单状态的逻辑（对应老代码 `updateClaimStatus()`）
- [ ] 异步逻辑：老代码中的 MQ 发送是否有对应新逻辑

#### 2.5 Load（步骤7）专项检查
- [ ] 老代码多个 View Service 的字段是否全部合并到 `TRmbsClaimPageFullDto`
- [ ] 特殊计算字段（不在 DO 中）是否在 DTO 中有对应字段
- [ ] `load()` 返回类型与接口声明一致

#### 2.6 Delete（步骤5/6）专项检查
- [ ] 删除前的状态校验（不能删除已提交的报账单）
- [ ] 级联删除：删除头时，行数据是否也级联处理

### Bug 输出格式

```markdown
## 🐛 Bug 检查报告: T{XXX} 步骤X ({功能名})

### ❌ 发现的 Bug / 问题

#### Bug 1: {Bug简述}
- **位置**: `{文件路径}` L{行号}
- **问题**: {详细描述}
- **老代码对应**: `{老代码文件}` 第 {XX-XX} 行
- **修复建议**: {具体修复方案}

#### Bug 2: {Bug简述}
...

### ⚠️ 疑似遗漏（需人工确认）

| 序号 | 描述 | 老代码位置 | 新代码状态 | 建议 |
|-----|------|----------|---------|------|
| 1 | {描述} | `{文件}` L{行} | 未找到对应实现 | 需补充 |

### ✅ 检查通过项（{N}/{总数}）
{列出通过检查的项目}
```

---

## 💰 功能3: 省钱策略 (`--save-cost`)

### 目标
**最小化 Token 消耗**，给出最优搜索顺序，避免大量读取不必要的文件。

### 省钱执行计划（按优先级排序）

**执行时输出以下策略表**:

```markdown
## 💰 省钱策略: T{XXX} 迁移分析

### 第1步: 先看已迁移的同类模块参考（0 Token 搜索）
参考路径（从最相似的模块选1个）:
- PTP 模块: `fssc-claim-service/claim-ptp-service/.../t010/`  
- OTC 模块: `fssc-claim-service/claim-otc-service/.../t044/`
- EER 模块: `fssc-claim-service/claim-eer-service/.../t047/`

**只读** `{最相似模板}` 的 **1个对应步骤文件**，用于了解模式。

### 第2步: 精准定位老代码（单文件读取）
老代码精确路径（直接读，不用搜索）:
```
yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{XXX}/
├── {列出所有需要的老代码文件}
```

### 第3步: 按步骤顺序读取（避免全量读取）
推荐顺序（先简单后复杂）:
1. New头 (通常 50-150 行，最简单)
2. Delete (通常 10-50 行)
3. Save头 (通常 80-200 行)
4. Load (通常 200-500 行，较复杂)
5. Submit (通常 200-1000 行，最复杂)

### 第4步: 基类方法查询（按需查，不提前读）
只在需要确认基类实现时才读基类：
- `BaseNewClaimService`: 167 行
- `BaseSaveOrUpdateClaimService`: 370 行
- `BaseSubmitClaimService`: 647 行
- `BaseCallBackClaimService`: 731 行

### 第5步: 节省 Token 的比较技巧
- 使用 `grep` 搜索关键字，不全量读文件
- 先读前100行（通常包含类声明和 Override 方法列表）
- Submit 方法重点关注 `validate()` 和 `preResult()` 区域

### 预估 Token 消耗
| 步骤 | 预估 Token | 备注 |
|------|---------|------|
| 分析老代码 | ~{N}K | 共 {N} 个文件，合计约 {N} 行 |
| 读新代码 | ~{N}K | 按步骤读，每步 ~{N} 行 |
| 基类查阅 | ~{N}K | 按需查阅 |
| **总计** | **~{N}K** | |
```

---

## 🔍 功能4: 上下文定位 (`--locate`)

### 目标
给定一个**类名/方法名/关键词**，快速找到：
1. 老代码中的对应位置
2. 新代码中的对应位置
3. 两者的调用关系

### 执行策略

**输入关键词 → 按以下优先级查找**:

#### 4.1 类名定位（如 `T044SaveClaimServiceImpl`）
1. 先匹配新代码命名模式: `T{XXX}{功能}ServiceImpl`
2. 推断路径: `claim-{module}-service/.../t{xxx}/{层级}/impl/`
3. 反推老代码: 根据功能映射关系找老代码文件

#### 4.2 方法名定位（如 `updateClaimLineFromClaim`）
1. 搜索基类中的定义
2. 找所有模块中的 Override 实现
3. 找老代码中的对应方法

#### 4.3 关键词定位（如 `processFlg`、`conClaimNo`）
1. 判断是字段名、方法参数还是常量
2. 在 DO/DTO 中查找字段定义
3. 在老代码 pojo 中查找对应字段

### 输出格式

```markdown
## 🔍 定位结果: `{关键词}`

### 老代码位置
- 文件: `{路径}`
- 行号: L{XX} - L{XX}
- 上下文:
```java
// 老代码片段（精简，最多20行）
```

### 新代码位置
- 文件: `{路径}`
- 行号: L{XX} - L{XX}
- 上下文:
```java
// 新代码片段（精简，最多20行）
```

### 调用关系
{老代码方法名} → {新代码对应方法名}

### 注意事项
- {如有特殊变化，如合并/拆分/重命名，在此说明}
```

---

## 📄 功能5: 文件级别迁移分析 (`--file-migrate`)

### 目标
分析**老代码文件**的逻辑，输出迁移到新框架的完整指导方案。  
**新文件可能不存在**（此时输出完整迁移方案）；**新文件已存在**时，额外检查迁移是否有遗漏。

### 两种模式

**模式A：只提供老文件（新文件不存在）**
> 读取老文件 → 分析所有逻辑 → 输出「应该如何迁移」的完整方案，包括：需要创建哪些新文件、每个方法如何映射到新框架

**模式B：同时提供新老文件（新文件已存在）**
> 读取两个文件 → 对比迁移完整度 → 找出遗漏逻辑 → 输出补全建议

### 执行流程

**Step 1: 读取老文件，提取全量逻辑清单**
- 提取所有方法签名、业务逻辑段落（精确到行号）
- 标注哪些是已注释代码（无需迁移）
- 标注哪些可能由基类处理（需在新框架中确认）

**Step 2（模式A）: 推断新框架映射方案**
- 根据老方法功能，映射到新框架对应的 Override 方法
- 参考同模块已迁移文件的模式
- 输出每个老逻辑块在新框架中的落地位置

**Step 2（模式B）: 对比已有新文件，检查遗漏**
- 读取新文件，提取所有 Override 方法
- 逐一核对老文件逻辑块在新文件中的覆盖情况

**Step 3: 输出报告**

### 输出格式

````markdown
## 📄 文件级迁移分析: `{老文件名}`

### 老文件概览
| 项 | 信息 |
|----|------|
| 路径 | `{老文件路径}` |
| 总行数 | {N} 行 |
| 方法数 | {N} 个 |
| 新文件状态 | 📁 不存在（模式A）/ ✅ 已存在（模式B） |

### 逻辑清单 & 迁移映射

| # | 老方法/逻辑块 (行号) | 功能描述 | 新框架落地位置 | 迁移状态 | 备注 |
|---|------------|---------|------------|--------|------|
| 1 | `execute()` L23-L89 | 保存报账单头 | `saveClaimHead()` 重写 | ✅ 已迁移/📋 待迁移 | |
| 2 | `validate()` L91-L120 | 字段校验 | `validation()` 重写 | ✅ 已迁移/📋 待迁移 | |
| 3 | `initParam()` L122-L150 | 初始化参数 | `before()` 重写 | 🔕 已注释 | 老代码已注释 |

### 待迁移逻辑详情（模式A 重点输出）

#### 逻辑块 {N}: `{老方法名}()` → 新框架 `{新方法名}()`
- **老代码** (L{XX}-L{XX}) 核心逻辑:
  - 行 L{XX}: {逻辑描述}
  - 行 L{XX}-L{XX}: {逻辑描述}
- **迁移建议**:
  - 在 `{新文件类名}` 中重写 `{新方法名}()`
  - 注意: {特殊处理说明，如 ClaimTemplateEnum 替换、BigDecimal 精度等}
- **参考**: 同类已迁移文件 `{参考文件路径}` L{XX}

### 遗漏/差异汇总（模式B 额外输出）
| 老代码行 | 逻辑描述 | 状态 | 说明 |
|---------|---------|------|------|
| L{XX}-L{XX} | {描述} | ❓遗漏 / ⚠️有差异 | {说明} |

### 迁移完成度
- 模式A: 共 {N} 个逻辑块，🔕 已注释 {N} 个，📋 待迁移 {N} 个
- 模式B: 已迁移 {N}/{N}，遗漏 {N} 处，差异 {N} 处
````

---

## 🔬 功能6: 方法级别迁移分析 (`--method-migrate`)

### 目标
分析**老方法**的逻辑，输出迁移到新框架的完整指导方案。  
**新方法可能不存在**（此时输出完整迁移方案）；**新方法已存在**时，额外检查迁移是否有遗漏。

### 两种模式

**模式A：只提供老方法（新方法不存在）**
> 读取老方法 → 逐逻辑块分析 → 输出「应该如何在新框架中实现」的完整方案

**模式B：同时提供新老方法（新方法已存在）**
> 读取两个方法 → 逐逻辑块核对 → 找出遗漏逻辑 → 输出补全建议

### 执行流程

**Step 1: 精确定位老方法边界，提取完整逻辑块清单**
- 在老文件中找到指定方法，记录起止行号
- 解析方法体：提取所有逻辑片段（判断、循环、调用、赋值等）
- 标注哪些是已注释代码（🔕 无需迁移）
- 推断哪些在新框架基类中已有对应实现（✅ 基类覆盖）

**Step 2（模式A）: 推断新框架落地位置**
- 每个逻辑块 → 在新框架哪个方法中实现
- 注意新框架的方法名变更规则、ClaimTemplateEnum 替换等

**Step 2（模式B）: 定位新方法，逐逻辑块核对**
- 在新文件中找到指定方法，记录起止行号
- 逐一核对老方法每个逻辑块在新方法中的覆盖情况

**Step 3: 输出报告**

### 输出格式

````markdown
## 🔬 方法级迁移分析: `{老文件名}#{老方法名}()`

### 方法概览
| 项 | 老方法 | 新方法 |
|----|--------|--------|
| 文件 | `{老文件路径}` | `{新文件路径}` / 不存在 |
| 行号 | L{XX}-L{XX} | L{XX}-L{XX} / — |
| 总行数 | {N} 行 | {N} 行 / — |
| 模式 | — | 模式A（新方法不存在）/ 模式B（已存在） |

### 逻辑块清单 & 迁移映射

| # | 老方法逻辑块 (行号) | 逻辑描述 | 新框架落地位置 | 迁移状态 |
|---|------------|---------|------------|--------|
| 1 | L{XX}-L{XX} | 参数校验: claimId 非空 | `validation()` L{XX} | ✅已迁移 / 📋待迁移 |
| 2 | L{XX}-L{XX} | 查询报账单头 | `saveClaimHead()` L{XX} | ✅已迁移 / 📋待迁移 |
| 3 | L{XX}-L{XX} | 发送 MQ 消息 | `after()` 重写 | ❓遗漏 |
| 4 | L{XX}-L{XX} | // 已注释逻辑 | — | 🔕已注释 |
| 5 | L{XX}-L{XX} | 更新状态 | 基类 `BaseSaveOrUpdateClaimService` | ✅基类覆盖 |

### 待迁移逻辑详情（模式A 重点输出）

#### 逻辑块 {N}: {逻辑描述} → 新框架 `{新方法名}()`
- **老代码** (L{XX}-L{XX}):
```java
// 老代码关键逻辑（保留行号注释）
```
- **迁移建议**:
  - 在 `{新框架方法名}()` 中实现
  - 注意: {特殊处理说明}
- **参考**: `{同类已迁移文件}` L{XX}

### 遗漏/差异详情（模式B 额外输出）

#### ❓ 遗漏项 {N}: {描述}
- **老方法** (L{XX}-L{XX}): {逻辑描述}
- **新方法**: 未找到对应实现
- **建议**: {补全方案}

### 迁移完成度
- 共 {N} 个逻辑块：✅已迁移 {N} | ✅基类覆盖 {N} | 🔕已注释 {N} | ❓遗漏 {N} | 📋待迁移 {N}
````

---

## 🧮 功能7: 两文件逻辑深度对比 (`--logic-diff`)

### 目标
对**任意两个文件**（不区分新老，可以是两个新文件、两个同类模块的实现文件等）进行深度逻辑对比，找出相同点、差异点和特殊处理。

### 适用场景
- 对比两个模块的同类实现（如 T044 的 Submit vs T001 的 Submit）
- 对比重构前后的两个版本
- 找出某模板特有的业务逻辑

### 执行流程

**Step 1: 读取两个文件并分析结构**
- 提取文件A、文件B的类声明、继承关系、字段、方法列表
- 建立方法名对应关系（同名方法直接对比，不同名方法按功能推断）

**Step 2: 方法维度对比**
- 逐方法分析：相同方法名的实现差异
- 独有方法：文件A有但文件B没有，反之亦然

**Step 3: 业务逻辑特征提取**
- 提取每个文件的业务特征（特殊字段处理、特殊校验等）

### 输出格式

````markdown
## 🧮 逻辑深度对比: `{文件A名}` vs `{文件B名}`

### 文件概览
| 项 | 文件A | 文件B |
|----|-------|-------|
| 路径 | `{路径A}` | `{路径B}` |
| 总行数 | {N} 行 | {N} 行 |
| 继承自 | `{基类A}` | `{基类B}` |
| 方法数 | {N} 个 | {N} 个 |

### 方法对比矩阵
| 方法名 | 文件A | 文件B | 差异等级 |
|-------|-------|-------|--------|
| `validate()` | L{XX}-L{XX} | L{XX}-L{XX} | 🟡 部分差异 |
| `saveClaimHead()` | L{XX}-L{XX} | — | 🔵 仅A有 |
| `preProcess()` | — | L{XX}-L{XX} | 🔵 仅B有 |
| `buildDto()` | L{XX}-L{XX} | L{XX}-L{XX} | 🟢 基本相同 |

差异等级: 🟢完全相同 🟡部分差异 🔴逻辑差异大 🔵仅一方有

### 核心差异分析

#### 差异1: `{方法名}()` — {差异等级}
**文件A实现** (L{XX}-L{XX}):
- {逻辑要点1}
- {逻辑要点2}

**文件B实现** (L{XX}-L{XX}):
- {逻辑要点1}
- {特殊处理: {描述}}

**关键差异**:
| 维度 | 文件A | 文件B |
|------|-------|-------|
| 校验逻辑 | {描述} | {描述} |
| 数据处理 | {描述} | {描述} |
| 异常处理 | {描述} | {描述} |

### 文件A特有逻辑
- {描述A独有的业务逻辑}

### 文件B特有逻辑
- {描述B独有的业务逻辑}

### 共同模式
- {描述两者共同的实现模式}

### 分析结论
{综合评估：两个实现的相似度、差异原因（业务差异/重构改进/Bug修复等）}
````

---

## ⚡ 功能8: 两方法逻辑深度对比 (`--method-diff`)

### 目标
对**任意两个方法**进行最细粒度的逻辑对比，逐语句分析差异，找出潜在 Bug 和改进点。

### 适用场景
- 对比同一方法在不同模块的实现差异
- 排查某方法重构后是否有逻辑遗漏
- 寻找某模板特有的业务逻辑处理

### 执行流程

**Step 1: 精确提取两个方法的完整方法体**
- 方法A: `{文件路径A}` 中的 `{方法名}()`，行号 L{XX}-L{XX}
- 方法B: `{文件路径B}` 中的 `{方法名}()`，行号 L{XX}-L{XX}

**Step 2: 语句级别对比**
- 对齐两个方法的语句序列
- 标注：相同语句 / 语义等价语句 / 差异语句 / 独有语句

**Step 3: 语义等价性分析**
- 即使写法不同，分析是否语义等价（如 `a.equals(b)` vs `Objects.equals(a,b)`）
- 标注语义差异（执行结果不同）

### 输出格式

````markdown
## ⚡ 方法逻辑深度对比

### 对比目标
- **方法A**: `{文件A名}#{方法名A}()` (L{XX}-L{XX}, {N}行)
- **方法B**: `{文件B名}#{方法名B}()` (L{XX}-L{XX}, {N}行)

### 语句级对比（Side-by-Side）

| # | 方法A (行) | 方法A 代码 | 等价性 | 方法B (行) | 方法B 代码 |
|---|-----------|-----------|-------|-----------|----------|
| 1 | L{XX} | `if (claimId == null)` | 🟢等价 | L{XX} | `if (claimId == null)` |
| 2 | L{XX} | `claim.setStatus(1)` | 🟡语义差异 | L{XX} | `claim.setStatus(StatusEnum.DRAFT.getCode())` |
| 3 | L{XX}-L{XX} | `// 金额计算逻辑` | 🔴逻辑差异 | — | (无对应) |
| 4 | — | (无对应) | 🔵仅B有 | L{XX} | `validateBudget(claim)` |

等价性标记: 🟢完全等价 🟡语义差异(但结果相同) 🔴逻辑差异(结果不同) 🔵仅一方有

### 关键差异详解

#### 差异1: 第{N}语句 — {差异简述}
- **方法A** (L{XX}): `{代码}`
- **方法B** (L{XX}): `{代码}`
- **差异类型**: 🔴 逻辑差异 / 🟡 语义差异
- **影响分析**: {此差异对业务结果的影响}
- **建议**: {是否需要同步修复}

### 方法A特有逻辑
| 行号 | 逻辑描述 | 重要性 | 建议 |
|------|---------|-------|------|
| L{XX} | {描述} | 🔴高 / 🟡中 / 🟢低 | {建议} |

### 方法B特有逻辑
| 行号 | 逻辑描述 | 重要性 | 建议 |
|------|---------|-------|------|
| L{XX} | {描述} | {重要性} | {建议} |

### 对比结论
- **相似度**: {N}%
- **逻辑等价语句**: {N}/{总语句数}
- **潜在 Bug**: {N} 处（需要立即处理）
- **建议同步**: {N} 处（建议参考对方实现）
- **综合评估**: {两个方法的总体差异评价}
````

---

## ⚠️ 强制约束

### 对比时必须遵守
1. **精确行号**: 所有引用必须有精确文件路径和行号（如 `L47-L89`）
2. **不推测**: 没有读到文件内容前，不推测逻辑
3. **省 Token**: 每次读文件前先说明为什么要读，避免重复读取
4. **分步确认**: 如果用户只指定了 `--step X`，只分析该步骤

### 输出格式规范
- 必须使用 Markdown 表格展示对比结果
- 状态标记: ✅已迁移 ⚠️有疑问 ❌Bug ❓遗漏 🔕已注释
- 路径使用反引号包裹
- 代码片段使用 ` ```java ` 包裹

### 常见迁移陷阱（必须检查）
1. **Insert+Update 合并**: 老代码的 `InsertT{XXX}ClaimService` 和 `UpdateT{XXX}ClaimService` 都要看
2. **Load 多文件合并**: `LoadAllT{XXX}Service` + `ViewT{XXX}ClaimService` + `ViewT{XXX}ClaimLineService` 全部合并到新 Load
3. **gd 前缀忽略**: 老代码 `gd/GdViewT{XXX}Service` 等 gd 前缀类不迁移
4. **已注释代码**: 老代码中大量已注释的代码不需要迁移，但要标注 `🔕已注释`
5. **ClaimTemplateEnum**: 新代码 itemId 必须使用枚举，不允许硬编码字符串
6. **父类实现**: 如果基类已实现，子类不要重复实现（标注 `✅基类实现`）
7. **@Resource vs @Autowired**: 新代码统一使用 `@Resource`
8. **executeEnd 禁止重写**: Callback 中 `executeEnd` 在某些模板（T045等）禁止重写

---

## 🗂️ 资源文件管理规范

### 资源目录说明

以下目录是 skill 的配套资源，随 skill 一起维护和更新：

| 目录 | 说明 | 维护方式 |
|------|------|--------|
| `references/` | 老代码结构、新代码结构等参考文档 | 📝 可随 skill 升级一起更新 |
| `templates/` | 输出报告模板、代码模板 | 📝 可随 skill 升级一起更新 |
| `scripts/` | 辅助脚本（如批量对比脚本） | 📝 可随 skill 升级一起更新 |
| `assets/` | 图片、附件等静态资源 | 📝 可随 skill 升级一起更新 |

### 使用场景区分

| 场景 | 对资源目录的操作权限 |
|------|--------------------|
| **更新/维护 skill 本身** | ✅ 可以读写、修改、新增、删除资源文件 |
| **执行分析任务**（用户调用 skill 分析代码时） | ⛔ 只读，禁止向资源目录写入任何内容 |

### 执行任务时的输出规则

当用户调用 `--compare`、`--file-migrate`、`--logic-diff` 等命令执行分析任务时：

1. **只读资源目录**: references/、templates/、scripts/、assets/ 仅作为参考读取，不写入
2. **输出隔离**: 所有生成的报告、分析结果，写入到 `output/` 目录或用户指定的目标路径
3. **路径校验**: 文件写入操作前，确认目标路径不是上述资源目录

### 允许写入的目录（执行任务时）

- `output/` — 生成的对比报告、分析结果
- 用户项目代码目录（用户明确指定时）

---

## 📁 参考资料

### references/
- **老代码结构**: [references/old-code-structure.md](references/old-code-structure.md)
- **新代码结构**: [references/new-code-structure.md](references/new-code-structure.md)

### templates/
- **对比报告模板** (--compare): [templates/compare-report.md](templates/compare-report.md)
- **Bug检查报告模板** (--bug-check): [templates/bug-check-report.md](templates/bug-check-report.md)
- **文件迁移分析模板** (--file-migrate): [templates/file-migrate-report.md](templates/file-migrate-report.md)
- **方法迁移分析模板** (--method-migrate): [templates/method-migrate-report.md](templates/method-migrate-report.md)
- **逻辑对比报告模板** (--logic-diff): [templates/logic-diff-report.md](templates/logic-diff-report.md)
- **方法对比报告模板** (--method-diff): [templates/method-diff-report.md](templates/method-diff-report.md)

### scripts/
- **老代码文件清单**: [scripts/batch-list-old-files.sh](scripts/batch-list-old-files.sh)
- **新代码文件清单**: [scripts/batch-list-new-files.sh](scripts/batch-list-new-files.sh)
- **快速搜索**: [scripts/quick-search.sh](scripts/quick-search.sh)

### assets/
- **方法映射表**: [assets/method-mapping.md](assets/method-mapping.md) — 老→新方法/文件映射规则
- **模板模块映射**: [assets/template-module-mapping.md](assets/template-module-mapping.md) — T编号→模块归属
- **状态标记图例**: [assets/status-markers.md](assets/status-markers.md) — 所有输出标记语义定义

### 外部参考
- **迁移工具**: `transform-claim` skill（执行实际迁移）
- **项目规范**: `/ai-spec/rules/agents.md`
- **老代码路径**: `yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/`
- **新代码基类路径**: `fssc-claim-service/claim-common/claim-common-service/src/main/java/com/yili/claim/common/service/claim/service/impl/`
- **已迁移参考**: `fssc-claim-service/claim-ptp/` (T010, T012等)、`fssc-claim-service/claim-eer/`、`fssc-claim-service/claim-otc/`
