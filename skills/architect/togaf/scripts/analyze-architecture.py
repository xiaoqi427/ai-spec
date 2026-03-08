#!/usr/bin/env python3
"""
TOGAF 架构分析脚本
从 Java 代码库中提取架构特征，分析分层结构、服务依赖、技术栈和潜在架构问题。

用法:
    python analyze-architecture.py <代码路径> [--output <输出文件>] [--format md|json]

示例:
    python analyze-architecture.py ./fssc-claim-service
    python analyze-architecture.py ./fssc-config-service --output arch-analysis.md --format md
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
class ServiceInfo:
    """服务信息"""
    name: str
    path: str
    modules: list = field(default_factory=list)
    controllers: list = field(default_factory=list)
    services: list = field(default_factory=list)
    mappers: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    feign_clients: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    tech_stack: list = field(default_factory=list)


@dataclass
class ArchitectureAnalysis:
    """架构分析结果"""
    scan_path: str
    services: list = field(default_factory=list)
    layer_violations: list = field(default_factory=list)
    tech_stack_summary: dict = field(default_factory=dict)
    dependency_graph: dict = field(default_factory=dict)
    issues: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)


# 层级识别模式
LAYER_PATTERNS = {
    'controller': [r'@RestController', r'@Controller', r'Controller\b'],
    'business': [r'business', r'Business'],
    'service': [r'@Service', r'DoService', r'ServiceImpl'],
    'mapper': [r'@Mapper', r'extends\s+BaseMapper', r'Mapper\b'],
    'entity': [r'@TableName', r'@Entity', r'extends\s+.*Do\b'],
    'dto': [r'Dto\b', r'DTO\b', r'Param\b', r'Request\b', r'Response\b'],
    'feign': [r'@FeignClient', r'Feign\b'],
}

# 技术栈识别
TECH_PATTERNS = {
    'Spring Boot': r'spring-boot',
    'Spring Cloud': r'spring-cloud',
    'MyBatis Plus': r'mybatis-plus',
    'Redis': r'spring-boot-starter-data-redis|jedis|lettuce',
    'RabbitMQ': r'spring-boot-starter-amqp|rabbitmq',
    'MySQL': r'mysql-connector',
    'MongoDB': r'spring-boot-starter-data-mongodb',
    'Nacos': r'nacos',
    'MapStruct': r'mapstruct',
    'Lombok': r'lombok',
    'Swagger/OpenAPI': r'springdoc|swagger|openapi',
}

# 架构反模式检测
ANTI_PATTERNS = {
    'controller_calls_mapper': {
        'desc': 'Controller 层直接调用 Mapper（跨层调用）',
        'severity': 'HIGH',
        'pattern': r'Controller.*Mapper|Controller.*Repository',
    },
    'service_has_business_logic': {
        'desc': 'DO Service 包含 if 逻辑（应在 Business 层）',
        'severity': 'MEDIUM',
    },
    'missing_business_layer': {
        'desc': '缺少 Business 层，Controller 直接调用 Service',
        'severity': 'MEDIUM',
    },
    'reflection_copy': {
        'desc': '使用反射进行对象复制（应使用 MapStruct）',
        'severity': 'HIGH',
        'pattern': r'BeanUtils\.copyProperties|PropertyUtils\.copyProperties',
    },
    'system_out': {
        'desc': '使用 System.out.println（应使用 @Slf4j）',
        'severity': 'LOW',
        'pattern': r'System\.out\.println|System\.err\.println',
    },
}


def scan_java_files(path: str) -> list:
    """扫描目录下的所有 Java 文件"""
    java_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ('test', 'target', 'build', '.git', 'node_modules')]
        for f in files:
            if f.endswith('.java'):
                java_files.append(os.path.join(root, f))
    return java_files


def scan_pom_files(path: str) -> list:
    """扫描 POM 文件"""
    pom_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ('target', 'build', '.git')]
        for f in files:
            if f == 'pom.xml':
                pom_files.append(os.path.join(root, f))
    return pom_files


def classify_file(file_path: str, content: str) -> str:
    """分类文件所属层级"""
    for layer, patterns in LAYER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, content) or re.search(pattern, file_path):
                return layer
    return 'other'


def detect_tech_stack(pom_content: str) -> list:
    """从 POM 文件检测技术栈"""
    techs = []
    for tech, pattern in TECH_PATTERNS.items():
        if re.search(pattern, pom_content, re.IGNORECASE):
            techs.append(tech)
    return techs


def detect_feign_dependencies(content: str) -> list:
    """检测 Feign 依赖（跨服务调用）"""
    feign_deps = re.findall(r'@FeignClient\s*\([^)]*name\s*=\s*"([^"]+)"', content)
    return feign_deps


def detect_anti_patterns(file_path: str, content: str) -> list:
    """检测架构反模式"""
    issues = []
    file_name = os.path.basename(file_path)

    # 检测反射复制
    if re.search(ANTI_PATTERNS['reflection_copy']['pattern'], content):
        issues.append({
            'type': 'REFLECTION_COPY',
            'severity': 'HIGH',
            'file': file_path,
            'message': f'{file_name}: 使用反射进行对象复制，应使用 MapStruct'
        })

    # 检测 System.out
    if re.search(ANTI_PATTERNS['system_out']['pattern'], content):
        issues.append({
            'type': 'SYSTEM_OUT',
            'severity': 'LOW',
            'file': file_path,
            'message': f'{file_name}: 使用 System.out.println，应使用 @Slf4j'
        })

    # 检测 Controller 层直接调用 Mapper
    if 'Controller' in file_name:
        if re.search(r'Mapper\s+\w+|@Resource.*Mapper|@Autowired.*Mapper', content):
            issues.append({
                'type': 'CROSS_LAYER_CALL',
                'severity': 'HIGH',
                'file': file_path,
                'message': f'{file_name}: Controller 层直接注入 Mapper（跨层调用）'
            })

    # 检测 DoService 层含 if 逻辑
    if 'DoServiceImpl' in file_name or 'DoService' in file_name:
        if_count = len(re.findall(r'\bif\s*\(', content))
        if if_count > 0:
            issues.append({
                'type': 'SERVICE_HAS_LOGIC',
                'severity': 'MEDIUM',
                'file': file_path,
                'message': f'{file_name}: DO Service 包含 {if_count} 个 if 语句，业务逻辑应在 Business 层'
            })

    return issues


def analyze_service(service_path: str) -> ServiceInfo:
    """分析单个服务"""
    service_name = os.path.basename(service_path)
    info = ServiceInfo(name=service_name, path=service_path)

    # 扫描子模块
    for item in os.listdir(service_path):
        item_path = os.path.join(service_path, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            info.modules.append(item)

    # 扫描 Java 文件
    java_files = scan_java_files(service_path)
    for file_path in java_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, IOError):
            continue

        layer = classify_file(file_path, content)
        file_name = os.path.basename(file_path)

        if layer == 'controller':
            info.controllers.append(file_name)
        elif layer == 'service':
            info.services.append(file_name)
        elif layer == 'mapper':
            info.mappers.append(file_name)
        elif layer == 'entity':
            info.entities.append(file_name)
        elif layer == 'feign':
            info.feign_clients.append(file_name)

        # 检测 Feign 依赖
        feign_deps = detect_feign_dependencies(content)
        info.dependencies.extend(feign_deps)

    info.dependencies = list(set(info.dependencies))

    # 分析技术栈
    pom_files = scan_pom_files(service_path)
    for pom_path in pom_files:
        try:
            with open(pom_path, 'r', encoding='utf-8') as f:
                pom_content = f.read()
            info.tech_stack.extend(detect_tech_stack(pom_content))
        except (UnicodeDecodeError, IOError):
            continue
    info.tech_stack = list(set(info.tech_stack))

    return info


def analyze(path: str) -> ArchitectureAnalysis:
    """执行架构分析"""
    result = ArchitectureAnalysis(scan_path=path)

    # 判断是单服务还是多服务
    if os.path.exists(os.path.join(path, 'pom.xml')):
        # 单服务分析
        info = analyze_service(path)
        result.services.append(info)
    else:
        # 多服务目录
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'pom.xml')):
                info = analyze_service(item_path)
                result.services.append(info)

    # 检测架构问题
    all_java_files = scan_java_files(path)
    for file_path in all_java_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            result.issues.extend(detect_anti_patterns(file_path, content))
        except (UnicodeDecodeError, IOError):
            continue

    # 汇总技术栈
    tech_count = defaultdict(int)
    for svc in result.services:
        for tech in svc.tech_stack:
            tech_count[tech] += 1
    result.tech_stack_summary = dict(tech_count)

    # 构建依赖图
    for svc in result.services:
        if svc.dependencies:
            result.dependency_graph[svc.name] = svc.dependencies

    # 计算度量
    result.metrics = {
        'total_services': len(result.services),
        'total_controllers': sum(len(s.controllers) for s in result.services),
        'total_services_classes': sum(len(s.services) for s in result.services),
        'total_mappers': sum(len(s.mappers) for s in result.services),
        'total_entities': sum(len(s.entities) for s in result.services),
        'total_issues': len(result.issues),
        'high_issues': len([i for i in result.issues if i['severity'] == 'HIGH']),
        'medium_issues': len([i for i in result.issues if i['severity'] == 'MEDIUM']),
        'low_issues': len([i for i in result.issues if i['severity'] == 'LOW']),
    }

    return result


def format_markdown(result: ArchitectureAnalysis) -> str:
    """输出 Markdown 格式报告"""
    lines = [
        "# 架构分析报告",
        "",
        f"**扫描路径**: `{result.scan_path}`",
        f"**分析时间**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 1. 概览",
        "",
        "| 度量 | 数量 |",
        "|------|------|",
        f"| 服务数 | {result.metrics.get('total_services', 0)} |",
        f"| Controller 数 | {result.metrics.get('total_controllers', 0)} |",
        f"| Service 数 | {result.metrics.get('total_services_classes', 0)} |",
        f"| Mapper 数 | {result.metrics.get('total_mappers', 0)} |",
        f"| Entity 数 | {result.metrics.get('total_entities', 0)} |",
        f"| 问题数 | {result.metrics.get('total_issues', 0)} (高:{result.metrics.get('high_issues', 0)} 中:{result.metrics.get('medium_issues', 0)} 低:{result.metrics.get('low_issues', 0)}) |",
        "",
    ]

    # 技术栈
    if result.tech_stack_summary:
        lines += ["## 2. 技术栈", "", "| 技术 | 使用服务数 |", "|------|----------|"]
        for tech, count in sorted(result.tech_stack_summary.items(), key=lambda x: -x[1]):
            lines.append(f"| {tech} | {count} |")
        lines.append("")

    # 服务列表
    lines += ["## 3. 服务清单", ""]
    for svc in result.services:
        lines.append(f"### {svc.name}")
        lines.append(f"- **模块**: {', '.join(svc.modules) if svc.modules else '无'}")
        lines.append(f"- **Controller**: {len(svc.controllers)} 个")
        lines.append(f"- **Service**: {len(svc.services)} 个")
        lines.append(f"- **Mapper**: {len(svc.mappers)} 个")
        lines.append(f"- **Entity**: {len(svc.entities)} 个")
        lines.append(f"- **Feign 依赖**: {', '.join(svc.dependencies) if svc.dependencies else '无'}")
        lines.append("")

    # 依赖关系
    if result.dependency_graph:
        lines += ["## 4. 服务依赖关系", "", "```mermaid", "graph LR"]
        for svc, deps in result.dependency_graph.items():
            for dep in deps:
                lines.append(f"    {svc} --> {dep}")
        lines += ["```", ""]

    # 问题列表
    if result.issues:
        lines += ["## 5. 架构问题", "",
                   "| 严重程度 | 类型 | 文件 | 说明 |",
                   "|---------|------|------|------|"]
        for issue in sorted(result.issues, key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['severity']]):
            severity_icon = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[issue['severity']]
            lines.append(f"| {severity_icon} {issue['severity']} | {issue['type']} | `{os.path.basename(issue['file'])}` | {issue['message']} |")
        lines.append("")

    return "\n".join(lines)


def format_json(result: ArchitectureAnalysis) -> str:
    """输出 JSON 格式"""
    data = {
        'scan_path': result.scan_path,
        'metrics': result.metrics,
        'tech_stack': result.tech_stack_summary,
        'services': [asdict(s) for s in result.services],
        'dependency_graph': result.dependency_graph,
        'issues': result.issues,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='TOGAF 架构分析脚本')
    parser.add_argument('path', help='要分析的代码路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='输出格式')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    print(f"正在分析: {args.path} ...")
    result = analyze(args.path)

    output = format_markdown(result) if args.format == 'md' else format_json(result)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"分析报告已输出到: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
