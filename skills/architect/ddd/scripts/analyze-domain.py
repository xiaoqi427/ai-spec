#!/usr/bin/env python3
"""
DDD 领域分析脚本
从 Java 代码库中提取领域概念，识别实体、值对象、服务和聚合候选。

用法:
    python analyze-domain.py <代码路径> [--output <输出文件>] [--format yaml|json|md]

示例:
    python analyze-domain.py ./fssc-claim-service
    python analyze-domain.py ./src/main/java/com/yili/claim --output domain-analysis.md --format md
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class DomainConcept:
    """领域概念"""
    name: str
    type: str  # entity / value_object / aggregate_root / domain_service / repository / factory
    file_path: str
    package: str
    annotations: list = field(default_factory=list)
    fields: list = field(default_factory=list)
    methods: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    notes: str = ""


@dataclass
class AnalysisResult:
    """分析结果"""
    scan_path: str
    total_files: int = 0
    entities: list = field(default_factory=list)
    value_objects: list = field(default_factory=list)
    aggregate_roots: list = field(default_factory=list)
    domain_services: list = field(default_factory=list)
    repositories: list = field(default_factory=list)
    factories: list = field(default_factory=list)
    controllers: list = field(default_factory=list)
    app_services: list = field(default_factory=list)
    packages: list = field(default_factory=list)
    issues: list = field(default_factory=list)


# 识别规则
ENTITY_PATTERNS = [
    r'@Entity',
    r'@Table',
    r'@TableName',
    r'extends\s+.*Do\b',
    r'extends\s+BaseDo\b',
]

VALUE_OBJECT_PATTERNS = [
    r'\brecord\s+\w+',
    r'@Value',
    r'@Immutable',
]

SERVICE_PATTERNS = [
    r'@Service',
    r'@Component',
    r'implements\s+I\w+Service',
]

REPOSITORY_PATTERNS = [
    r'@Repository',
    r'extends\s+BaseMapper',
    r'extends\s+JpaRepository',
    r'interface\s+\w+Repository',
    r'interface\s+\w+Mapper',
]

CONTROLLER_PATTERNS = [
    r'@RestController',
    r'@Controller',
]

AGGREGATE_ROOT_HINTS = [
    r'extends\s+AggregateRoot',
    r'List<\w+Event>',
    r'registerEvent',
    r'getDomainEvents',
]

ANTI_PATTERNS = {
    'anemic_model': r'class\s+\w+\s*\{[^}]*(?:get\w+|set\w+|is\w+)[^}]*\}',
    'god_class': None,  # 通过方法数检测
    'cross_layer_call': None,  # 通过依赖分析检测
}


def scan_java_files(path: str) -> list:
    """扫描目录下的所有 Java 文件"""
    java_files = []
    for root, dirs, files in os.walk(path):
        # 跳过测试目录和构建目录
        dirs[:] = [d for d in dirs if d not in ('test', 'target', 'build', '.git', 'node_modules')]
        for f in files:
            if f.endswith('.java'):
                java_files.append(os.path.join(root, f))
    return java_files


def extract_package(content: str) -> str:
    """提取包名"""
    match = re.search(r'^package\s+([\w.]+);', content, re.MULTILINE)
    return match.group(1) if match else ""


def extract_class_name(content: str) -> str:
    """提取类名"""
    match = re.search(r'(?:class|interface|enum|record)\s+(\w+)', content)
    return match.group(1) if match else ""


def extract_annotations(content: str) -> list:
    """提取类级别注解"""
    annotations = re.findall(r'^@(\w+)(?:\([^)]*\))?', content, re.MULTILINE)
    return list(set(annotations))


def extract_fields(content: str) -> list:
    """提取字段"""
    fields = re.findall(
        r'(?:private|protected|public)\s+(?:final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*[;=]',
        content
    )
    return [{'type': t, 'name': n} for t, n in fields]


def extract_methods(content: str) -> list:
    """提取公共方法"""
    methods = re.findall(
        r'public\s+(?:static\s+)?(?:<[^>]+>\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)',
        content
    )
    return [{'return_type': r, 'name': n, 'params': p.strip()} for r, n, p in methods
            if n not in ('main', 'toString', 'hashCode', 'equals')]


def extract_imports(content: str) -> list:
    """提取导入"""
    return re.findall(r'^import\s+([\w.]+);', content, re.MULTILINE)


def classify_concept(file_path: str, content: str) -> Optional[DomainConcept]:
    """分类领域概念"""
    class_name = extract_class_name(content)
    if not class_name:
        return None

    package = extract_package(content)
    annotations = extract_annotations(content)
    fields = extract_fields(content)
    methods = extract_methods(content)
    imports = extract_imports(content)

    concept = DomainConcept(
        name=class_name,
        type="unknown",
        file_path=file_path,
        package=package,
        annotations=annotations,
        fields=fields,
        methods=methods,
        dependencies=[i.split('.')[-1] for i in imports if 'com.yili' in i]
    )

    # 判断是否是聚合根
    if any(re.search(p, content) for p in AGGREGATE_ROOT_HINTS):
        concept.type = "aggregate_root"
        return concept

    # 判断类型
    if any(re.search(p, content) for p in CONTROLLER_PATTERNS):
        concept.type = "controller"
    elif any(re.search(p, content) for p in REPOSITORY_PATTERNS):
        concept.type = "repository"
    elif any(re.search(p, content) for p in ENTITY_PATTERNS):
        concept.type = "entity"
    elif any(re.search(p, content) for p in VALUE_OBJECT_PATTERNS):
        concept.type = "value_object"
    elif any(re.search(p, content) for p in SERVICE_PATTERNS):
        # 区分领域服务和应用服务
        if 'ApplicationService' in class_name or 'AppService' in class_name:
            concept.type = "app_service"
        elif 'business' in package or 'domain' in package:
            concept.type = "domain_service"
        else:
            concept.type = "app_service"
    elif class_name.endswith('Factory'):
        concept.type = "factory"
    elif len(methods) <= 3 and all(m['name'].startswith(('get', 'is', 'of', 'from')) for m in methods):
        concept.type = "value_object"

    return concept


def detect_issues(concepts: list) -> list:
    """检测设计问题"""
    issues = []

    for c in concepts:
        # 贫血模型检测
        if c.type == 'entity':
            business_methods = [m for m in c.methods
                                if not m['name'].startswith(('get', 'set', 'is', 'has'))]
            if len(business_methods) == 0 and len(c.fields) > 3:
                issues.append({
                    'type': 'ANEMIC_MODEL',
                    'severity': 'WARNING',
                    'class': c.name,
                    'message': f'实体 {c.name} 疑似贫血模型：有 {len(c.fields)} 个字段但无业务方法'
                })

        # 上帝类检测
        if len(c.methods) > 20:
            issues.append({
                'type': 'GOD_CLASS',
                'severity': 'WARNING',
                'class': c.name,
                'message': f'{c.name} 有 {len(c.methods)} 个公共方法，可能职责过多'
            })

        # 依赖过多检测
        if len(c.dependencies) > 10:
            issues.append({
                'type': 'HIGH_COUPLING',
                'severity': 'INFO',
                'class': c.name,
                'message': f'{c.name} 依赖了 {len(c.dependencies)} 个内部类，耦合度较高'
            })

    return issues


def analyze(path: str) -> AnalysisResult:
    """执行领域分析"""
    result = AnalysisResult(scan_path=path)
    java_files = scan_java_files(path)
    result.total_files = len(java_files)
    packages = set()

    for file_path in java_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, IOError):
            continue

        concept = classify_concept(file_path, content)
        if not concept:
            continue

        packages.add(concept.package)

        category_map = {
            'entity': result.entities,
            'value_object': result.value_objects,
            'aggregate_root': result.aggregate_roots,
            'domain_service': result.domain_services,
            'repository': result.repositories,
            'factory': result.factories,
            'controller': result.controllers,
            'app_service': result.app_services,
        }
        target = category_map.get(concept.type)
        if target is not None:
            target.append(concept)

    result.packages = sorted(packages)
    all_concepts = (result.entities + result.value_objects + result.aggregate_roots +
                    result.domain_services + result.repositories + result.factories +
                    result.controllers + result.app_services)
    result.issues = detect_issues(all_concepts)
    return result


def format_markdown(result: AnalysisResult) -> str:
    """输出 Markdown 格式报告"""
    lines = [
        f"# 领域分析报告",
        f"",
        f"**扫描路径**: `{result.scan_path}`",
        f"**扫描文件数**: {result.total_files}",
        f"",
        f"---",
        f"",
        f"## 概览",
        f"",
        f"| 分类 | 数量 |",
        f"|------|------|",
        f"| 聚合根 | {len(result.aggregate_roots)} |",
        f"| 实体 | {len(result.entities)} |",
        f"| 值对象 | {len(result.value_objects)} |",
        f"| 领域服务 | {len(result.domain_services)} |",
        f"| 应用服务 | {len(result.app_services)} |",
        f"| 仓储/Mapper | {len(result.repositories)} |",
        f"| 工厂 | {len(result.factories)} |",
        f"| Controller | {len(result.controllers)} |",
        f"",
    ]

    def render_concept_table(title, concepts):
        if not concepts:
            return []
        rows = [f"## {title}", "", "| 名称 | 包路径 | 字段数 | 方法数 |", "|------|--------|-------|--------|"]
        for c in concepts:
            rows.append(f"| {c.name} | {c.package} | {len(c.fields)} | {len(c.methods)} |")
        rows.append("")
        return rows

    lines += render_concept_table("聚合根", result.aggregate_roots)
    lines += render_concept_table("实体", result.entities)
    lines += render_concept_table("值对象", result.value_objects)
    lines += render_concept_table("领域服务", result.domain_services)
    lines += render_concept_table("应用服务", result.app_services)
    lines += render_concept_table("仓储/Mapper", result.repositories)
    lines += render_concept_table("Controller", result.controllers)

    if result.issues:
        lines += ["## 潜在问题", ""]
        lines += ["| 类型 | 严重程度 | 类名 | 说明 |", "|------|---------|------|------|"]
        for issue in result.issues:
            lines.append(f"| {issue['type']} | {issue['severity']} | {issue['class']} | {issue['message']} |")
        lines.append("")

    if result.packages:
        lines += ["## 包结构", ""]
        for pkg in result.packages:
            lines.append(f"- `{pkg}`")
        lines.append("")

    return "\n".join(lines)


def format_json(result: AnalysisResult) -> str:
    """输出 JSON 格式"""
    data = {
        'scan_path': result.scan_path,
        'total_files': result.total_files,
        'summary': {
            'aggregate_roots': len(result.aggregate_roots),
            'entities': len(result.entities),
            'value_objects': len(result.value_objects),
            'domain_services': len(result.domain_services),
            'app_services': len(result.app_services),
            'repositories': len(result.repositories),
            'factories': len(result.factories),
            'controllers': len(result.controllers),
        },
        'aggregate_roots': [asdict(c) for c in result.aggregate_roots],
        'entities': [asdict(c) for c in result.entities],
        'value_objects': [asdict(c) for c in result.value_objects],
        'domain_services': [asdict(c) for c in result.domain_services],
        'issues': result.issues,
        'packages': result.packages,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='DDD 领域分析脚本')
    parser.add_argument('path', help='要分析的代码路径')
    parser.add_argument('--output', '-o', help='输出文件路径（默认输出到控制台）')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='输出格式')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    print(f"正在分析: {args.path} ...")
    result = analyze(args.path)

    if args.format == 'json':
        output = format_json(result)
    else:
        output = format_markdown(result)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"分析报告已输出到: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
