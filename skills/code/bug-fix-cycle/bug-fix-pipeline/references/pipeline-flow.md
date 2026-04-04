# Pipeline 流程图和状态机（五阶段模式）

## 全流程总览

```
┌──────────────────────────────────────────────────────┐
│                    输入                                │
│  单 Bug: #bug-id    批量: --filter <url>              │
└──────────────┬───────────────────────┬────────────────┘
               │                       │
          单 Bug 模式             批量模式
               │                       │
               │            ┌──────────▼──────────┐
               │            │  Phase 1: 预采集     │
               │            │  Prefetch            │
               │            │  批量读取 Bug+截图   │
               │            └──────────┬──────────┘
               │                       │
               │            ┌──────────▼──────────┐
               │            │  Phase 2: 分诊台     │
               │            │  Triage              │
               │            │  用户排序+标记+确认  │
               │            └──────────┬──────────┘
               │                       │
               ▼                       ▼
        ┌──────────────────────────────────────┐
        │  Phase 3: 批量修复                    │
        │  Fix & Commit                          │
        │  逐个: 分析→确认→修复→编译→commit    │
        └──────────────────┬───────────────────┘
                           │
        ┌──────────────────▼───────────────────┐
        │  Phase 4: 统一推送                    │
        │  Push                                │
        │  pull --rebase → push                │
        └──────────────────┬───────────────────┘
                           │
        ┌──────────────────▼───────────────────┐
        │  Phase 5: 统一闭环                    │
        │  Finalize                            │
        │  CI构建 → SIT验证 → Coding操作        │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                      汇总报告
```

---

## Phase 1: 预采集状态机

```
┌─────────────┐
│  P1_INIT     │ 开始预采集
│  登录 Coding │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P1_LIST     │ 读取 Bug 列表
│  coding-bug  │
│  -ops        │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────┐
│  P1_DETAIL   │────▶│ 无更多Bug │──▶ P1_DONE
│  读取详情+   │     └──────────┘
│  评论+截图   │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
成功      失败
  │         │
  │         └──▶ 记录失败，继续下一个
  │
  ▼
保存到本地
  │
  └──▶ 下一个 Bug
       │
       ▼
┌─────────────┐
│  P1_DONE     │ 生成 prefetch-summary.json
│  关闭浏览器  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│P1_TEST_INDEX │ [可选] 解析测试用例索引
│test-case-ref │ → test-case-index.json
│  .parse      │ (已存在且未过期则跳过)
└─────────────┘
```

---

## Phase 2: 分诊台状态机

```
┌─────────────┐
│  P2_LOAD     │ 读取 prefetch-summary.json
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P2_CLASSIFY │ 初步分类（前端/后端/混合）
│              │ [可选] test-case-ref.lookup
│              │ → 匹配相关测试用例数量
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P2_PRESENT  │ 展示分诊表格
│  等待用户    │
└──────┬──────┘
       │
  ┌────┴────────────┐
  │                  │
  ▼                  ▼
调整               确认
  │                  │
  └─▶ 重新展示      │
                     ▼
              ┌─────────────┐
              │  P2_DONE     │ 生成 fix-queue.json
              └─────────────┘
```

---

## Phase 3: 批量修复状态机

```
┌─────────────┐
│  P3_LOAD     │ 读取 fix-queue.json
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│  P3_NEXT     │────▶│ 队列处理完毕  │──▶ P3_DONE
│  取下一个Bug │     └──────────────┘
└──────┬──────┘
       │
  ┌────┴────────────┬──────────────┐
  │                  │              │
  ▼                  ▼              ▼
action=fix     action=tag     action=skip
  │            -frontend           │
  │                  │              └──▶ 记录跳过 ──▶ P3_NEXT
  │                  │
  │                  └──▶ 准备评论草稿
  │                       查找前端负责人
  │                       记录结果 ──▶ P3_NEXT
  │
  ▼
┌─────────────┐
│P3_LOAD_TEST  │ [可选] test-case-ref.lookup
│  CASE        │ 加载相关测试用例参考
│              │ ⚠️ 仅供参考
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P3_ANALYZE  │ yili-code-fix.analyze
│  分析 Bug    │ [可选] db-query
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P3_PRESENT  │ 展示分析方案
│  等待确认    │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
确认      跳过
  │         │
  │         └──▶ 记录跳过 ──▶ P3_NEXT
  │
  ▼
┌─────────────┐
│  P3_FIX      │ yili-code-fix.fix
│  执行修复    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P3_COMPILE  │ mvn compile
│  编译验证    │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
通过      失败
  │         │
  │         └──▶ 重试(最多3次) ──▶ 失败则标注
  │
  ▼
┌─────────────┐
│P3_UNIT_TEST  │ [可选] fix-verify
│  单元测试    │ discover-tests + run-tests
│              │ verdict: PASS/WARN/FAIL/SKIP
└──────┬──────┘
       │
       ▼
┌─────────────┐
│P3_DATA_VERIFY│ [可选] fix-verify → db-query
│  数据验证    │ check-data + trace-branch
│              │ verdict: PASS/WARN/FAIL/SKIP
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P3_TEST     │ [可选] local-api-test
│  本地测试    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P3_COMMIT   │ git add + git commit
│  本地提交    │ fix(<module>): #<id> <标题>
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P3_REVIEW   │ self-improving-agent
│  单Bug复盘   │
└──────┬──────┘
       │
       ▼
记录修复结果
  │
  └──▶ P3_NEXT (下一个 Bug)
```

---

## Phase 4: 统一推送状态机

```
┌─────────────┐
│  P4_LOG      │ git log --oneline
│  展示commits │ 展示本批次所有 commit
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P4_REBASE   │ git pull --rebase
│  拉取+变基   │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
成功      冲突
  │         │
  │         └──▶ ⏸️ 用户手动解决
  │              → git rebase --continue
  ▼
┌─────────────┐
│  P4_CONFIRM  │ ⏸️ 用户确认 push
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P4_PUSH     │ git push
└──────┬──────┘
       │
       ▼
P4_DONE
```

---

## Phase 5: 统一闭环状态机

```
┌─────────────┐
│  P5_CI       │ coding-ci-deploy
│  触发CI构建  │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
成功      失败
  │         │
  │         └──▶ ⏸️ 通知用户，等待决策
  │              （Coding 操作不依赖 CI 成功）
  ▼
┌─────────────┐
│  P5_SIT      │ [可选] SIT 验证
│  (可选)      │ sit-smoke-test + sit-verify-analyze
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  P5_LOGIN    │ 打开 Coding 浏览器
│  登录 Coding │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│  P5_NEXT     │────▶│ 全部处理完毕  │──▶ P5_REPORT
│  取下一个Bug │     └──────────────┘
└──────┬──────┘
       │
  ┌────┴────────────┬──────────────┐
  │                  │              │
  ▼                  ▼              ▼
status=fixed   status=tag     status=skipped
  │            -frontend           │
  │                  │              └──▶ P5_NEXT
  │                  │
  │                  ├─ add-comment
  │                  ├─ reassign → 前端
  │                  └──▶ P5_NEXT
  │
  ├─ add-comment
  ├─ update-status → "待验证"
  ├─ reassign → 发起人
  └──▶ P5_NEXT
       │
       ▼
┌─────────────┐
│  P5_REPORT   │ 输出汇总报告
│  全局复盘    │ self-improving-agent
└─────────────┘
```

---

## 单 Bug 处理流程

```
输入: Bug ID
  │
  ├─ 跳过 Phase 1/2
  │
  ├─ Phase 3:
  │   ├─ 1. coding-bug-ops.read-detail(id) + read-comments(id)
  │   │     → 完整 Bug 上下文 (实时读取，不预采集)
  │   │
  │   ├─ 1a. [可选] test-case-ref.lookup(module)
  │   │     → 加载相关测试用例作为参考 (⚠️ 仅供参考)
  │   │
  │   ├─ 2. yili-code-fix.analyze(context)
  │   │     → 遗漏清单 + 前后端分类
  │   │
  │   ├─ 2a. [可选] db-query.check-data → 查库了解数据现状
  │   │
  │   ├─ 3. 展示分析方案 → ⏸️ 等待确认
  │   │
  │   ├─ 4a. [前端] → 准备评论草稿 + 查找前端负责人
  │   │
  │   ├─ 4b. [后端] → yili-code-fix.fix(context)
  │   │               → mvn compile
  │   │               → [可选] fix-verify (单元测试 + 数据验证)
  │   │               → [可选] local-api-test
  │   │               → git commit (本地提交)
  │   │
  │   └─ 5. 单 Bug 复盘
  │
  ├─ Phase 4:
  │   └─ git pull --rebase + push
  │
  └─ Phase 5:
      ├─ [可选] coding-ci-deploy
      ├─ [可选] SIT 验证
      ├─ coding-bug-ops 评论 + 状态 + 转派
      └─ 输出修复报告
```

---

## 批量处理流程

```
输入: filter URL
  │
  ├─ Phase 1: 预采集
  │   ├─ coding-bug-ops.read-list(url)
  │   │     → Bug 列表 [{id, title, status}, ...]
  │   ├─ 逐个: read-detail + read-comments + 截图
  │   │     → 保存到 yili-out/bug-prefetch/
  │   └─ [可选] test-case-ref.parse → 测试用例索引
  │
  ├─ Phase 2: 分诊台
  │   ├─ 初步分类（前端/后端）+ [可选] 匹配测试用例
  │   ├─ ⏸️ 用户调整优先级/标记跳过
  │   └─ 生成 fix-queue.json
  │
  ├─ Phase 3: 批量修复
  │   └─ for each bug in fix-queue (按 priority):
  │       └─ [可选]加载测试用例 → 分析 → 确认 → 修复 → 编译 → [单元测试] → [数据验证] → [接口测试] → commit → 复盘
  │
  ├─ Phase 4: 统一推送
  │   └─ git pull --rebase + push
  │
  └─ Phase 5: 统一闭环
      ├─ CI 构建
      ├─ [可选] SIT 验证
      ├─ 批量 Coding 操作（评论+状态+转派）
      └─ 汇总报告 + 全局复盘
```

---

## 状态标记说明

### Phase 级别状态

| 状态 | 含义 |
|------|------|
| P1_INIT | Phase 1 初始化 |
| P1_LIST | 正在读取 Bug 列表 |
| P1_DETAIL | 正在采集 Bug 详情 |
| P1_DONE | 预采集完成 |
| P1_TEST_INDEX | [可选] 正在解析测试用例索引 |
| P2_LOAD | 正在加载预采集数据 |
| P2_CLASSIFY | 正在初步分类 |
| P2_PRESENT | 等待用户确认分诊结果 |
| P2_DONE | 分诊完成 |
| P3_LOAD | 正在加载修复队列 |
| P3_LOAD_TESTCASE | [可选] 正在加载测试用例参考 |
| P3_ANALYZE | 正在分析 Bug |
| P3_FIX | 正在修复 |
| P3_COMPILE | 正在编译 |
| P3_UNIT_TEST | [可选] 正在运行单元测试 |
| P3_DATA_VERIFY | [可选] 正在执行数据验证 |
| P3_TEST | 正在本地测试 |
| P3_COMMIT | 正在 git commit |
| P3_REVIEW | 正在复盘 |
| P3_DONE | 批量修复完成 |
| P4_LOG | 正在展示 commit 列表 |
| P4_REBASE | 正在 pull --rebase |
| P4_CONFIRM | 等待用户确认 push |
| P4_PUSH | 正在推送 |
| P4_DONE | 推送完成 |
| P5_CI | 正在 CI 构建 |
| P5_SIT | 正在 SIT 验证 |
| P5_LOGIN | 正在登录 Coding |
| P5_FINALIZE | 正在执行 Coding 操作 |
| P5_REPORT | 正在生成报告 |
| P5_DONE | 全部完成 |

### Bug 级别状态

| 状态 | 含义 |
|------|------|
| queued | 在修复队列中等待 |
| analyzing | 正在分析 |
| waiting_confirm | 等待用户确认 |
| fixing | 正在修复 |
| compiling | 正在编译 |
| unit_testing | 正在运行单元测试 |
| data_verifying | 正在执行数据验证 |
| testing | 正在本地测试 |
| fixed | 修复+编译通过，待 commit |
| tag-frontend | 标记为前端问题，待 Phase 5 操作 |
| skipped | 用户跳过 |
| committed | 已 commit 到本地，待 push |
| pushed | 已推送到远端 |
| deployed | 已部署 SIT |
| sit-pass | SIT 验证通过 |
| sit-fail | SIT 验证失败 |
| finalized | Coding 操作完成 |
| failed | 处理失败 |

### fix-queue action 类型

| action | 含义 |
|--------|------|
| fix | 后端修复 |
| tag-frontend | 标注前端问题 + 转派 |
| skip | 跳过不处理 |

---

## 错误处理策略

| 错误类型 | 发生阶段 | 处理方式 |
|----------|---------|---------|
| 浏览器认证失败 | Phase 1/5 | 降级认证策略 (Profile -> Cookie -> SSO) |
| Bug 详情读取失败 | Phase 1 | 重试1次，失败则跳过并记录，不阻塞其他 Bug |
| 老代码定位失败 | Phase 3 | 报告给用户，等待手动指定 |
| 新代码定位失败 | Phase 3 | 报告给用户，可能未迁移 |
| 编译失败 | Phase 3 | 自动修复重试3次，失败则标注 |
| 本地测试失败 | Phase 3 | 记录失败，不阻塞后续 Bug |
| 单元测试失败 | Phase 3 | 报告 verdict 给用户，不自动阻塞 git commit |
| 数据验证失败 | Phase 3 | 报告给用户，不自动阻塞（db-query 连接失败则跳过） |
| Git 冲突 | Phase 4 | ⏸️ 暂停等待用户手动解决 |
| CI 构建失败 | Phase 5 | ⏸️ 通知用户，等待决策（Coding 操作不依赖 CI 成功） |
| SIT 测试失败 | Phase 5 | 记录失败截图，按 sit-verify-analyze 路由处理 |
| Coding 评论提交失败 | Phase 5 | 重试1次，失败则本地保存评论内容 |
| 预采集数据缺失 | Phase 3 | 降级为实时读取（Phase 1 采集失败的 Bug） |
| 测试用例索引缺失 | Phase 1/3 | 跳过测试用例加载，不阻塞流程（可选步骤） |
