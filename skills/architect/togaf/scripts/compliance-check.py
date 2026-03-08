#!/usr/bin/env python3
"""
架构合规性检查脚本
自动化检查项目代码是否符合架构原则和技术标准。

用法:
    python compliance-check.py <代码路径> [--standards <标准文件>] [--output <输出文件>]

示例:
    python compliance-check.py ./fssc-claim-service
    python compliance-check.py ./fssc-config-service --output compliance-report.md
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CheckResult:
    """检查结果"""
    category: str
    check_item: str
    status: str  # PASS / WARN / FAIL
    description: str
    file_path: str = ""
    line_number: int = 0
    suggestion: str = ""


@dataclass
class ComplianceReport:
    """合规性报告"""
    scan_path: str
    scan_time: str = ""
    total_checks: int = 0
    passed: int = 0
    warnings: int = 0
    failures: int = 0
    results: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)


# 检查规则定义
COMPLIANCE_RULES = {
    '分层架构': {
        'controller_no_mapper': {
            'description': 'Controller 不应直接注入 Mapper',
            'file_pattern': r'Controller\.java$',
            'fail_pattern': r'(@Resource|@Autowired)\s+\w*Mapper\b',
            'suggestion': '请通过 Business 层调用 DoService 层，再由 DoService 调用 Mapper',
        },
        'controller_no_direct_db': {
            'description': 'Controller 不应包含数据库操作',
            'file_pattern': r'Controller\.java$',
            'fail_pattern': r'\.selectList|\.selectById|\.insert|\.updateById|\.deleteById',
            'suggestion': '数据库操作应在 Mapper/DoService 层完成',
        },
        'doservice_no_if': {
            'description': 'DO Service 不应包含业务逻辑（if语句）',
            'file_pattern': r'DoServiceImpl\.java$',
            'fail_pattern': r'\bif\s*\(',
            'suggestion': '业务逻辑应在 Business 层处理，DoService 只负责与 Mapper 交互',
        },
        'doservice_no_sql': {
            'description': 'DO Service 不应包含 SQL 语句',
            'file_pattern': r'DoServiceImpl\.java$',
            'fail_pattern': r'@Select|@Insert|@Update|@Delete|SELECT\s+|INSERT\s+|UPDATE\s+|DELETE\s+',
            'suggestion': 'SQL 应在 Mapper 层（XML 或注解）中定义',
        },
    },
    '代码规范': {
        'no_system_out': {
            'description': '不应使用 System.out.println',
            'file_pattern': r'\.java$',
            'fail_pattern': r'System\.(out|err)\.(println|print|printf)',
            'suggestion': '请使用 @Slf4j + log.info/error/debug',
        },
        'no_reflection_copy': {
            'description': '不应使用反射进行对象复制',
            'file_pattern': r'\.java$',
            'fail_pattern': r'BeanUtils\.copyProperties|PropertyUtils\.copyProperties|BeanCopier',
            'suggestion': '请使用 MapStruct 进行对象转换',
        },
        'use_lombok': {
            'description': 'DO/DTO 类应使用 Lombok 注解',
            'file_pattern': r'(Do|Dto|DTO)\.java$',
            'pass_pattern': r'@Data|@Getter|@Setter|@Builder',
            'suggestion': '请使用 @Data 或 @Getter/@Setter 注解',
        },
        'no_magic_numbers': {
            'description': '不应使用魔法数字',
            'file_pattern': r'(Service|Business|Controller).*\.java$',
            'fail_pattern': r'==\s*\d{2,}|>\s*\d{2,}|<\s*\d{2,}',
            'suggestion': '请将数字定义为有意义的常量',
        },
    },
    '安全规范': {
        'no_hardcoded_password': {
            'description': '不应硬编码密码',
            'file_pattern': r'\.java$|\.yml$|\.yaml$|\.properties$',
            'fail_pattern': r'password\s*=\s*"[^"]{3,}"|password:\s+\S{3,}(?!.*\$\{)',
            'suggestion': '密码应通过配置中心或环境变量注入',
        },
        'no_hardcoded_token': {
            'description': '不应硬编码 Token/Secret',
            'file_pattern': r'\.java$',
            'fail_pattern': r'(token|secret|apiKey)\s*=\s*"[^"]{10,}"',
            'suggestion': 'Token/Secret 应通过配置中心管理',
        },
    },
    '技术标准': {
        'java_version': {
            'description': '应使用 Java 21',
            'file_pattern': r'pom\.xml$',
            'pass_pattern': r'<java\.version>21</java\.version>|<source>21</source>|<release>21</release>',
            'suggestion': '请升级到 Java 21',
        },
        'mapstruct_usage': {
            'description': '对象转换应使用 MapStruct',
            'file_pattern': r'Converter\.java$',
            'pass_pattern': r'@org\.mapstruct\.Mapper|@Mapper\(componentModel',
            'suggestion': '请使用 MapStruct @Mapper 注解',
        },
    },
    '事务管理': {
        'transaction_rollback': {
            'description': '@Transactional 应指定 rollbackFor',
            'file_pattern': r'\.java$',
            'fail_pattern': r'@Transactional(?!\(.*rollbackFor)',
            'suggestion': '请添加 rollbackFor = Exception.class',
        },
        'no_transaction_in_controller': {
            'description': 'Controller 不应使用 @Transactional',
            'file_pattern': r'Controller\.java$',
            'fail_pattern': r'@Transactional',
            'suggestion': '事务管理应在 Business/Service 层',
        },
    },
}


def scan_files(path: str, pattern: str) -> list:
    """扫描匹配的文件"""
    matched = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ('test', 'target', 'build', '.git', 'node_modules')]
        for f in files:
            if re.search(pattern, f):
                matched.append(os.path.join(root, f))
    return matched


def check_file(file_path: str, rule: dict) -> list:
    """对文件执行检查"""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except (UnicodeDecodeError, IOError):
        return results

    file_name = os.path.basename(file_path)

    # 失败模式检查
    if 'fail_pattern' in rule:
        for i, line in enumerate(lines, 1):
            if re.search(rule['fail_pattern'], line):
                results.append(CheckResult(
                    category='',
                    check_item=rule['description'],
                    status='FAIL',
                    description=f'第 {i} 行: {line.strip()[:80]}',
                    file_path=file_path,
                    line_number=i,
                    suggestion=rule.get('suggestion', ''),
                ))

    # 通过模式检查（整个文件应包含）
    if 'pass_pattern' in rule and 'fail_pattern' not in rule:
        if not re.search(rule['pass_pattern'], content):
            results.append(CheckResult(
                category='',
                check_item=rule['description'],
                status='WARN',
                description=f'{file_name} 未检测到符合要求的模式',
                file_path=file_path,
                suggestion=rule.get('suggestion', ''),
            ))

    return results


def run_compliance_check(path: str) -> ComplianceReport:
    """执行合规性检查"""
    report = ComplianceReport(
        scan_path=path,
        scan_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )

    for category, rules in COMPLIANCE_RULES.items():
        for rule_name, rule in rules.items():
            files = scan_files(path, rule['file_pattern'])
            for file_path in files:
                check_results = check_file(file_path, rule)
                for result in check_results:
                    result.category = category
                    report.results.append(result)

            # 如果检查了文件但没有发现问题，记录 PASS
            if files and not any(r for r in report.results
                                 if r.check_item == rule['description']
                                 and r.status in ('FAIL', 'WARN')):
                report.results.append(CheckResult(
                    category=category,
                    check_item=rule['description'],
                    status='PASS',
                    description=f'检查了 {len(files)} 个文件，全部通过',
                ))

    # 统计
    report.total_checks = len(report.results)
    report.passed = len([r for r in report.results if r.status == 'PASS'])
    report.warnings = len([r for r in report.results if r.status == 'WARN'])
    report.failures = len([r for r in report.results if r.status == 'FAIL'])

    # 分类汇总
    category_summary = defaultdict(lambda: {'pass': 0, 'warn': 0, 'fail': 0})
    for r in report.results:
        category_summary[r.category][r.status.lower()] += 1
    report.summary = dict(category_summary)

    return report


def format_markdown(report: ComplianceReport) -> str:
    """输出 Markdown 格式报告"""
    pass_rate = (report.passed / report.total_checks * 100) if report.total_checks > 0 else 0
    overall = '合规' if report.failures == 0 else ('有条件合规' if report.failures < 5 else '不合规')

    lines = [
        "# 架构合规性检查报告",
        "",
        f"**扫描路径**: `{report.scan_path}`",
        f"**检查时间**: {report.scan_time}",
        f"**总体结论**: **{overall}**",
        "",
        "---",
        "",
        "## 1. 概览",
        "",
        "| 指标 | 数量 |",
        "|------|------|",
        f"| 总检查项 | {report.total_checks} |",
        f"| ✅ 通过 | {report.passed} |",
        f"| ⚠️ 警告 | {report.warnings} |",
        f"| ❌ 失败 | {report.failures} |",
        f"| 合规率 | {pass_rate:.1f}% |",
        "",
    ]

    # 分类汇总
    if report.summary:
        lines += ["## 2. 分类汇总", "",
                   "| 分类 | ✅通过 | ⚠️警告 | ❌失败 | 状态 |",
                   "|------|-------|-------|-------|------|"]
        for category, counts in sorted(report.summary.items()):
            status = '✅' if counts['fail'] == 0 and counts['warn'] == 0 else (
                '⚠️' if counts['fail'] == 0 else '❌')
            lines.append(
                f"| {category} | {counts['pass']} | {counts['warn']} | {counts['fail']} | {status} |")
        lines.append("")

    # 失败项详情
    failures = [r for r in report.results if r.status == 'FAIL']
    if failures:
        lines += ["## 3. 失败项详情", "",
                   "| 分类 | 检查项 | 文件 | 行号 | 说明 | 建议 |",
                   "|------|--------|------|------|------|------|"]
        for r in failures:
            file_name = os.path.basename(r.file_path) if r.file_path else '-'
            lines.append(
                f"| {r.category} | {r.check_item} | `{file_name}` | "
                f"{r.line_number or '-'} | {r.description[:50]} | {r.suggestion} |")
        lines.append("")

    # 警告项
    warnings = [r for r in report.results if r.status == 'WARN']
    if warnings:
        lines += ["## 4. 警告项", "",
                   "| 分类 | 检查项 | 文件 | 说明 | 建议 |",
                   "|------|--------|------|------|------|"]
        for r in warnings:
            file_name = os.path.basename(r.file_path) if r.file_path else '-'
            lines.append(
                f"| {r.category} | {r.check_item} | `{file_name}` | "
                f"{r.description[:50]} | {r.suggestion} |")
        lines.append("")

    # 改进建议
    lines += [
        "## 5. 改进建议",
        "",
        "### 优先修复（高优先级）",
        "",
    ]
    for r in failures[:5]:
        lines.append(f"1. **{r.check_item}** — {r.suggestion}")
    if not failures:
        lines.append("无高优先级问题")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='架构合规性检查脚本')
    parser.add_argument('path', help='要检查的代码路径')
    parser.add_argument('--standards', '-s', help='自定义标准文件（YAML/JSON）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='输出格式')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    print(f"正在检查: {args.path} ...")
    report = run_compliance_check(args.path)

    if args.format == 'json':
        output = json.dumps({
            'scan_path': report.scan_path,
            'scan_time': report.scan_time,
            'total_checks': report.total_checks,
            'passed': report.passed,
            'warnings': report.warnings,
            'failures': report.failures,
            'summary': report.summary,
        }, indent=2, ensure_ascii=False)
    else:
        output = format_markdown(report)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"检查报告已输出到: {args.output}")
        print(f"结果: ✅{report.passed} ⚠️{report.warnings} ❌{report.failures}")
    else:
        print(output)


if __name__ == '__main__':
    main()
