#!/usr/bin/env python3
"""
ADM 报告生成脚本
基于架构分析结果生成 ADM 阶段性报告框架。

用法:
    python gen-adm-report.py <分析结果文件> --phase <ADM阶段> [--output <输出文件>]

示例:
    python gen-adm-report.py arch-analysis.json --phase A --output vision-report.md
    python gen-adm-report.py arch-analysis.json --phase B-D --output arch-definition.md
"""

import os
import sys
import json
import argparse
from datetime import datetime


# ADM 阶段报告模板
PHASE_TEMPLATES = {
    'preliminary': {
        'title': '预备阶段报告 — 架构能力评估',
        'sections': [
            ('1. 组织架构能力评估', [
                '- 当前架构成熟度级别',
                '- 架构团队组成和职责',
                '- 已有架构资产盘点',
                '- 架构工具和方法论',
            ]),
            ('2. 架构原则定义', [
                '| 编号 | 原则名称 | 声明 | 理由 | 影响 |',
                '|------|---------|------|------|------|',
                '| AP-001 | [原则名称] | [声明] | [理由] | [影响] |',
            ]),
            ('3. 框架定制', [
                '- ADM 裁剪说明',
                '- 适用的 TOGAF Series Guides',
                '- 组织特定扩展',
            ]),
            ('4. 治理框架初始化', [
                '- ARB 组织结构',
                '- 治理流程定义',
                '- 评审机制设计',
            ]),
        ]
    },
    'A': {
        'title': '阶段 A 报告 — 架构愿景',
        'sections': [
            ('1. 业务目标与驱动力', [
                '- 战略目标',
                '- 业务问题',
                '- 预期价值',
            ]),
            ('2. 利益相关者分析', [
                '| 利益相关者 | 角色 | 关注点 | 影响力 | 参与级别 |',
                '|-----------|------|--------|--------|---------|',
                '| [...] | [...] | [...] | 高/中/低 | [...] |',
            ]),
            ('3. 架构范围', [
                '| 维度 | 包含 | 排除 |',
                '|------|------|------|',
                '| 业务范围 | [...] | [...] |',
                '| 系统范围 | [...] | [...] |',
                '| 组织范围 | [...] | [...] |',
            ]),
            ('4. 架构愿景描述', [
                '- 目标架构高层视图',
                '- 关键架构变化',
                '- 价值主张',
            ]),
            ('5. 架构工作说明书', [
                '- 工作范围和方法',
                '- 时间表和里程碑',
                '- 资源需求',
            ]),
        ]
    },
    'B': {
        'title': '阶段 B 报告 — 业务架构',
        'sections': [
            ('1. 业务架构现状（Baseline）', [
                '- 业务能力地图',
                '- 核心业务流程',
                '- 组织结构和角色',
            ]),
            ('2. 业务架构目标（Target）', [
                '- 目标业务能力',
                '- 优化后的业务流程',
                '- 组织变更方案',
            ]),
            ('3. 差距分析', [
                '| 能力/流程 | 当前 | 目标 | 差距 | 优先级 |',
                '|-----------|------|------|------|--------|',
                '| [...] | [...] | [...] | [...] | 高/中/低 |',
            ]),
            ('4. 业务架构制品', [
                '- 业务能力目录',
                '- 组织/角色目录',
                '- 业务交互矩阵',
                '- 业务流程图',
            ]),
        ]
    },
    'C': {
        'title': '阶段 C 报告 — 信息系统架构（数据+应用）',
        'sections': [
            ('1. 数据架构', [
                '### 1.1 数据架构现状',
                '- 数据实体清单',
                '- 数据流向分析',
                '- 数据质量评估',
                '',
                '### 1.2 数据架构目标',
                '- 目标数据模型',
                '- 数据治理规则',
                '',
                '### 1.3 数据差距分析',
            ]),
            ('2. 应用架构', [
                '### 2.1 应用架构现状',
                '- 应用组合目录',
                '- 应用通信关系',
                '- TIME 评估',
                '',
                '### 2.2 应用架构目标',
                '- 目标应用组合',
                '- 集成方式优化',
                '',
                '### 2.3 应用差距分析',
            ]),
        ]
    },
    'D': {
        'title': '阶段 D 报告 — 技术架构',
        'sections': [
            ('1. 技术架构现状', [
                '- 技术标准目录',
                '- 技术参考模型（TRM）',
                '- 基础设施现状',
            ]),
            ('2. 技术架构目标', [
                '- 目标技术标准',
                '- 目标 TRM',
                '- 基础设施演进方案',
            ]),
            ('3. 非功能需求矩阵', [
                '| 服务 | 响应时间 | TPS | 可用性 | 安全级别 |',
                '|------|---------|-----|--------|---------|',
                '| [...] | [...] | [...] | [...] | [...] |',
            ]),
            ('4. 技术差距分析', [
                '| 技术域 | 当前 | 目标 | 差距 | 优先级 |',
                '|--------|------|------|------|--------|',
                '| [...] | [...] | [...] | [...] | 高/中/低 |',
            ]),
        ]
    },
    'E-F': {
        'title': '阶段 E-F 报告 — 机会与迁移规划',
        'sections': [
            ('1. 工作包定义', [
                '| 工作包 | 描述 | 涉及域 | 优先级 | 依赖 |',
                '|--------|------|--------|--------|------|',
                '| WP-01 | [...] | [...] | P0 | 无 |',
            ]),
            ('2. 过渡架构', [
                '- 过渡态 1 描述',
                '- 过渡态 2 描述',
                '- 目标态描述',
            ]),
            ('3. 架构路线图', [
                '### 短期（0-6个月）',
                '### 中期（6-18个月）',
                '### 长期（18-36个月）',
            ]),
            ('4. 资源与预算', [
                '| 阶段 | 人力 | 预算 | 时间 |',
                '|------|------|------|------|',
                '| [...] | [...] | [...] | [...] |',
            ]),
        ]
    },
    'G-H': {
        'title': '阶段 G-H 报告 — 实施治理与变更管理',
        'sections': [
            ('1. 架构合同', [
                '- 约束范围',
                '- 架构原则遵从要求',
                '- 技术标准遵从要求',
                '- 评审计划',
            ]),
            ('2. 合规性评审计划', [
                '| 评审节点 | 评审范围 | 评审人 | 时间 |',
                '|----------|---------|--------|------|',
                '| [...] | [...] | [...] | [...] |',
            ]),
            ('3. 变更管理流程', [
                '- 变更分类标准',
                '- 变更审批流程',
                '- 影响分析方法',
            ]),
            ('4. 架构度量', [
                '| 指标 | 目标值 | 度量方式 | 频率 |',
                '|------|--------|---------|------|',
                '| 合规率 | > 90% | 评审通过率 | 月度 |',
            ]),
        ]
    },
}


def load_analysis(file_path: str) -> dict:
    """加载分析结果"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def enrich_with_analysis(sections: list, analysis: dict) -> list:
    """用分析结果丰富报告内容"""
    if not analysis:
        return sections

    enriched = list(sections)

    # 自动填充技术栈信息
    tech_stack = analysis.get('tech_stack', {})
    if tech_stack:
        tech_lines = ['', '**自动检测到的技术栈**:', '']
        tech_lines.append('| 技术 | 使用服务数 |')
        tech_lines.append('|------|----------|')
        for tech, count in sorted(tech_stack.items(), key=lambda x: -x[1]):
            tech_lines.append(f'| {tech} | {count} |')
        enriched.append(('附录: 技术栈检测结果', tech_lines))

    # 自动填充服务信息
    services = analysis.get('services', [])
    if services:
        svc_lines = ['', '**自动检测到的服务**:', '']
        svc_lines.append('| 服务 | Controller | Service | Mapper | Entity |')
        svc_lines.append('|------|-----------|---------|--------|--------|')
        for svc in services:
            svc_lines.append(
                f"| {svc['name']} | {len(svc.get('controllers', []))} | "
                f"{len(svc.get('services', []))} | {len(svc.get('mappers', []))} | "
                f"{len(svc.get('entities', []))} |"
            )
        enriched.append(('附录: 服务清单', svc_lines))

    # 自动填充问题
    issues = analysis.get('issues', [])
    if issues:
        issue_lines = ['', '**自动检测到的问题**:', '']
        issue_lines.append('| 严重程度 | 类型 | 说明 |')
        issue_lines.append('|---------|------|------|')
        for issue in issues[:20]:
            issue_lines.append(f"| {issue['severity']} | {issue['type']} | {issue['message']} |")
        enriched.append(('附录: 检测到的架构问题', issue_lines))

    return enriched


def generate_report(phase: str, analysis: dict = None) -> str:
    """生成 ADM 报告"""
    template = PHASE_TEMPLATES.get(phase)
    if not template:
        return f"错误: 未知的 ADM 阶段: {phase}\n可选阶段: {', '.join(PHASE_TEMPLATES.keys())}"

    sections = template['sections']
    if analysis:
        sections = enrich_with_analysis(sections, analysis)

    lines = [
        f"# {template['title']}",
        "",
        f"**生成日期**: {datetime.now().strftime('%Y-%m-%d')}",
        f"**ADM 阶段**: {phase}",
        "",
        "---",
        "",
    ]

    for section_title, content in sections:
        lines.append(f"## {section_title}")
        lines.append("")
        for line in content:
            lines.append(line)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='ADM 报告生成脚本')
    parser.add_argument('analysis_file', nargs='?', help='架构分析结果文件（JSON格式）')
    parser.add_argument('--phase', '-p', required=True,
                        choices=['preliminary', 'A', 'B', 'C', 'D', 'E-F', 'G-H', 'B-D'],
                        help='ADM 阶段')
    parser.add_argument('--output', '-o', help='输出文件路径')
    args = parser.parse_args()

    analysis = {}
    if args.analysis_file:
        analysis = load_analysis(args.analysis_file)

    # B-D 生成合并报告
    if args.phase == 'B-D':
        reports = []
        for phase in ['B', 'C', 'D']:
            reports.append(generate_report(phase, analysis))
        output = "\n\n---\n\n".join(reports)
    else:
        output = generate_report(args.phase, analysis)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"报告已生成: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
