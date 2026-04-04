---
name: self-improving-agent
description: 在任务完成后做短周期自改进复盘，提炼可复用启发式、检查项和避免重复失误的策略。支持多记忆架构（语义+情景+工作记忆）、自修正工作流和 hooks 集成。适用于 Bug 修复、调试、测试和长流程自动化编排。
---
# Self Improving Agent

## 概述

此 skill 用来做**短、硬、可执行**的复盘，同时支持**多记忆架构**和**自修正机制**。

核心目标:

1. 这次为什么成功或失败
2. 哪些信号本可以更早发现
3. 下一次默认应多做哪一步检查

扩展能力（来自外部增强）:

- **多记忆架构**: 语义记忆(模式/规则) + 情景记忆(具体经历) + 工作记忆(当前会话)
- **自修正**: 检测并修复 skill 指导错误
- **演化标记**: 可追踪的变更归因
- **Hooks 集成**: skill 事件自动触发（开始/完成/出错）

适用场景:

- 单个 Bug 修复完成后
- 一轮 SIT 验证结束后
- 批量流水线全部结束后
- 手动触发: "自我进化"、"分析今天的经验"、"总结教训"

兼容策略:

- 本 skill 提供仓库内可控的轻量复盘格式
- 如果环境里安装了 OpenSkill 市场版 `self-improving-agent`，可以额外参考其 pattern 抽象和 memory 分层方法
- 在 `bug-fix-pipeline` 中，默认先执行本地复盘模板，再按需吸收外部 skill 的长期演化做法

---

## 输出格式

```markdown
## Improvement Review
- outcome:
- what_worked:
- what_failed:
- missed_signals:
- new_heuristics:
- checklist_updates:
- carry_forward:
```

要求:

- 每项只写可执行内容
- 优先 1-3 条高价值启发式
- 不写泛泛而谈的结论

---

## 工作流

### Phase 1: 经验提取

对比预期与实际，提取:

```yaml
What happened:
  skill_used: {使用了哪个 skill}
  task: {在做什么}
  outcome: {success|partial|failure}

Key Insights:
  what_went_well: [做对了什么]
  what_went_wrong: [做错了什么]
  root_cause: {根因，如果适用}

User Feedback:
  rating: {1-10，如果有}
  comments: {具体反馈}
```

先看:

- 计划是否按预期推进
- 哪一步最耗时
- 哪一步最容易误判

### Phase 2: 分类失误来源

优先落到这几类之一:

- 上下文缺失
- 评论/历史信息漏读
- 前后端归因错误
- 服务模块判断错误
- 请求体构造错误
- 环境异常误判为代码问题
- 验证不充分

### Phase 3: 模式抽象

把具体经历转成可复用的模式:

| 具体经历 | 抽象模式 | 目标 Skill |
|----------|----------|------------|
| "评论里的复现步骤没读到" | "先读评论，再读描述" | coding-bug-ops |
| "前端问题误判为后端" | "SIT 先区分 API 正确还是前端渲染错误" | sit-verify-analyze |
| "列表接口请求体不对" | "分页接口默认先测最小 PageParam" | local-api-test |

**抽象规则:**

```yaml
If 同类经历重复 3+ 次:
  级别: critical
  动作: 写入 skill 的"关键检查项"

If 解决方案有效:
  级别: best_practice
  动作: 写入 skill 的"最佳实践"

If 用户评分 >= 7:
  级别: strength
  动作: 强化这个方法

If 用户评分 <= 4:
  级别: weakness
  动作: 写入"避免事项"
```

### Phase 4: 更新检查项

把新规则转成简短检查项，回写给 `memory-setup` 的 `carry_forward_checks`。

只保留下一轮真正可复用的规则，例如:

- "先用 `local-api-test` 的前端反推脚本定模块，再改代码"
- "分页接口默认先测最小 `pageNum/pageSize/params`"
- "SIT 页面异常先区分 API 正确还是前端渲染错误"

### Phase 5: 全局复盘

如果是批量流程最后一轮，再额外输出:

- 重复出现最多的 1-2 类失误
- 最有效的 1-2 个默认动作
- 建议补进主 skill 的流程位

---

## 多记忆架构

### 1. 语义记忆 (模式/规则)

存储**可跨场景复用的抽象模式**:

```json
{
  "patterns": {
    "pat-2026-04-03-001": {
      "name": "先读评论再读描述",
      "source": "bug-fix-pipeline 复盘",
      "confidence": 0.95,
      "applications": 5,
      "category": "bug_analysis",
      "target_skills": ["coding-bug-ops", "yili-code-fix"]
    }
  }
}
```

位置: `memory/semantic-patterns.json`（如果需要落盘）

### 2. 情景记忆 (具体经历)

存储**特定的经验记录**:

```json
{
  "id": "ep-2026-04-03-001",
  "timestamp": "2026-04-03T10:30:00Z",
  "skill": "yili-code-fix",
  "situation": "T047 凭证预览内容为空",
  "root_cause": "前端 invoiceType 校验被注释",
  "solution": "恢复 detail-page-header.vue 中 invoiceType 校验",
  "lesson": "老代码有条件判断的按钮，新代码不能无条件显示",
  "related_pattern": "前后端归因"
}
```

位置: `memory/episodic/YYYY-MM-DD-{skill}.json`（如果需要落盘）

### 3. 工作记忆 (当前会话)

由 `memory-setup` 的 Run Memory 承担，不重复建设。

---

## 自修正工作流

当 skill 指导产生错误时触发:

```
1. 检测错误
   - 从工作记忆中获取错误上下文
   - 识别遵循了哪个 skill 的指导

2. 确认根因
   - skill 指导本身错误？
   - 指导被误解？
   - 指导不完整？

3. 应用修正
   - 更新 skill 文件，加修正标记
   - 更新语义记忆中的相关模式

4. 验证修正
   - 测试修正后的指导
   - 请用户确认
```

### 演化标记

更新 skill 时加上来源追踪:

```markdown
<!-- Evolution: 2026-04-03 | source: ep-2026-04-03-001 | skill: coding-bug-ops -->
## 新增检查项 (2026-04-03)
- [ ] Bug 分析前先读评论区全部信息
```

### 修正标记

修正错误指导时加上原因:

```markdown
<!-- Correction: 2026-04-03 | was: "无条件显示凭证预览按钮" | reason: 老代码有 invoiceType 条件 -->
## 修正: 凭证预览按钮显示条件
凭证预览按钮需要判断 invoiceType 是否有效值，不能无条件显示。
```

---

## Hooks 集成（可选）

如果 agent 环境支持 hooks，可配置自动触发:

| 事件 | 触发时机 | 动作 |
|------|----------|------|
| `before_start` | 任何 skill 启动 | 记录会话开始 |
| `after_complete` | 任何 skill 完成 | 提取模式，更新 skill |
| `on_error` | 命令返回非零 | 捕获错误上下文，触发自修正 |

---

## 强制约束

1. 复盘必须短，默认 5-10 行
2. 只记录下次真的会执行的动作
3. 不要把环境偶发现象误写成通用规则
4. 单 Bug 复盘和全局复盘都要能回写到运行记忆
5. 如果发现问题来自 skill 自身缺口，明确指出应补哪个 skill
6. 模式抽象要在正确的层级，不要从单次经历过度泛化
7. 修正 skill 时必须加修正标记，保留可追踪性
8. 自修正不要无限递归，只纠正一次，效果不好则请用户确认
