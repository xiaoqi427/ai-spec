#!/usr/bin/env python3
"""
上下文映射图生成脚本
从 Java 多模块项目中分析模块间依赖关系，自动生成限界上下文映射图（Mermaid 格式）。

用法:
    python gen-context-map.py <项目根路径> [--output <输出文件>] [--include-external]

示例:
    python gen-context-map.py ./
    python gen-context-map.py ./ --output context-map.md --include-external
"""

import os
import re
import sys
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BoundedContext:
    """限界上下文"""
    name: str
    module_path: str
    packages: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    feign_clients: list = field(default_factory=list)
    feign_providers: list = field(default_factory=list)
    mq_publishers: list = field(default_factory=list)
    mq_consumers: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)


@dataclass
class ContextRelation:
    """上下文关系"""
    upstream: str
    downstream: str
    relation_type: str  # CS (Customer-Supplier) / ACL / OHS / SK / PL
    communication: str  # REST / MQ / SharedDB
    details: str = ""


def discover_modules(root_path: str) -> list:
    """发现 Maven 多模块项目的模块"""
    modules = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        pom_path = os.path.join(item_path, 'pom.xml')
        if os.path.isdir(item_path) and os.path.exists(pom_path):
            # 提取模块名
            name = item
            # 去掉 fssc- 前缀和 -service 后缀
            clean_name = re.sub(r'^fssc-', '', name)
            clean_name = re.sub(r'-service$', '', clean_name)
            if clean_name and clean_name not in ('parent', 'web-framework'):
                modules.append({
                    'name': clean_name,
                    'display_name': clean_name.replace('-', ' ').title(),
                    'path': item_path,
                    'original_name': item,
                })
    return modules


def analyze_pom_dependencies(pom_path: str) -> list:
    """分析 POM 文件的模块间依赖"""
    deps = []
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

        for dep in root.findall('.//m:dependency', ns):
            artifact = dep.find('m:artifactId', ns)
            group = dep.find('m:groupId', ns)
            if artifact is not None and group is not None:
                artifact_id = artifact.text or ''
                group_id = group.text or ''
                if 'yili' in group_id or 'fssc' in artifact_id:
                    deps.append(artifact_id)
    except (ET.ParseError, FileNotFoundError):
        pass
    return deps


def scan_feign_clients(module_path: str) -> list:
    """扫描 Feign Client 调用"""
    feign_clients = []
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if d not in ('test', 'target', '.git')]
        for f in files:
            if f.endswith('.java'):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                    # 查找 @FeignClient 注解
                    matches = re.findall(r'@FeignClient\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']', content)
                    feign_clients.extend(matches)
                    # 查找 Feign 接口导入
                    imports = re.findall(r'import\s+com\.yili\.(\w+)\.api\.feign', content)
                    feign_clients.extend(imports)
                except (UnicodeDecodeError, IOError):
                    continue
    return list(set(feign_clients))


def scan_mq_usage(module_path: str) -> tuple:
    """扫描消息队列使用"""
    publishers = []
    consumers = []
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if d not in ('test', 'target', '.git')]
        for f in files:
            if f.endswith('.java'):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                    # RabbitMQ 发布
                    if re.search(r'RabbitTemplate|convertAndSend|publishEvent', content):
                        event_names = re.findall(r'new\s+(\w+Event)\(', content)
                        publishers.extend(event_names)
                    # RabbitMQ 消费
                    if re.search(r'@RabbitListener|@EventListener', content):
                        listener_events = re.findall(r'@RabbitListener.*queues?\s*=\s*["\']([^"\']+)', content)
                        consumers.extend(listener_events)
                        event_params = re.findall(r'public\s+void\s+\w+\((\w+Event)\s+', content)
                        consumers.extend(event_params)
                except (UnicodeDecodeError, IOError):
                    continue
    return list(set(publishers)), list(set(consumers))


def scan_entities(module_path: str) -> list:
    """扫描实体/DO 类"""
    entities = []
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if d not in ('test', 'target', '.git')]
        for f in files:
            if f.endswith('.java') and ('Do.java' in f or 'Entity.java' in f):
                entities.append(f.replace('.java', ''))
            elif f.endswith('.java'):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                    if '@TableName' in content or '@Entity' in content:
                        match = re.search(r'class\s+(\w+)', content)
                        if match:
                            entities.append(match.group(1))
                except (UnicodeDecodeError, IOError):
                    continue
    return list(set(entities))


def build_contexts(root_path: str) -> list:
    """构建限界上下文"""
    modules = discover_modules(root_path)
    contexts = []

    for mod in modules:
        ctx = BoundedContext(
            name=mod['display_name'],
            module_path=mod['path'],
        )

        # 分析 POM 依赖
        pom_files = []
        for r, d, f in os.walk(mod['path']):
            d[:] = [x for x in d if x not in ('target', '.git')]
            for file in f:
                if file == 'pom.xml':
                    pom_files.append(os.path.join(r, file))

        for pom in pom_files:
            ctx.dependencies.extend(analyze_pom_dependencies(pom))

        # 扫描 Feign Client
        ctx.feign_clients = scan_feign_clients(mod['path'])

        # 扫描 MQ 使用
        publishers, consumers = scan_mq_usage(mod['path'])
        ctx.mq_publishers = publishers
        ctx.mq_consumers = consumers

        # 扫描实体
        ctx.entities = scan_entities(mod['path'])

        contexts.append(ctx)

    return contexts


def infer_relations(contexts: list) -> list:
    """推断上下文间关系"""
    relations = []
    ctx_map = {c.name.lower().replace(' ', '-'): c for c in contexts}

    for ctx in contexts:
        # 基于 Feign Client 推断 Customer-Supplier 关系
        for feign in ctx.feign_clients:
            upstream_name = feign.replace('fssc-', '').replace('-service', '')
            upstream_name = upstream_name.replace('-', ' ').title()
            if upstream_name != ctx.name:
                relations.append(ContextRelation(
                    upstream=upstream_name,
                    downstream=ctx.name,
                    relation_type='C/S',
                    communication='REST (Feign)',
                    details=f'{ctx.name} 通过 Feign 调用 {upstream_name}'
                ))

        # 基于 POM 依赖推断关系
        for dep in ctx.dependencies:
            dep_name = dep.replace('fssc-', '').replace('-api', '').replace('-do', '')
            dep_name = dep_name.replace('-service', '').replace('-', ' ').title()
            if dep_name != ctx.name and dep_name not in ('Common', 'Parent'):
                # 避免重复
                existing = [r for r in relations
                            if r.upstream == dep_name and r.downstream == ctx.name]
                if not existing:
                    relations.append(ContextRelation(
                        upstream=dep_name,
                        downstream=ctx.name,
                        relation_type='Dependency',
                        communication='Maven',
                        details=f'{ctx.name} 依赖 {dep_name} 的 API/DO'
                    ))

    # 去重
    seen = set()
    unique_relations = []
    for r in relations:
        key = (r.upstream, r.downstream, r.relation_type)
        if key not in seen:
            seen.add(key)
            unique_relations.append(r)

    return unique_relations


def generate_mermaid(contexts: list, relations: list) -> str:
    """生成 Mermaid 图"""
    lines = ["```mermaid", "graph TB"]

    # 添加节点
    for ctx in contexts:
        node_id = ctx.name.replace(' ', '_')
        entity_count = len(ctx.entities)
        label = f"{ctx.name}"
        if entity_count > 0:
            label += f"<br/>({entity_count} entities)"
        lines.append(f"    {node_id}[{label}]")

    lines.append("")

    # 添加关系
    for rel in relations:
        from_id = rel.upstream.replace(' ', '_')
        to_id = rel.downstream.replace(' ', '_')
        # 确保节点存在
        ctx_names = [c.name for c in contexts]
        if rel.upstream in ctx_names and rel.downstream in ctx_names:
            label = rel.relation_type
            if rel.communication != 'Maven':
                label += f"<br/>{rel.communication}"
            lines.append(f"    {from_id} -->|{label}| {to_id}")

    lines.append("```")
    return "\n".join(lines)


def generate_report(contexts: list, relations: list) -> str:
    """生成完整报告"""
    lines = [
        "# 限界上下文映射图",
        "",
        "## 上下文映射",
        "",
        generate_mermaid(contexts, relations),
        "",
        "---",
        "",
        "## 上下文清单",
        "",
        "| 上下文 | 实体数 | Feign调用 | MQ发布 | MQ消费 |",
        "|--------|-------|-----------|--------|--------|",
    ]

    for ctx in contexts:
        lines.append(
            f"| {ctx.name} | {len(ctx.entities)} | "
            f"{len(ctx.feign_clients)} | {len(ctx.mq_publishers)} | "
            f"{len(ctx.mq_consumers)} |"
        )

    lines += [
        "",
        "## 关系清单",
        "",
        "| 上游 | 下游 | 关系模式 | 通信方式 | 说明 |",
        "|------|------|---------|---------|------|",
    ]

    for rel in relations:
        lines.append(
            f"| {rel.upstream} | {rel.downstream} | "
            f"{rel.relation_type} | {rel.communication} | {rel.details} |"
        )

    lines += [
        "",
        "## 各上下文实体",
        "",
    ]

    for ctx in contexts:
        if ctx.entities:
            lines.append(f"### {ctx.name}")
            lines.append("")
            for entity in sorted(ctx.entities):
                lines.append(f"- {entity}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='上下文映射图生成脚本')
    parser.add_argument('path', help='项目根路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--include-external', action='store_true', help='包含外部系统依赖')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    print(f"正在分析项目结构: {args.path} ...")

    contexts = build_contexts(args.path)
    print(f"发现 {len(contexts)} 个限界上下文")

    relations = infer_relations(contexts)
    print(f"推断出 {len(relations)} 个上下文关系")

    report = generate_report(contexts, relations)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"上下文映射图已输出到: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
