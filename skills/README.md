# AI Spec Skills

这个目录存放伊利项目的本地技能定义、参考资料和少量历史提示词文档。

优先级约定：

1. 本地 `SKILL.md` 是主能力
2. 外部 OpenSkill 只做增强，不替代本地业务流程
3. 安装命令统一放在本文末尾

---

## 目录结构

当前目录主要分为这些类别：

- `architect/`
- `code/`
- `db/`
- `finance/`
- `pm/`
- `ppt/`
- `requirements/`
- `test/`
- `team/`

其中最常用的是 `code/`，已经形成一组比较完整的研发与修复流水线技能。

---

## 核心本地 Skills

### 代码修复与验证

位于 `code/bug-fix-cycle/`：

- `bug-fix-pipeline`
  端到端 Bug 修复编排器
- `coding-bug-ops`
  Coding 缺陷读取、评论、转派、状态更新
- `yili-code-fix`
  基于老新代码对比的后端修复
- `local-api-test`
  本地接口自动推导与 curl 验证
- `git-commit-push`
  安全提交与 push
- `coding-ci-deploy`
  Coding CI 发布到 SIT
- `sit-smoke-test`
  SIT 冒烟与场景验证
- `sit-verify-analyze`
  SIT 验证后归因与路由
- `memory-setup`
  长流程运行记忆初始化与维护
- `self-improving-agent`
  单 Bug 和批量流程复盘

### 研发生成类

位于 `code/`：

- `front-end-skills`
  `fssc-web` / `fssc-web-framework` 前端开发、联调、页面测试
- `claim-generator`
  报账单模块生成器
- `yili-crud`
  标准 CRUD 代码生成

### 其它代码资产

下面这些目录目前更偏参考资料、转换流程或历史提示词，不全是完整 skill：

- `code/compare-transform/`
- `code/transform-claim/`
- `code/project/`
- `code/test/`

使用前先看目录内是否存在正式 `SKILL.md`。

---

## 其它本地 Skills 分类

- `architect/`
  包含架构分析类 skill，例如 DDD、TOGAF
- `db/`
  数据库与 Oracle DBA 能力
- `finance/`
  金融分析相关 skill
- `pm/`
  项目管理与沟通类 skill
- `ppt/`
  PPT 美化与说服型表达
- `requirements/`
  需求分析、建模、模板
- `test/`
  测试系统与接口测试资产
- `team/`
  团队角色说明和职责规范

---

## 推荐外部增强 Skills

这些不是必须，但和当前本地 skill 体系很匹配。

### 浏览器与 E2E

- `browser-use`
  适合 Coding 页面操作、CI 页面触发、SIT 登录态复用
- `playwright-e2e-testing`
  适合稳定回归和正式断言
- `agent-browser`
  适合作为页面联调和临时浏览器 fallback

### 记忆与自改进

- `memory-management`
  适合作为 `memory-setup` 的长期记忆增强
- `knowledge-management`
  适合作为个人/团队知识库和文件夹知识组织增强
- `source-management`
  适合作为外部知识源、连接器和内容来源管理增强
- `task-management`
  适合作为轻量任务面板和任务文件管理增强
- `self-improving-agent`
  适合作为本地复盘模板的外部增强版本

### 文档、幻灯片与前端设计增强

- `doc-coauthoring`
  适合结构化写文档、方案、设计说明
- `internal-comms`
  适合周报、公告、项目进展和 FAQ 类内部沟通
- `stakeholder-comms`
  适合面向跨团队、业务方、管理层的沟通文本
- `frontend-design`
  适合补强页面设计方法论
- `theme-factory`
  适合统一文档、幻灯片、网页的视觉主题和品牌一致性
- `web-artifacts-builder`
  适合快速构建网页原型、交互式 artifact、演示页

### Skill 开发与演进

- `skill-creator`
  适合把本地经验沉淀成正式 skill
- `skill-development`
  适合系统化设计、拆分和验证新的 skill 结构

---

## 公众号文章提炼

参考文章：

- [2026用上这些Skills，你就跑赢了90%的人](https://mp.weixin.qq.com/s/YPmdgMo44YD3ZVfCH45lLw)

从可提取正文来看，文章和其中引用的 Anthropic/Cowork 实践，强调了这些方向：

1. 文档和幻灯片需要统一品牌与风格
2. 个人文件夹和知识库能显著减少重复上下文输入
3. 高价值用户会创建、共享、复用技能
4. 从洞见到原型、从原型到 artifact 的链路要尽量缩短

映射到本仓库，优先推荐这几类外部 skill：

- 文档与幻灯片：
  `doc-coauthoring`、`theme-factory`、`internal-comms`
- 记忆与知识管理：
  `memory-management`、`knowledge-management`、`source-management`
- 原型与前端 artifact：
  `frontend-design`、`web-artifacts-builder`
- 技能演化：
  `self-improving-agent`、`skill-creator`、`skill-development`
- 浏览器与验证：
  `browser-use`、`playwright-e2e-testing`

---

## 使用建议

- 本地业务流程优先走 `ai-spec/skills` 下的本地 skill
- 涉及浏览器、E2E、长期记忆、设计增强时，再补外部 skill
- `bug-fix-pipeline` 已经按“双轨兼容”设计：
  本地 `memory-setup` 和 `self-improving-agent` 为主轨
  外部 `memory-management` 和市场版 `self-improving-agent` 为增强轨

---

## 常用入口

- 代码修复主入口：
  `code/bug-fix-cycle/bug-fix-pipeline/`
- 前端开发主入口：
  `code/front-end-skills/`
- 本地接口测试入口：
  `code/bug-fix-cycle/local-api-test/`
- 报账单代码生成入口：
  `code/claim-generator/`
- CRUD 生成入口：
  `code/yili-crud/`

---

## 安装命令

### Skills CLI 常用命令

```bash
npx skills --help
npx skills find "frontend design"
npx skills find "memory management"
npx skills find "self improving"
npx skills find "doc coauthoring"
npx skills find "theme factory"
npx skills add <package-or-git-url> -g -y
npx skills check
npx skills update
```

说明：

- `find`
  搜索市场中的 skill
- `add`
  安装指定 skill
- `check`
  检查本机已安装 skill 的更新
- `update`
  更新本机已安装 skill

如果本机还没有全局安装，可以直接按需使用 `npx skills`。

### 浏览器与测试增强

```bash
npx skills add https://github.com/browser-use/browser-use --skill browser-use -g -y
npx skills add bobmatnyc/claude-mpm-skills@playwright-e2e-testing -g -y
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser -g -y
```

### 记忆、知识管理与自改进增强

```bash
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill memory-management -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill knowledge-management -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill source-management -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill task-management -g -y
npx skills add charon-fan/agent-playbook@self-improving-agent -g -y
```

### 文档、幻灯片与 artifact 增强

```bash
npx skills add https://github.com/anthropics/skills --skill doc-coauthoring -g -y
npx skills add https://github.com/anthropics/skills --skill internal-comms -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill stakeholder-comms -g -y
npx skills add https://github.com/anthropics/skills --skill theme-factory -g -y
npx skills add https://github.com/anthropics/claude-plugins-official --skill frontend-design -g -y
npx skills add https://github.com/anthropics/skills --skill web-artifacts-builder -g -y
```

### Skill 开发与维护增强

```bash
npx skills add https://github.com/anthropics/skills --skill skill-creator -g -y
npx skills add https://github.com/anthropics/claude-code --skill skill-development -g -y
```

### 公众号优选一键安装清单

如果按当前仓库最匹配的组合一次性安装，建议执行：

```bash
npx skills add https://github.com/browser-use/browser-use --skill browser-use -g -y
npx skills add bobmatnyc/claude-mpm-skills@playwright-e2e-testing -g -y
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill memory-management -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill knowledge-management -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill source-management -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill task-management -g -y
npx skills add charon-fan/agent-playbook@self-improving-agent -g -y
npx skills add https://github.com/anthropics/skills --skill doc-coauthoring -g -y
npx skills add https://github.com/anthropics/skills --skill internal-comms -g -y
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill stakeholder-comms -g -y
npx skills add https://github.com/anthropics/skills --skill theme-factory -g -y
npx skills add https://github.com/anthropics/claude-plugins-official --skill frontend-design -g -y
npx skills add https://github.com/anthropics/skills --skill web-artifacts-builder -g -y
npx skills add https://github.com/anthropics/skills --skill skill-creator -g -y
npx skills add https://github.com/anthropics/claude-plugins-official --skill skill-development -g -y
```

### 可选：检查已安装技能

```bash
npx skills check
npx skills update
```
