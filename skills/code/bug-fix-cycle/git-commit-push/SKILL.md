---
name: git-commit-push
description: Bug 修复后的代码提交流程。先 pull 更新，检测冲突，展示 diff，等待用户确认后再 commit + push。支持多行提交信息（HEREDOC）、错误恢复（误提交/秘钥泄露）和提交前检查清单。当用户修复完 Bug 需要提交代码时使用。
allowed-tools: Bash(git:*), AskUser
---
# Git Commit Push (代码提交)
@author: sevenxiao

## 概述

Bug 修复后的安全代码提交流程，严格遵循 **先更新 → 冲突检测 → 人工确认 → 提交推送** 的顺序。

**核心约束**: **提交代码之前，必须人工确认**。AI 不得自动提交代码。

## 外部依赖

无外部依赖，仅使用 git 命令行。

兼容策略:

- 本 skill 是伊利项目的主提交流程，包含项目特定的 scope 映射和强制人工确认
- 如果环境里安装了 OpenSkill `git-workflow-with-conventional-commits`，可以借用其 PR 创建、Worktree、HEREDOC 多行 commit 等增强能力
- 但人工确认约束始终优先于外部 skill 的自动化行为

---

## 使用方式

```bash
# 提交当前修改（自动检测模块）
/skill git-commit-push

# 指定提交信息
/skill git-commit-push "fix(config): 修复会计分组座席状态修改人字段不同步"

# 指定模块目录
/skill git-commit-push fssc-config-service "fix(config): 修复座席状态修改人字段"
```

---

## 提交流程（5 步）

### Step 1: 检查当前状态

```bash
# 查看当前分支
git branch --show-current

# 查看修改的文件
git status

# 查看详细 diff
git diff
git diff --cached
```

**输出**: 列出所有修改的文件和变更内容，供用户审查。

---

### Step 2: Pull 更新

```bash
# 拉取远程最新代码
git pull --rebase
```

**判断结果**:
- `Already up to date.` → 无需合并，继续 Step 3
- 正常合并完成 → 继续 Step 3
- **`CONFLICT`** → 有冲突，进入冲突处理流程

---

### Step 3: 冲突处理（如有）

**如果 pull 时遇到冲突**:

```bash
# 查看冲突文件
git diff --name-only --diff-filter=U
```

**冲突时必须停止，提示用户手动处理**:

```
代码冲突！以下文件有冲突需要手动合并：

<冲突文件列表>

请手动解决冲突后，执行以下命令继续：
  git add <冲突文件>
  git rebase --continue

或放弃本次 rebase：
  git rebase --abort

解决冲突后重新执行本 skill。
```

**AI 绝不自动解决冲突**，必须等用户手动处理完成。

---

### Step 4: 展示 Diff + 等用户确认

**无冲突时，展示完整变更供用户审查**:

```bash
# 展示即将提交的所有变更
git diff HEAD
# 或者如果已暂存
git diff --cached

# 列出变更文件摘要
git diff --stat HEAD
```

**向用户展示**:

```markdown
## 即将提交的变更

**分支**: <当前分支名>
**变更文件**:
- M fssc-config-service/.../TProcAccountantteamUserDoMapper.xml
- M fssc-config-service/.../TProcAccountantteamUserServiceImpl.java

**Diff 摘要**:
<git diff --stat 输出>

**提交信息**: <type>(<scope>): <subject>

---
请确认以上变更是否正确，确认后将执行 git add + commit + push。
```

**必须调用 AskUser 等待用户确认**:
- 用户确认 → 继续 Step 5
- 用户拒绝 → 停止，不提交

---

### Step 5: 提交 + 推送

用户确认后：

```bash
# 暂存所有变更
git add <修改的文件列表>

# 提交（不要 add 不相关的文件，只 add 本次修改的文件）
git commit -m "<type>(<scope>): <subject>"

# 推送到远程
git push
```

**多行提交信息**（body 较长时使用 HEREDOC）:

```bash
git commit -m "$(cat <<'EOF'
fix(config): 修复会计分组座席状态修改人字段不同步

Bug #4686: 修改座席状态时同时更新 MODIFY_* 和 MODIFIER_* 两套字段，
确保查询页面能正确显示最新的修改时间和修改人。

Closes #4686
EOF
)"
```

**验证推送结果**:
```bash
# 确认推送成功
git log --oneline -1
git status
```

---

## 提交信息规范

遵循项目 Git 提交偏好：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**type 类型**:
| type | 说明 | 频率 |
|------|------|------|
| `fix` | Bug 修复 | 高 |
| `feat` | 新功能 | 高 |
| `refactor` | 重构 | 中 |
| `docs` | 文档 | 中 |
| `test` | 测试 | 中 |
| `style` | 格式调整 | 低 |
| `chore` | 构建/工具变更 | 低 |
| `perf` | 性能优化 | 低 |
| `ci` | CI/CD 变更 | 低 |
| `revert` | 回滚 | 稀 |

**scope 映射**（根据修改文件所在模块）:
| 模块目录 | scope |
|----------|-------|
| `fssc-config-service/` | `config` |
| `fssc-claim-service/claim-base/` | `claim-base` |
| `fssc-claim-service/claim-common/` | `claim-common` |
| `fssc-claim-service/claim-ptp/` | `claim-ptp` |
| `fssc-claim-service/claim-tr/` | `claim-tr` |
| `fssc-claim-service/claim-otc/` | `claim-otc` |
| `fssc-claim-service/claim-eer/` | `claim-eer` |
| `fssc-claim-service/claim-fa/` | `claim-fa` |
| `fssc-claim-service/claim-rtr/` | `claim-rtr` |
| `fssc-common-service/` | `common` |
| `fssc-integration-service/` | `integration` |
| `fssc-fund-service/` | `fund` |
| `fssc-image-service/` | `image` |
| `fssc-voucher-service/` | `voucher` |
| `fssc-bpm-service/` | `bpm` |
| `fssc-invoice-service/` | `invoice` |
| `fssc-web/` | `web` |
| `fssc-web-framework/` | `web-framework` |
| `ai-spec/` | `ai-spec` |

**示例**:
```
fix(config): 修复会计分组座席状态修改人字段不同步

Bug #4686: 修改座席状态时同时更新 MODIFY_* 和 MODIFIER_* 两套字段，
确保查询页面能正确显示最新的修改时间和修改人。
```

---

## 提交前检查清单

### 代码检查

- [ ] 修改的文件都是本次任务相关的
- [ ] 没有包含敏感信息（密码、Token、密钥）
- [ ] 没有包含调试代码（System.out.println、console.log）
- [ ] 没有包含未使用的 import
- [ ] 提交信息遵循 Conventional Commits 规范

### 构建检查（如适用）

- [ ] `mvn compile` 编译通过
- [ ] 相关单元测试通过
- [ ] 无新增 SonarLint 问题

---

## 错误恢复

### 误提交到错误分支

```bash
# 撤回最后一次提交（保留修改）
git reset --soft HEAD~1

# 切换到正确分支
git checkout <correct-branch>

# 重新提交
git add <files>
git commit -m "<message>"
```

### 提交了不该提交的文件

```bash
# 从暂存区移除（保留本地文件）
git rm --cached path/to/file

# 修正提交
git commit --amend --no-edit

# 安全推送（仅限未被他人拉取时）
git push --force-with-lease
```

### 秘钥/敏感信息误提交

```bash
# 立即从暂存区移除
git rm --cached path/to/secret-file
echo "path/to/secret-file" >> .gitignore
git commit --amend --no-edit
git push --force-with-lease

# 如果已推送且可能被拉取，必须立即：
# 1. 轮换（revoke + regenerate）泄露的密钥
# 2. 通知团队
```

### 提交信息写错了

```bash
# 修改最后一次提交信息（未推送时）
git commit --amend -m "<正确的提交信息>"

# 已推送时（谨慎使用）
git commit --amend -m "<正确的提交信息>"
git push --force-with-lease
```

---

## 强制约束

1. **提交前必须人工确认**: AI 展示 diff 后必须等用户确认，绝不自动提交
2. **冲突不自动解决**: 遇到冲突立即停止，提示用户手动 merge
3. **只提交相关文件**: 不要 `git add .`，只 add 本次修改的文件
4. **先 pull 后 push**: 必须先拉取最新代码再推送
5. **提交信息规范**: 遵循 `<type>(<scope>): <subject>` 格式
6. **不 force push**: 绝不使用 `git push --force`（仅 `--force-with-lease` 在错误恢复时允许）
7. **不跳过 hooks**: 绝不使用 `--no-verify`
8. **不提交敏感信息**: 提交前必须检查是否包含密码、Token、密钥
