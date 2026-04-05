---
name: sit-verify-analyze
description: SIT 验证后分析判断器。根据 SIT 测试结果分析 Bug 的真实原因（后端未修复/前端问题/数据问题），并路由到对应处理流程：重新修复、转派前端、标记已修复待验证。被 bug-fix-pipeline 在 SIT 验证步骤后调用。
allowed-tools: Bash(browser-use:*), Bash(curl:*)
---
# SIT Verify Analyze (SIT 验证后分析判断器)
@author: sevenxiao

## 概述

此 skill 在 **SIT 验证步骤之后** 被调用，负责分析测试结果并路由到正确的后续流程。

核心判断逻辑:

```
SIT 验证结果
  │
  ├─ 通过 → 后端修复成功
  │   ├─ add-comment (修复说明)
  │   ├─ update-status → "待验证"
  │   └─ reassign → 发起人
  │
  └─ 未通过 → 分析原因
      │
      ├─ API 返回正确 + 页面展示错误 → 前端问题
      │   ├─ add-comment (后端OK, 前端问题)
      │   ├─ update-remark (备注说明)
      │   └─ reassign → 前端处理人
      │
      ├─ API 返回错误 → 后端未修复
      │   ├─ add-comment (未修复原因分析)
      │   └─ 重新进入修复流程 (yili-code-fix)
      │
      └─ 其他原因 (环境/数据/配置)
          └─ add-comment (分析结果) + 等待人工处理
```

## 使用方式

```bash
# 分析 SIT 验证结果（通常由 bug-fix-pipeline 调用）
/skill sit-verify-analyze --bug 4686 --result fail

# 带 API 对比数据分析
/skill sit-verify-analyze --bug 4686 --api-ok --ui-fail

# 全部通过
/skill sit-verify-analyze --bug 4686 --result pass
```

---

## 分析流程

### Step 1: 确定验证结果类型

| 验证情况 | API 数据 | 页面展示 | 判定 |
|----------|---------|---------|------|
| 全部通过 | 正确 | 正确 | **后端修复成功** |
| API 正确，页面错误 | 正确 | 错误/缺失 | **前端问题** |
| API 错误 | 错误/缺失 | 不关心 | **后端未修复** |
| API 超时/500 | 异常 | 不关心 | **环境/部署问题** |

### Step 2: 验证 API 数据（curl，不需要浏览器）

通过 curl 直接验证后端接口返回，**无需浏览器**，避免 DOM 交互不稳定问题：

```bash
# 1. 检查 SIT Cookie 缓存是否有效
#    Cookie 文件: /tmp/sit-cookies.txt
#    如果文件存在且未过期（30分钟内），直接复用，跳到步骤 2

# 1a. Cookie 不存在或过期 → 重新登录获取
curl -v -X POST http://pri-fssc-web-sit.digitalyili.com/api/config/sys/login \
  -H "Content-Type: application/json" \
  -d '{"usernum":"fsscadmin","password":"2"}' \
  -c /tmp/sit-cookies.txt

# 2. 调用相关接口验证数据（复用缓存 Cookie）
curl -s -X GET "http://pri-fssc-web-sit.digitalyili.com/api/config/<path>" \
  -b /tmp/sit-cookies.txt | python3 -m json.tool

# 3. 检查返回数据中修复的字段是否正确
```

**SIT Cookie 缓存策略**:
- 缓存文件: `/tmp/sit-cookies.txt`
- 有效期: 30 分钟内复用，不重复登录
- 过期判断: `find /tmp/sit-cookies.txt -mmin -30` 有结果则未过期
- 所有 curl 验证共享同一份 Cookie

**判断标准**:
- API 返回的修复字段有值且正确 → API 正确
- API 返回的修复字段为空或错误 → API 错误（后端未修复）

### Step 2.5: [可选] 数据库验证（db-query）

当 API 返回错误时，可通过 `db-query` 查库进一步精确定位问题根因：

```
API 返回错误 → db-query.query 查库对比
  │
  ├─ 库里有正确数据 + API 没返回
  │   → 后端查询/映射逻辑有问题（SQL/MyBatis/DO 转换）
  │   → 重点检查: Mapper.xml, ServiceImpl 中的查询方法
  │
  ├─ 库里没有数据
  │   → 后端写入逻辑有问题（数据根本没存进去）
  │   → 重点检查: save/insert 方法, 事务是否提交
  │
  └─ 库里数据值不对
      → 数据本身有问题（写入时值就不对，或被其他逻辑覆盖）
      → 重点检查: 字段赋值逻辑, 是否有触发器/定时任务修改
```

**使用方式**:

```bash
# 通过 db-query 的 run_query.sh 在 SIT 环境查库
./run_query.sh --env sit "SELECT * FROM T_PROC_CLAIM_HEAD WHERE CLAIM_NO = '<报账单号>'"

# 或使用 db-query 的 check-data 能力，自动根据 Bug 上下文生成查询
db-query.check-data(bug-context)
```

**注意**: 此步骤为可选增强，不改变主流程判断逻辑。仅在需要精确定位"后端未修复"根因时使用。

### Step 3: 验证页面展示（浏览器，仅此步骤需要）

使用 browser-use 在 SIT 页面操作并检查（**只有此步骤需要浏览器**，Step 2 用 curl）：

```bash
# 1. 登录 SIT（认证顺序: Cookie 文件 → Profile → 账号密码）
#    优先导入 config/sit-cookies.json
browser-use cookies import config/sit-cookies.json
browser-use open "http://pri-fssc-web-sit.digitalyili.com"
# → 如果 Cookie 失效，降级到 Profile 或账号密码登录

# 2. 导航到 Bug 对应页面

# 3. 执行 Bug 复现步骤

# 4. 检查页面展示是否正确
browser-use state
browser-use screenshot sit-verify-result.png
```

**判断标准**:
- 页面展示与 API 数据一致 → 页面正确
- 页面展示为空/旧值，但 API 有正确数据 → 前端问题

---

## 路由决策

### 路由 A: 后端修复成功（全部通过）

```
执行动作:
  1. coding-bug-ops.add-comment(bug-id, "【SIT验证通过】...")
  2. coding-bug-ops.update-status(bug-id, "待验证")
  3. coding-bug-ops.reassign(bug-id, --to-reporter)
  4. 截图存证

评论模板:
  【SIT验证通过】
  修复内容: <修复说明>
  修改文件: <文件列表>
  验证步骤: <操作步骤>
  验证结果: API返回正确，页面展示正确
  部署环境: SIT
  截图: 见附件
```

### 路由 B: 前端问题（API 正确，页面错误）

```
执行动作:
  1. coding-bug-ops.add-comment(bug-id, "【后端已修复，前端问题】...")
  2. coding-bug-ops.update-remark(bug-id, "后端已修复，前端展示问题")
  3. coding-bug-ops.reassign(bug-id, --to <前端处理人>)
  4. coding-bug-ops.update-status(bug-id, "待处理")  // 重置为待处理
  5. 截图存证

评论模板:
  【后端已修复，前端展示问题】
  后端修复: <修复说明>
  API验证: 接口返回数据正确（字段: xxx = yyy）
  页面问题: <具体描述哪里展示不正确>
  前端页面: <页面路径/组件>
  建议: 请前端检查页面是否正确读取了对应字段
  截图: 见附件

备注:
  【后端OK】API返回正确，前端展示未更新，已转前端处理
```

### 路由 C: 后端未修复（API 错误）

```
执行动作:
  1. coding-bug-ops.add-comment(bug-id, "【SIT验证未通过】...")
  2. [可选] db-query.query → 查库精确定位根因:
     - 库里有正确数据 + API 没返回 → 后端查询逻辑问题
     - 库里没数据 → 后端写入逻辑问题
     - 库里数据不对 → 数据本身问题
  3. 分析未修复原因:
     a. 代码没有部署成功 → 检查 CI 构建状态
     b. 修复逻辑有误 → 回到 yili-code-fix 重新分析修复
     c. 修复不完整 → 补充修复
  3. ⏸️ 通知用户，等待决策:
     - "重新修复" → 回到 pipeline Step 2.2 (分析)
     - "人工处理" → 暂停流水线

评论模板:
  【SIT验证未通过 - 后端未修复】
  验证步骤: <操作步骤>
  期望结果: <期望数据>
  实际结果: <实际数据>
  初步分析: <可能原因>
  建议: 需要重新分析修复逻辑
```

### 路由 D: 环境/数据问题

```
执行动作:
  1. coding-bug-ops.add-comment(bug-id, "【SIT验证异常】...")
  2. ⏸️ 通知用户，等待人工排查

评论模板:
  【SIT验证异常 - 环境问题】
  异常类型: <接口超时/500/服务不可用>
  可能原因: 服务未启动/配置错误/数据库连接异常
  建议: 请检查 SIT 环境状态
```

---

## 前端处理人识别

当判定为前端问题时，需要确定转派给谁：

### 1. 从排期文档查找（首选）

```
1. 读取 ai-spec/skills/code/coding-bug-ops/references/fssc-schedule.xlsx
   - 来源: https://www.kdocs.cn/l/cpSC0fYjdOJn
   - 如果本地不存在，提示用户手动下载
2. 使用 xlsx skill 读取 "FSSC系统功能整体排期" sheet
3. 从 Bug 标签/标题提取模块关键词（如 "T044", "杂项采购"）
4. 在排期表中搜索匹配行，读取"前端负责人"列
5. 找到 → 直接转派
6. 找不到 → ⏸️ 询问用户
```

### 2. 从 Bug 详情获取线索（补充）

```bash
# 检查 Bug 标签/模块中是否有前端相关人员
# 检查 Bug 历史评论中是否有前端开发参与
# 检查 Bug 的创建人是否是前端测试人员
```

### 3. 无法确定时

如果无法确定具体前端处理人，执行以下操作:
1. 在评论中说明"需要转前端处理"
2. **⏸️ 暂停并询问用户**: "此 Bug 是前端问题，请指定转派给哪位前端开发？"
3. 用户指定后执行 reassign

---

## 与 Pipeline 集成

此 skill 被 `bug-fix-pipeline` 在 **Step 2.9 (SIT 验证)** 之后调用:

```
bug-fix-pipeline
  └─ Step 2.9: ui-smoke-test → SIT 验证
  └─ Step 2.10: sit-verify-analyze → 分析结果
      ├─ 通过 → 更新状态 + 转派发起人 → Step 2.11 记录结果
      ├─ 前端问题 → 添加评论 + 转派前端 → Step 2.11 记录结果
      ├─ 后端未修复 → 回到 Step 2.2 重新分析修复
      └─ 环境问题 → ⏸️ 等待人工
```

---

## 强制约束

1. **API 优先**: 判断修复是否生效以 API 返回为准，不以页面展示为准
2. **截图存证**: 每个验证步骤都要截图
3. **评论完整**: Coding 评论必须包含验证步骤、期望/实际结果、截图
4. **不猜测**: 没有实际验证的数据不要推测结论
5. **人工兜底**: 无法自动判断时暂停询问用户
6. **转派确认**: 转派前端时如果无法确定具体人选，必须询问用户
7. **重试限制**: 后端未修复最多自动重试 1 次，之后交给用户决策

## 参考

- Coding 操作: `ai-spec/skills/code/coding-bug-ops/SKILL.md`
- SIT 测试: `ai-spec/skills/code/bug-fix-cycle/ui-smoke-test/SKILL.md`
- 代码修复: `ai-spec/skills/code/yili-code-fix/SKILL.md`
- 本地测试: `ai-spec/skills/code/local-api-test/SKILL.md`
- 数据库查询: `ai-spec/skills/code/bug-fix-cycle/db-query/SKILL.md`
- Pipeline: `ai-spec/skills/code/bug-fix-pipeline/SKILL.md`
