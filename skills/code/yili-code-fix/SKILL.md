---
name: yili-code-fix
description: 代码修复引擎，基于 Bug 描述+评论对比老新代码，定位遗漏逻辑，判断前后端，自动修复后端代码。当用户需要根据 Coding Bug 对比老新代码、找出迁移遗漏、自动修复后端 Bug 时使用。
---
# Yili Code Fix (代码修复引擎)
@author: sevenxiao

## 概述

此 skill 专注于**根据 Bug 描述对比老新代码，找出迁移遗漏并修复**。

核心能力:
1. **解析 Bug** - 从 Bug 描述+评论中提取关键信息（模板编号、功能模块、问题现象）
2. **定位老代码** - 在老代码仓库中精准定位对应的基线代码
3. **定位新代码** - 在新代码仓库中找到对应的迁移代码
4. **对比分析** - 逐方法对比老新代码，找出遗漏逻辑
5. **分类判定** - 判断遗漏属于前端还是后端
6. **修复后端** - 按项目规范修复后端代码
7. **编译验证** - 编译确认修复无误

## 外部依赖

此 skill 不需要额外安装外部 skill，但会复用以下已有 skill:

| 复用 Skill | 位置 | 用途 |
|------------|------|------|
| `compare-transform` | `ai-spec/skills/code/compare-transform/` | 复用 `--bug-check` 和 `--locate` 能力 |
| `transform-claim` | `ai-spec/skills/code/transform-claim/` | 参考迁移步骤映射表定位老代码 |
| `coding-bug-ops` | `ai-spec/skills/code/coding-bug-ops/` | 前端 Bug 时添加评论 + 转派前端处理人 |
| `xlsx` | 系统 skill | 读取排期表查找前端负责人 |

---

## 使用方式

```bash
# 从 Bug 上下文分析并修复
/skill yili-code-fix analyze "<bug上下文文本>"

# 指定模板编号分析
/skill yili-code-fix analyze --template T044 "<bug描述>"

# 只分析不修复（输出分析报告）
/skill yili-code-fix analyze --dry-run "<bug上下文文本>"
```

**通常由 `bug-fix-pipeline` 调用，也可独立使用。**

---

## 代码仓库路径

| 仓库 | 路径 | 说明 |
|------|------|------|
| 新后端 | `fssc-claim-service/` | Spring Boot 3 + MyBatis Plus |
| 新前端 | `fssc-web/` + `fssc-web-framework/` | Vue 2 + Setaria |
| 老后端 | `yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/` | Struts + JDBC |
| 老前端 | `yldc-caiwugongxiangpingtai-fsscYR-master/WebRoot/` | JSP + JS |

### 新后端模块映射

| 业务模块 | 新代码路径 |
|----------|-----------|
| TR (差旅报账) | `fssc-claim-service/claim-tr/` |
| OTC (杂项报账) | `fssc-claim-service/claim-otc/` |
| PTP (采购报账) | `fssc-claim-service/claim-ptp/` |
| EER (费用报账) | `fssc-claim-service/claim-eer/` |
| FA (资产报账) | `fssc-claim-service/claim-fa/` |
| RTR (应收报账) | `fssc-claim-service/claim-rtr/` |
| BASE (公共基础) | `fssc-claim-service/claim-base/` |
| COMMON (通用) | `fssc-claim-service/claim-common/` |

### 老后端代码路径

```
yldc-caiwugongxiangpingtai-fsscYR-master/
  └── src/com/ibm/gbs/efinance/business/ylService/claim/T{XXX}/
      ├── NewT{XXX}ClaimService.java          → 新建报账单头
      ├── NewT{XXX}ClaimLineService.java      → 新建报账单行
      ├── InsertT{XXX}ClaimService.java       → 保存报账单头(新增)
      ├── UpdateT{XXX}ClaimService.java       → 保存报账单头(更新)
      ├── InsertT{XXX}ClaimLineService.java   → 保存报账单行(新增)
      ├── UpdateT{XXX}ClaimLineService.java   → 保存报账单行(更新)
      ├── DeleteT{XXX}ClaimService.java       → 删除报账单头
      ├── DeleteT{XXX}ClaimLinesService.java  → 删除报账单行
      ├── LoadAllT{XXX}Service.java           → 加载报账单
      ├── ViewT{XXX}*.java                    → 查看报账单(多个文件)
      ├── CallBackT{XXX}Service.java          → 回调
      ├── SubmitT{XXX}Service.java            → 提交
      └── ListAllT{XXX}ClaimLinesService.java → 加载行列表
```

### 老前端代码路径

```
yldc-caiwugongxiangpingtai-fsscYR-master/
  ├── WebRoot/newPages/efinance/claim/T{XXX}/  → JSP 页面
  └── WebRoot/easjs/                           → JS 脚本
```

---

## 核心流程

### Step 1: 解析 Bug 描述 + 评论

**输入**: 从 `coding-bug-ops` 获取的 Bug 完整上下文（描述 + 评论）

**处理**:
1. 提取报账单模板编号:
   - 标签: "049杂项采购报账单" → T049
   - 标题: "T044xxx异常" → T044
   - 描述/评论: 搜索 `T\d{3}` 模式
2. 提取功能模块:
   - 关键词映射: "差旅" → TR, "杂项" → OTC, "采购" → PTP, "费用" → EER, "资产" → FA, "应收" → RTR
3. 提取问题现象:
   - "保存失败" / "字段不显示" / "金额计算错误" / "状态不对" / "页面报错"
4. **从评论中提取关键信息**:
   - 复现步骤
   - 补充说明（如"老代码在 InsertT044ClaimService L120 有一段特殊处理"）
   - 已尝试的修复思路
   - 测试人员的额外反馈

**输出**:
```markdown
### Bug 分析
- 模板编号: T{XXX}
- 业务模块: {TR/OTC/PTP/EER/FA/RTR}
- 问题现象: {一句话描述}
- 涉及功能: {New/Save/Delete/Load/Submit/Callback}
- 关键线索: {从描述+评论中提取的关键信息}
```

### Step 2: 定位老代码基线

**策略**: 先定位，后阅读。精准定位避免浪费 Token。

**执行**:
1. 根据 Step 1 的模板编号，直接定位老代码目录:
   ```
   yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{XXX}/
   ```
2. 列出目录内文件
3. 根据 Bug 涉及的功能，精准读取对应文件:
   - 保存相关 → `InsertT{XXX}ClaimService.java` + `UpdateT{XXX}ClaimService.java`
   - 提交相关 → `SubmitT{XXX}Service.java`
   - 加载相关 → `LoadAllT{XXX}Service.java` + `ViewT{XXX}*.java`
   - 新建相关 → `NewT{XXX}ClaimService.java`
4. 记录: 老代码文件路径、对应方法、关键逻辑行数

**复用 compare-transform**: 可用 `--locate` 功能快速定位:
```bash
/skill compare-transform --locate <关键词>
```

### Step 3: 定位新代码

**执行**:
1. 根据业务模块确定新代码目录:
   ```
   fssc-claim-service/claim-{module}/claim-{module}-service/src/main/java/com/yili/claim/{module}/claim/t{xxx}/
   ```
2. 列出目录，找到对应的 Service 实现类
3. 新老代码类名对照 (参考 transform-claim 映射表):

| 老代码 | 新代码 |
|--------|--------|
| `NewT{XXX}ClaimService` | `T{XXX}NewClaimServiceImpl` |
| `Insert/UpdateT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` |
| `DeleteT{XXX}ClaimService` | `T{XXX}DeleteClaimServiceImpl` |
| `LoadAllT{XXX}Service` + `ViewT{XXX}*` | `T{XXX}LoadClaimServiceImpl` |
| `CallBackT{XXX}Service` | `T{XXX}CallBackClaimServiceImpl` |
| `SubmitT{XXX}Service` | `T{XXX}SubmitClaimServiceImpl` |

4. 老前端 → 新前端:
   ```
   老: yldc-.../WebRoot/newPages/efinance/claim/T{XXX}/
   新: fssc-web/src/page/claim/**/T{XXX}/
   ```

### Step 4: 对比分析 (Old vs New Decision Rule)

**核心**: 逐方法对比老新代码逻辑，找出遗漏。

**检查点清单**:

| 检查项 | 说明 |
|--------|------|
| 分支条件 | if/else/switch 是否完整保留 |
| 默认值 | 字段默认值是否一致 |
| 状态流转 | 状态码/枚举是否完整 |
| 过滤条件 | 查询过滤是否遗漏 |
| 特殊处理 | 特定模板的特殊逻辑是否保留 |
| SQL条件 | 查询条件是否一致 |
| 参数传递 | 方法参数是否完整 |
| 异常处理 | try/catch/throw 是否保留 |
| 事务边界 | 事务注解是否正确 |

**执行**:
1. 读取老代码关键方法
2. 读取新代码对应方法
3. 逐行对比关键逻辑
4. 标注每个差异是 ✅已迁移 / ❌遗漏 / ⚠️有疑问

**输出**: 遗漏清单
```markdown
### 遗漏清单

| 编号 | 老代码位置 | 逻辑描述 | 类型 | 新代码位置 |
|------|-----------|---------|------|-----------|
| 1 | InsertT044 L120-L135 | 金额字段校验逻辑 | 后端 | 未迁移 |
| 2 | T044.jsp L50-L65 | 字段显示/隐藏控制 | 前端 | 未迁移 |
```

### Step 5: 分类判定

**判定规则**:

```
遗漏逻辑的来源文件路径
    │
    ├── yldc-.../src/com/ibm/gbs/**/*.java  → 后端 Bug → 修复 (Step 6)
    ├── yldc-.../WebRoot/**/*.jsp            → 前端 Bug → 标注 + 转派前端
    ├── yldc-.../WebRoot/**/*.js             → 前端 Bug → 标注 + 转派前端
    └── 同时涉及前后端                        → 只修后端, 前端部分标注 + 转派
```

**前端 Bug 处理流程**:

当判定为前端 Bug 时，不只是标注，还要执行转派:

```
1. 添加评论: coding-bug-ops.add-comment
   "【AI分析】前端问题, 对应老代码 xxx, 新框架不修改"

2. 查找前端负责人:
   - 读取 ai-spec/skills/code/coding-bug-ops/references/fssc-schedule.xlsx
   - 使用 xlsx skill 读取 "FSSC系统功能整体排期" sheet
   - 用 Bug 模块关键词（模板编号、功能名称）匹配，找到前端负责人
   - 如果本地文件不存在，提示用户手动下载
     (来源: https://www.kdocs.cn/l/cpSC0fYjdOJn)

3. 转派: coding-bug-ops.reassign(bug-id, --to <前端负责人>)
   - 找到 → 直接转派
   - 找不到 → ⏸️ 暂停询问用户指定

4. 跳过后续 Step 6-7，直接输出分析报告
```

**前端 Bug 输出**:
```markdown
**[前端 Bug - 已转派]**
对应老代码: `WebRoot/newPages/efinance/claim/T{XXX}/xxx.jsp` L{行号}
遗漏逻辑: {描述}
前端负责人: {从排期表查到的人名}
处理方式: 已添加评论 + 转派前端处理人
```

**后端 Bug**: 进入 Step 6

### Step 6: 修复后端代码

**强制遵守的规范**:

1. **分层架构** (来自 agents.md):
   - Controller → Business → DO Service → Mapper
   - 禁止跨层调用
   - DO Service 禁止 if/SQL/业务逻辑

2. **迁移原则** (来自 user-rules.md):
   - 不修改代码，需要变更请重写
   - 存在父类逻辑直接调用
   - 在新代码中标注老代码对应行数
   - 逻辑要完整，不要遗漏

3. **技术栈规范**:
   - 使用 `@Slf4j` + `@Resource`
   - 使用 Lombok 注解
   - 使用 MapStruct (禁止反射复制)
   - 使用 MyBatis Plus `LambdaQueryWrapperX`
   - 金额使用 BigDecimal
   - 时间使用 LocalDateTime

4. **修复代码格式**:
   ```java
   /**
    * {方法说明}
    * 老代码: {老文件名} L{行号}-L{行号}
    * Bug修复: #{bug-id}
    *
    * @author sevenxiao
    */
   ```

5. **复用 compare-transform** 的 `--bug-check` 辅助检查:
   ```bash
   /skill compare-transform T{XXX} --bug-check
   ```

### Step 7: 编译验证

```bash
# 定位到项目根目录
cd fssc-claim-service

# 编译修改的模块
mvn compile -pl claim-{module}/claim-{module}-service -am -T 1C

# 如果编译失败, 自动修复并重试 (最多 3 次)
```

**常见编译问题**:
- import 缺失 → 添加 import
- 类型不匹配 → 检查 DTO/DO 转换
- 方法签名不一致 → 检查父类方法
- Mapper 方法不存在 → 添加 Mapper 方法

### Step 8: 完成检查清单

修复完成后必须逐项确认:

- [ ] 说明用了哪段老代码作为基线 (文件路径+行号)
- [ ] 确认修复后逻辑与老代码一致
- [ ] 确认没有跨层调用
- [ ] 确认没有在 DO Service 写 if 逻辑
- [ ] 确认事务注解正确 (`@Transactional(rollbackFor = Exception.class)`)
- [ ] 确认 import 正确、无遗漏
- [ ] 确认使用 `@Resource` 而非 `@Autowired`
- [ ] 确认使用 Lombok 注解
- [ ] 确认没有魔法数字
- [ ] 确认编译通过

---

## 输出格式

### 分析报告 (Step 1-5 输出)

```markdown
## Bug #{id} 分析报告

### 基本信息
- 模板编号: T{XXX}
- 业务模块: {module}
- 问题现象: {描述}

### 老代码基线
- 文件: `{路径}`
- 关键方法: `{方法名}` L{行号}-L{行号}
- 逻辑描述: {描述}

### 新代码位置
- 文件: `{路径}`
- 对应方法: `{方法名}` L{行号}-L{行号}

### 遗漏清单
| 编号 | 来源 | 老代码位置 | 逻辑描述 | 类型 |
|------|------|-----------|---------|------|
| 1 | {文件} L{行号} | {描述} | 后端/前端 |

### 修复方案
{修复思路描述, 等待用户确认后执行}

### 前端标注 (如有)
{前端 Bug 的标注信息 + 转派情况}
- 前端负责人: {人名}
- 已转派: 是/否
```

### 修复报告 (Step 6-8 输出)

```markdown
## Bug #{id} 修复报告

### 修复文件
- `{修改的文件路径}` : {修改说明}

### 对应老代码
- `{老代码文件}` L{行号}-L{行号}

### 修复内容
{修复的具体逻辑描述}

### 检查清单
- [x] 老代码基线标注
- [x] 逻辑一致性
- [x] 分层规范
- [x] 编译通过

### 编译结果
{编译输出}
```

---

## 强制约束

1. **先分析再修复**: 必须先输出分析报告，等待用户确认后才能修改代码
2. **精确行号**: 所有引用必须有精确文件路径和行号
3. **不推测**: 没有读到的代码不推测其逻辑
4. **标注来源**: 修复的代码必须标注对应的老代码行号，老代码逻辑找对应逻辑才能改新代码，不能照搬其他类似业务，可能逻辑就不一样
5. **评论信息不可忽略**: Bug 描述和评论都要分析，评论中经常有关键线索
6. **编译必须通过**: 修复后必须编译验证

## 参考

- 老代码目录映射: [references/old-code-map.md](references/old-code-map.md)
- 新代码目录映射: [references/new-code-map.md](references/new-code-map.md)
- 修复检查清单: [references/fix-checklist.md](references/fix-checklist.md)
- 修复报告模板: [templates/fix-report.md](templates/fix-report.md)
- 对比分析器: `ai-spec/skills/code/compare-transform/skill.md`
- 迁移转换器: `ai-spec/skills/code/transform-claim/skill.md`
- Coding Bug 操作: `ai-spec/skills/code/coding-bug-ops/SKILL.md`
- 前端人员排期表: `ai-spec/skills/code/coding-bug-ops/references/fssc-schedule.xlsx`
- 项目规范: `.qoder/rules/agents.md`
- 个人偏好: `.qoder/rules/user-rules.md`
