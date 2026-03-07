---
name: compare-transform
description: 报账单老新代码对比分析器。对比老代码（yldc-caiwugongxiangpingtai-fsscYR-master）与新框架代码（fssc-claim-service），输出对比报告、检测迁移Bug、定位代码上下文、提供省钱策略。当用户需要对比老新代码差异、检查迁移是否有遗漏/Bug、或者想找某个功能在新代码中的位置时使用。
---
# Compare Transform Skill（报账单老新代码对比分析器）
@author: sevenxiao

## 📋 概述

此 skill 专注于**对比老代码与新框架迁移代码**，提供4大核心能力：

1. **`--compare`** 输出老新代码对比 Markdown 报告
2. **`--bug-check`** 检查新代码流程明显 Bug / 迁移遗漏
3. **`--save-cost`** 省钱策略（减少 Token 消耗的最优搜索路径）
4. **`--locate`** 输入新代码上下文，快速定位相关文件和逻辑

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

## 📁 参考资料

- **老代码结构**: [references/old-code-structure.md](references/old-code-structure.md)
- **新代码结构**: [references/new-code-structure.md](references/new-code-structure.md)
- **迁移工具**: `transform-claim` skill（执行实际迁移）
- **项目规范**: `/ai-spec/rules/agents.md`
- **老代码路径**: `yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/`
- **新代码基类路径**: `fssc-claim-service/claim-common/claim-common-service/src/main/java/com/yili/claim/common/service/claim/service/impl/`
- **已迁移参考**: `fssc-claim-service/claim-ptp/` (T010, T012等)、`fssc-claim-service/claim-eer/`、`fssc-claim-service/claim-otc/`
