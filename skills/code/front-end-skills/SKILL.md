---
name: front-end-skills
description: 处理伊利 FSSC 前端项目开发与重构任务，适用于 fssc-web 与 fssc-web-framework。用户需要新增或修改搜索页、报账单详情页、行表格、路由、schema 适配、service 接口、Setaria/FSSC 业务组件接入，或需要基于现有页面模式快速落地 Vue2 页面时使用此技能。
---

# FSSC Front End Skills

## 适用范围

- `fssc-web` 业务页面开发、改造、排查
- `fssc-web-framework` 组件、工具、样式、文档示例开发
- 基于 `Vue 2 + Setaria + fssc-web-framework` 的页面骨架生成
- 前端页面路由联调、浏览器自动化验收、页面截图与交互回归

## 先判断做哪一类任务

### 1. 业务搜索页

目标通常在 `fssc-web/src/page/**/index.vue`，配套文件常见为：

- `index.vue`
- `service.js`
- `tableSchemaFile.js`
- `src/config/route/**/index.js`

这类页面优先复用：

- `fssc-search-page`
- `SchemaUtils`
- `SchemaUiUtils`
- `$getSchemaByApiKey`
- `$createDefaultObjectBySchema`

详细模式见 [references/page-patterns.md](references/page-patterns.md)。

### 2. 报账单详情页 / 明细页

目标通常在 `fssc-web/src/page/claim/**/T***/`，常见结构：

- `index.vue`
- `service.js`
- `header/`
- `table/`
- `other/`

这类页面优先复用：

- `fssc-detail-page`
- `fssc-detail-page-header`
- `fssc-detail-page-footer`
- `fssc-detail-page-table`
- `fssc-detail-page-package-tabs`
- `BaseMixin`
- `WorkflowMixin`

### 3. 框架层开发

目标在 `fssc-web-framework`：

- 新增/修改组件时先找 `src/package/**` 现有同类实现
- 新增公共工具时先找 `src/util/**`
- 新增全局安装内容时看 `src/install.js`
- 新增导出入口时看 `src/lib.js`
- 若有文档演示，补 `doc/demo/*.md`

项目地图见 [references/project-map.md](references/project-map.md)。

### 4. 页面联调与浏览器测试

当任务包含以下意图时，必须联动浏览器能力：

- “打开页面看看”
- “验证路由是否可达”
- “启动项目后帮我点进去测一下”
- “看这个页面有没有报错”
- “做一遍前端冒烟测试”
- “弹出浏览器”
- “用 computer use 打开”
- “我要看到真实浏览器窗口”

这类任务除了读代码，还要使用 `agent-browser` 实际打开页面验证。

优先套用下面两个标准动作：

- `open-page`：根据代码找到路由并真实打开页面，确认“页面能不能看到”
- `smoke-test`：在页面打开后，继续检查标题、查询区、表格、按钮、跳转是否正常

如果用户明确要求“看到浏览器”或“使用 computer use”，必须使用 `agent-browser --headed`，不能退回无头模式。

## Browser Automation Boundary

浏览器联调统一按下面规则执行，不再混用口径：

### 统一规则

- 需要可见浏览器窗口时：优先 `Playwright`
- 优先复用本机已有 Chrome，不先依赖下载 Playwright 自带 Chromium
- 只有当 `Playwright` 被环境阻塞时，才退回 `agent-browser`

### Playwright

- 适合可见浏览器联调
- 适合仓库内可重复执行的自动化测试
- 适合编写 `spec`、断言、回归测试、CI 执行、稳定复跑
- 适合“请给我写测试用例”“请补自动化测试”“请新增 e2e”

### agent-browser

- 作为浏览器联调 fallback
- 适合 Playwright 被环境问题卡住时的临时操作
- 适合快速打开真实系统、点击菜单、截图、确认当前页面状态

默认顺序：

1. `Playwright + system Chrome`
2. `Playwright + installed Chromium`
3. `agent-browser --headed`

## 默认工作流

### 第一步：找最近似实现

不要直接从零写。先在目标仓库中搜索以下之一：

- 同模块兄弟页面
- 同类型页面
- 同 itemId 报账单
- 同类框架组件

优先复制结构，再做最小必要修改。

### 第二步：确认数据来源

- 业务页面的 schema 优先来自 `src/json-schema`
- schema 缺失时，先确认能否从 `setaria.config.js` 对应 swagger 源生成
- service 调用优先沿用 `Setaria.getHttp().<domain>`
- 报账单页面优先复用 `@/page/claim/base/service`

### 第二步半：确认页面入口与路由

测试页面前，必须先从代码里把真实 URL 推出来，不要猜。

按顺序检查：

- `src/config/route/index.js` 里是否汇总了对应模块
- 目标模块的 `src/config/route/**/index.js`
- 页面组件里的 `this.$router.push(...)`、`path:`、`name:`
- 若是报账单，确认是否存在 query 参数依赖，如 `claimId`、`itemId`、`archiveId`

常见规则：

- 顶层模块通常是 `/模块名/子路径`
- 例如 `accountingDoc/index.js` 中 `path: 'autoArchiveCheckPool'`，实际通常是 `/accountingDoc/autoArchiveCheckPool`
- 报账单页面常见路径是 `/claim/T065`、`/claim/T044`

如果页面依赖 query，先准备最小可打开参数；拿不到参数时，先打开列表页或入口页，再通过页面按钮跳转。

### 第三步：按页面类型落文件

#### 搜索页

至少检查：

- `index.vue` 里是否包含 `schema / conditionSchema / conditionData / tableSchema / tableUiSchema`
- `service.js` 是否只做接口封装，不混业务状态
- `tableSchemaFile.js` 是否仅保留列定义与 ui schema
- 路由文件是否补充菜单标题与懒加载路径

#### 报账单详情页

至少检查：

- `index.vue` 是否只做装配，不堆积大量字段逻辑
- `service.js` 是否统一暴露 `apiGetInitData / apiSaveData / apiSubmitData / apiDeleteData`
- 头、行、备注等复杂逻辑是否拆到 `header/ table/ other/`
- 是否复用现有 mixin 与 workflow 交互

#### 框架组件

至少检查：

- 是否已在 `src/install.js` 注册
- 是否已在 `src/lib.js` 导出
- 是否补充样式入口
- 是否需要补 demo 文档

#### 浏览器联调

至少检查：

- 本地开发服务是否已启动
- 使用的 base URL 是多少，例如 `http://localhost:8080`
- 目标页面完整 URL 是否由路由代码推导确认
- 打开页面后是否有白屏、报错、权限或登录拦截
- 关键按钮、表格、查询条件是否真的可见
- 必要时截图、保存当前 URL、记录异常

## 浏览器测试工作流

当需要真实打开页面时，按下面流程执行：

### 1. 启动前端

优先检查 `package.json`，通常：

- `fssc-web`: `yarn dev`
- `fssc-web-framework`: `yarn dev`

若已有运行中的本地服务，优先复用，不重复启动。

### 2. 从代码推导 URL

示例：

- `src/config/route/index.js` 汇总 `accountingDoc`
- `src/config/route/accountingDoc/index.js` 中 `MODULE_BASE_URL = 'accountingDoc'`
- 子路由 `path: 'autoArchiveCheckPool'`
- 最终访问路径通常是 `/accountingDoc/autoArchiveCheckPool`

如果是 `fssc-web`，优先使用脚本自动解析：

```bash
python3 scripts/route-open.py src/page/accountingDoc/autoArchiveCheckPool/index.vue
python3 scripts/route-open.py page/accountingDoc/autoArchiveCheckPool/index.vue --open
python3 scripts/route-open.py autoArchiveCheckPool --base-url http://localhost:8080
```

### 3. 用浏览器打开并校验

优先顺序：

1. `Playwright + system Chrome`
2. `Playwright + installed Chromium`
3. `agent-browser --headed`

优先示例：

```bash
npx playwright open --browser chromium http://localhost:8080/accountingDoc/autoArchiveCheckPool
```

如果需要仓库内断言或脚本化：

```bash
PLAYWRIGHT_BASE_URL=http://localhost:8080 npx playwright test tests/smoke/t034.spec.ts
```

如果 Playwright 被环境阻塞，再退回：

```bash
agent-browser --headed open http://localhost:8080/accountingDoc/autoArchiveCheckPool
agent-browser wait --load networkidle
agent-browser snapshot -i
```

如果页面有跳转、懒加载、异步表格，再补：

```bash
agent-browser wait 2000
agent-browser snapshot -i
agent-browser screenshot --full
agent-browser get url
```

如果需要点击入口按钮进入详情页：

```bash
agent-browser snapshot -i
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
```

### 4. 记录测试结果

至少输出：

- 实际访问 URL
- 页面是否成功打开
- 是否命中目标路由
- 页面上是否出现关键组件
- 是否存在报错、空白、接口失败、参数缺失

注意：

- 这一步是 browser automation / computer use，不是 Playwright test run
- 结果主要用于联调、排障、确认页面状态，不等价于自动化回归覆盖

## 标准动作

### open-page

适用场景：

- “把这个页面打开看看”
- “这个路由能不能进去”
- “页面能看到不”

执行目标：

- 从代码推出真实 URL
- 打开本地页面
- 判断页面是否成功渲染

执行步骤：

1. 从 `src/config/route/index.js` 和目标模块路由文件推导路径
2. 确认是否需要 query 参数
3. 启动或复用本地前端服务
4. 用 `agent-browser open` 打开页面
5. 用 `snapshot -i` 和 `screenshot --full` 确认页面实际可见
6. 输出结论

如果用户明确要求可见窗口，第 4 步默认先走 `Playwright`，只有失败时才换成 `agent-browser --headed open`。

最低输出要求：

- 访问的完整 URL
- 页面是否打开成功
- 当前看到的是目标页面、登录页、报错页还是白屏
- 若失败，指出是路由错误、参数缺失、权限拦截还是接口异常

### smoke-test

适用场景：

- “帮我冒烟测一下这个页面”
- “看看这个页面基本功能是不是正常”
- “改完代码后进去点一下”

执行目标：

- 在页面可打开的前提下，验证基础可用性

最小检查项：

- 页面标题或主区域是否出现
- 查询条件区是否渲染
- 表格或主要内容区是否渲染
- 关键按钮是否可见
- 点击一个入口动作后是否发生预期跳转或弹层
- 是否出现明显报错、空数据异常、无限 loading

推荐执行顺序：

```bash
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser screenshot --full
```

如果页面包含典型入口按钮，再继续：

```bash
agent-browser click @eN
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser get url
```

如果用户要求 computer use，可见窗口必须保持开启；默认先走 `Playwright` 可见模式，失败后再切 `agent-browser --headed`。

最低输出要求：

- 冒烟检查了哪些点
- 哪些点通过
- 哪些点失败
- 失败时的页面现象和可能原因

## Playwright 何时介入

只有在下面场景才切到 Playwright：

- 用户明确要求“写 Playwright 测试”
- 需要把验证沉淀成仓库内可复跑脚本
- 需要断言具体交互结果并纳入 CI
- 需要稳定回归同一流程

如果切到 Playwright，先做三件事：

1. 确认仓库里是否已有 Playwright 配置
2. 复用现有测试目录、fixture、登录方案
3. 区分“联调脚本”和“正式测试用例”，不要混在一起

如果仓库里还没有 Playwright：

1. 不要假装“已有测试体系”
2. 明确告知当前仓库缺少 `playwright.config.*`、测试目录和脚本
3. 只有在用户明确要求时，才新增最小可运行基线，例如：
   - `playwright.config.ts`
   - `tests/`
   - `package.json` 中的 Playwright 脚本
4. 对真实 SIT/UAT 登录流程，优先先验证是否适合沉淀为 Playwright，而不是直接硬编码账号流程

## 强约束

- 保持 `Vue 2 Options API` 风格，除非目标文件已经用了别的模式
- 优先使用 `fssc-web-framework` 组件，不要随意退回原生 `el-*` 直接拼业务
- schema 字段标题、格式、隐藏逻辑优先通过 `SchemaUtils / SchemaUiUtils` 调整
- 搜索页列表列宽、格式化、slot 覆盖要与同目录页面保持一致
- 不要把接口 URL、页面状态、路由跳转逻辑散落在多个文件里
- 缺 schema 时先说明依赖 swagger 生成，不要编造大量字段

## 输出前自检

- 页面路径是否放对
- 路由是否注册
- service domain 是否正确，如 `claim / fund / tr / config / image`
- schema key 与接口 bean 名是否真实存在
- 复用了最近似页面模式，而不是自造结构
- 若是 framework 改动，入口导出和 demo 是否完整
- 若要求实际验证，是否已经用 `agent-browser` 打开页面并确认 URL 与界面结果

## 模板资源

- 搜索页骨架：[assets/search-page-index.vue](assets/search-page-index.vue)
- 搜索页 service：[assets/search-page-service.js](assets/search-page-service.js)
- 表格 schema：[assets/table-schema-file.js](assets/table-schema-file.js)
- 报账单详情页骨架：[assets/detail-page-index.vue](assets/detail-page-index.vue)
- 报账单 service：[assets/detail-page-service.js](assets/detail-page-service.js)

这些模板只用于起步，生成代码前仍然要先比对目标目录中的相似实现。

## 脚本资源

- 路由解析脚本：[scripts/route-open.py](scripts/route-open.py)

用途：

- 输入页面路径，输出推导后的路由 URL
- 输入路由片段，输出最可能的访问地址
- 可配合 `agent-browser` 做 `open-page`

## 参考

- [references/project-map.md](references/project-map.md)
- [references/page-patterns.md](references/page-patterns.md)
- `agent-browser` skill，用于真实打开页面、点击和截图

## 与 Computer Use 的关系

这里的集成方式不是把浏览器能力硬编码进 skill，而是：

- `front-end-skills` 负责识别该测什么页面、路由在哪、参数是什么
- `agent-browser` 负责真实打开页面、点击、截图、读取结果

当用户要求 computer use 时，执行要求进一步收紧：

- 必须使用可见浏览器窗口
- 默认命令形式为 `agent-browser --headed ...`
- 结果里要说明当前看到的是目标页、登录页还是错误页

也就是代码理解加浏览器执行的两段式协作。

当任务涉及真实页面验证时，不能只停留在静态代码分析，必须切换到这个模式。
