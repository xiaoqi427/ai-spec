https://github.com/anthropics/skills?spm=a2s0k.28103460.0.0.14ca6308D1NImp


# 安装与配置 OpenSkills
## 安装 OpenSkills 工具‌：首先，确保你的系统已安装 Node.js（版本 20.6+）。然后在终端中全局安装 OpenSkills：

bash
Copy Code
npm i -g openskills
## 安装官方技能包‌：从 Anthropic 官方市场安装技能。你可以选择安装到当前项目（仅对当前项目生效）或全局（对所有项目生效）。

### 项目级别安装‌（推荐，仅影响当前 Qoder 项目）：
bash
Copy Code
openskills install anthropics/skills
### 全局安装‌：
bash
Copy Code
openskills install anthropics/skills --global
安装成功后，技能文件会被下载到 .claude/skills/ 目录下。

## 同步技能到 Qoder‌：这是关键一步，需要创建一个 AGENTS.md 文件来告诉 Qoder 可用的技能列表。

在你的 Qoder 项目根目录下创建一个名为 AGENTS.md 的文件（如果不存在）。
运行同步命令，将已安装的技能写入该文件：
bash
Copy Code
openskills sync --output .qoder/rules/AGENTS.md
命令会提示你选择要包含的技能，确认后，AGENTS.md 文件将被更新。
## 在 Qoder 中使用技能
配置完成后，你就可以在 Qoder 的提示词中直接调用技能了。例如：

‌将 README.md 转为 PDF‌：在 Qoder 中输入提示词：“把当前项目的 README.md 使用 pdf 技能转为 PDF 并放到项目中”。
‌处理 Excel 文件‌：输入提示词：“用 xlsx 技能分析这个销售数据表，并生成一个摘要”。
Qoder 会根据 AGENTS.md 文件中的指令，自动调用相应的技能来完成任务