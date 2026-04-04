---
name: test-case-ref
description: 解析项目 Excel 测试用例，按模块/功能索引，为 Bug 修复提供业务上下文参考。支持三种操作: parse（解析 Excel 生成索引）、lookup（按模块/关键词查找）、enrich（给定 Bug 上下文自动匹配）。测试用例仅供参考，不作为修复通过/失败的判定指标。当需要理解 Bug 对应的业务场景、操作步骤和预期行为时使用。
---
# Test Case Reference (测试用例参考)

@author: sevenxiao

## 概述

此 skill 将项目中散布在 Excel 文件中的**功能测试用例**解析为结构化索引，在 Bug 修复流程中提供业务上下文参考。

核心能力:
1. **`parse`** - 解析 Excel 测试用例文件 → 生成 `test-case-index.json` 索引
2. **`lookup`** - 按模块/模板号(T044/T047)或关键词查找相关测试用例
3. **`enrich`** - 给定 Bug 上下文，自动匹配相关测试用例作为分析补充

> **重要**: 测试用例仅供参考，帮助理解业务场景。测试用例本身不一定准确，**不作为 Bug 修复的通过/失败判定指标**。

---

## 测试用例来源

测试用例存放在本 skill 的 `doc/` 目录下，按业务域分文件夹组织:

```
ai-spec/skills/code/bug-fix-cycle/test-case-ref/doc/
├── otc/                  # OTC 销售
│   ├── 系统运维-基础数据配置-OTC销售-手工发票报账单配置.xlsx
│   └── 系统运维-基础数据配置-OTC销售-收款方法配置.xlsx
├── ptp/                  # PTP 采购（待补充）
├── tr/                   # TR 差旅（待补充）
└── ...
```

每个 Excel 文件包含标准测试用例格式（详见 [references/test-case-format.md](references/test-case-format.md)）。

---

## 输出索引位置

```
yili-out/test-case-index/
└── test-case-index.json
```

---

## 使用方式

### 1. parse — 解析测试用例

解析指定目录下的 Excel 测试用例文件，生成结构化索引。

```bash
# 解析整个 doc 目录
/skill test-case-ref parse --dir ai-spec/skills/code/bug-fix-cycle/test-case-ref/doc/

# 解析指定文件
/skill test-case-ref parse --file ai-spec/skills/code/bug-fix-cycle/test-case-ref/doc/otc/系统运维-基础数据配置-OTC销售-手工发票报账单配置.xlsx

# 增量更新（仅解析新增/修改的文件）
/skill test-case-ref parse --dir ai-spec/skills/code/bug-fix-cycle/test-case-ref/doc/ --incremental
```

**执行脚本**:
```bash
python3 ai-spec/skills/code/bug-fix-cycle/test-case-ref/scripts/parse_test_cases.py \
  --input <目录或文件路径> \
  --output yili-out/test-case-index/test-case-index.json
```

**输出**: `yili-out/test-case-index/test-case-index.json`

### 2. lookup — 查找测试用例

按模块、模板号或关键词查找相关测试用例。

```bash
# 按模板号查找
/skill test-case-ref lookup T047

# 按关键词查找
/skill test-case-ref lookup 收款方法

# 按模块查找
/skill test-case-ref lookup OTC-手工发票报账单配置

# 按 Bug ID 关联查找（通过问题编号列）
/skill test-case-ref lookup --bug-id 5001
```

**执行方式**: 读取 `yili-out/test-case-index/test-case-index.json`，检索匹配项。

**输出示例**:
```markdown
## 相关测试用例（仅供参考）

来源: 系统运维-基础数据配置-OTC销售-手工发票报账单配置.xlsx
模块: OTC-手工发票报账单配置

| # | 用例描述 | 操作步骤 | 预期结果 | 测试结论 |
|---|---------|---------|---------|---------|
| 1 | 初始化页面查询条件展示验证 | 1. 进入报账单配置页面... | 查询条件展示:... | 通过 |
| 2 | 验证"报账单模板"下拉可选值 | 1. 点击下拉框... | 下拉列表展示... | 通过 |

⚠️ 以上测试用例仅供参考，不一定完全准确
```

### 3. enrich — 自动匹配 Bug 上下文

给定 Bug 的标题、描述和模块信息，自动匹配相关测试用例并输出参考上下文。

```bash
# 自动匹配
/skill test-case-ref enrich --bug-title "T047 手工发票报账单配置查询报错" --module T047
```

**匹配策略** (按优先级):
1. Bug 问题编号直接关联（`问题编号` 列）
2. 模板号匹配（T044/T047 等）
3. 功能关键词匹配（查询/新增/删除/导出 等）
4. 业务域匹配（OTC/PTP/TR 等）

**输出**: 匹配到的测试用例列表，按相关度排序，限制最多 10 条。

---

## 索引结构

`test-case-index.json` 的完整结构:

```json
{
  "version": "1.0",
  "parsed_at": "2026-04-04T10:00:00",
  "source_dir": "ai-spec/skills/code/bug-fix-cycle/test-case-ref/doc/",
  "source_files": [
    {
      "path": "otc/系统运维-基础数据配置-OTC销售-手工发票报账单配置.xlsx",
      "last_modified": "2026-03-22T00:00:00",
      "sheet_count": 1,
      "case_count": 12
    }
  ],
  "modules": {
    "OTC-手工发票报账单配置": {
      "source_file": "otc/系统运维-基础数据配置-OTC销售-手工发票报账单配置.xlsx",
      "business_domain": "otc",
      "total_cases": 12,
      "features": {
        "查询条件": [
          {
            "id": 1,
            "description": "初始化页面查询条件展示验证",
            "precondition": "登录系统并进入手工发票报账单配置列表界面",
            "steps": "1. 进入报账单配置页面；2. 查看查询条件区域",
            "expected": "查询条件展示：报账单模板下拉框、类型下拉框、数量下拉框，布局清晰可交互",
            "actual_input": null,
            "actual_output": "符合预期",
            "result": "通过",
            "bug_id": null,
            "keywords": ["报账单模板", "下拉框", "查询条件", "类型", "数量"]
          }
        ],
        "功能按钮": [],
        "查询结果": []
      }
    }
  },
  "keyword_index": {
    "T047": ["OTC-手工发票报账单配置"],
    "手工发票": ["OTC-手工发票报账单配置"],
    "收款方法": ["OTC-收款方法配置"],
    "报账单模板": ["OTC-手工发票报账单配置"],
    "重置": ["OTC-手工发票报账单配置", "OTC-收款方法配置"],
    "删除": ["OTC-手工发票报账单配置"],
    "导出": ["OTC-收款方法配置"],
    "分页": ["OTC-收款方法配置"]
  },
  "bug_index": {
    "5001": ["OTC-手工发票报账单配置/查询条件/3"]
  }
}
```

---

## 在 Pipeline 中的位置

### Phase 1 (预采集)

```
1.5.1 [可选] 解析测试用例索引
    test-case-ref.parse(docs-dir)
    → 生成 yili-out/test-case-index/test-case-index.json
    → 如果索引已存在且未过期，跳过此步
```

### Phase 2 (分诊台)

```
2.2 对每个 Bug 做初步分类
    → 标题/描述 → 前端/后端/混合
    → [可选] test-case-ref.lookup → 是否有相关测试用例
    → 分诊表格展示: "测试用例" 列 (有 N 条 / 无)
```

### Phase 3 (批量修复)

```
3.2.1 [可选] 加载相关测试用例参考 (test-case-ref.lookup)
    → 根据 Bug 的模块(T044/T047)和关键词匹配相关测试用例
    → 输出: 相关测试用例列表（操作步骤+预期结果）
    → 作为 yili-code-fix.analyze 的补充上下文
    → ⚠️ 仅供参考，测试用例不一定准确
```

---

## 关键设计原则

1. **仅供参考**: 测试用例不一定准确，不作为修复通过/失败指标。在所有输出中明确标注 "⚠️ 仅供参考"
2. **可选步骤**: Pipeline 中测试用例加载标记为 `[可选]`，没有测试用例不阻塞修复流程
3. **增量解析**: 支持增量更新，新增 Excel 文件时不需重新解析全部
4. **多维匹配**: 通过模板号(T044/T047)、功能名词、Bug 问题编号三种方式匹配
5. **离线查询**: parse 生成索引后，lookup 和 enrich 纯离线操作，不依赖外部服务

---

## 参考

- 测试用例格式说明: [references/test-case-format.md](references/test-case-format.md)
- 解析脚本: [scripts/parse_test_cases.py](scripts/parse_test_cases.py)
- Pipeline 编排器: `ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/SKILL.md`
