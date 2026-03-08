#!/usr/bin/env python3
"""
DDD 模型验证脚本
验证领域模型的一致性和规范性，检查常见的 DDD 反模式。

用法:
    python validate-model.py <代码路径> [--strict] [--output <报告文件>]

示例:
    python validate-model.py ./fssc-claim-service
    python validate-model.py ./src --strict --output validation-report.md
"""

import os
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationIssue:
    """验证问题"""
    rule: str
    severity: str  # ERROR / WARNING / INFO
    file: str
    line: int
    message: str
    suggestion: str = ""


@dataclass
class ValidationReport:
    """验证报告"""
    scan_path: str
    total_files: int = 0
    issues: list = field(default_factory=list)
    passed_rules: list = field(default_factory=list)

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == 'ERROR']

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == 'WARNING']

    @property
    def infos(self):
        return [i for i in self.issues if i.severity == 'INFO']


class DddValidator:
    """DDD 模型验证器"""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.report = None

    def validate(self, path: str) -> ValidationReport:
        """执行完整验证"""
        self.report = ValidationReport(scan_path=path)
        java_files = self._scan_files(path)
        self.report.total_files = len(java_files)

        for file_path in java_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
            except (UnicodeDecodeError, IOError):
                continue

            self._check_layer_violations(file_path, content, lines)
            self._check_anemic_model(file_path, content, lines)
            self._check_aggregate_rules(file_path, content, lines)
            self._check_value_object_rules(file_path, content, lines)
            self._check_service_rules(file_path, content, lines)
            self._check_repository_rules(file_path, content, lines)
            self._check_naming_conventions(file_path, content, lines)
            self._check_dependency_direction(file_path, content, lines)

        return self.report

    def _scan_files(self, path: str) -> list:
        """扫描 Java 文件"""
        java_files = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ('test', 'target', 'build', '.git')]
            for f in files:
                if f.endswith('.java'):
                    java_files.append(os.path.join(root, f))
        return java_files

    def _add_issue(self, rule, severity, file, line, message, suggestion=""):
        self.report.issues.append(ValidationIssue(
            rule=rule, severity=severity, file=file,
            line=line, message=message, suggestion=suggestion
        ))

    # ========== 验证规则 ==========

    def _check_layer_violations(self, file_path, content, lines):
        """检查分层违规"""
        pkg = self._get_package(content)

        # Controller 层不应直接引用 Mapper
        if 'controller' in pkg.lower():
            for i, line in enumerate(lines, 1):
                if re.search(r'import\s+.*Mapper;', line):
                    self._add_issue(
                        'LAYER_VIOLATION', 'ERROR', file_path, i,
                        'Controller 层直接引用了 Mapper，违反分层架构',
                        '应通过 Service/Business 层间接访问数据层'
                    )
                if re.search(r'import\s+.*Repository;', line) and 'domain' not in pkg:
                    self._add_issue(
                        'LAYER_VIOLATION', 'WARNING', file_path, i,
                        'Controller 层直接引用了 Repository',
                        '应通过应用服务层访问'
                    )

        # Mapper/Repository 层不应引用 Controller
        if 'mapper' in pkg.lower() or 'repository' in pkg.lower():
            for i, line in enumerate(lines, 1):
                if re.search(r'import\s+.*[Cc]ontroller;', line):
                    self._add_issue(
                        'REVERSE_DEPENDENCY', 'ERROR', file_path, i,
                        'Mapper/Repository 层引用了 Controller，存在反向依赖',
                        '数据访问层不应依赖上层'
                    )

    def _check_anemic_model(self, file_path, content, lines):
        """检查贫血模型"""
        # 仅检查标注为 Entity 或文件名含 Do/Entity 的类
        class_match = re.search(r'class\s+(\w+)', content)
        if not class_match:
            return

        class_name = class_match.group(1)
        is_entity = (
            '@Entity' in content or
            '@TableName' in content or
            class_name.endswith('Do') or
            class_name.endswith('Entity')
        )

        if not is_entity:
            return

        # 统计字段和非 getter/setter 方法
        field_count = len(re.findall(r'private\s+\w+\s+\w+\s*;', content))
        all_methods = re.findall(r'public\s+\w+\s+(\w+)\s*\(', content)
        business_methods = [m for m in all_methods
                           if not m.startswith(('get', 'set', 'is', 'has', 'toString', 'hashCode', 'equals'))]

        if field_count > 5 and len(business_methods) == 0:
            line_no = content[:content.find(f'class {class_name}')].count('\n') + 1
            self._add_issue(
                'ANEMIC_MODEL', 'WARNING', file_path, line_no,
                f'{class_name} 有 {field_count} 个字段但没有业务方法，疑似贫血模型',
                '考虑将相关业务逻辑移入实体中，使其成为充血模型'
            )

    def _check_aggregate_rules(self, file_path, content, lines):
        """检查聚合规则"""
        if 'AggregateRoot' not in content and not re.search(r'聚合根', content):
            return

        class_name = self._get_class_name(content)

        # 检查聚合根是否有过多关联
        object_refs = re.findall(r'private\s+(?:List<)?(\w+)(?:>)?\s+\w+;', content)
        entity_refs = [r for r in object_refs if r[0].isupper() and r not in
                       ('String', 'Integer', 'Long', 'BigDecimal', 'LocalDateTime',
                        'Boolean', 'Double', 'Float', 'Date', 'Map', 'Set', 'List')]
        if len(entity_refs) > 5:
            self._add_issue(
                'LARGE_AGGREGATE', 'WARNING', file_path, 1,
                f'聚合根 {class_name} 引用了 {len(entity_refs)} 个实体类型，聚合可能过大',
                '考虑拆分为更小的聚合，使用 ID 引用而非对象引用'
            )

    def _check_value_object_rules(self, file_path, content, lines):
        """检查值对象规则"""
        if 'record ' not in content:
            return

        class_name = self._get_class_name(content)

        # record 类不应有 setter 方法
        if re.search(r'void\s+set\w+\(', content):
            self._add_issue(
                'MUTABLE_VALUE_OBJECT', 'ERROR', file_path, 1,
                f'值对象 {class_name} 包含 setter 方法，违反不可变原则',
                '值对象应为不可变，移除 setter 方法'
            )

    def _check_service_rules(self, file_path, content, lines):
        """检查服务层规则"""
        pkg = self._get_package(content)
        class_name = self._get_class_name(content)

        # DoService 层不应包含 if 逻辑（项目规则）
        if 'facade' in pkg.lower() or ('DoService' in class_name):
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('if ') or stripped.startswith('if('):
                    if self.strict:
                        self._add_issue(
                            'LOGIC_IN_DO_SERVICE', 'ERROR', file_path, i,
                            f'DO Service {class_name} 中包含 if 逻辑',
                            '将业务逻辑移到 Business 层'
                        )

    def _check_repository_rules(self, file_path, content, lines):
        """检查仓储规则"""
        if 'Repository' not in self._get_class_name(content):
            return

        # 仓储不应包含业务逻辑
        for i, line in enumerate(lines, 1):
            if re.search(r'throw\s+new\s+\w*Business\w*Exception', line):
                self._add_issue(
                    'BUSINESS_LOGIC_IN_REPO', 'WARNING', file_path, i,
                    '仓储中抛出了业务异常',
                    '仓储只负责数据访问，业务异常应在服务层处理'
                )

    def _check_naming_conventions(self, file_path, content, lines):
        """检查命名规范"""
        class_name = self._get_class_name(content)
        if not class_name:
            return

        # 检查接口命名
        is_interface = re.search(r'interface\s+' + class_name, content) is not None
        if is_interface:
            if class_name.startswith('I') and class_name[1].isupper():
                pass  # I 开头的接口命名，符合项目规范
            elif class_name.endswith('Service') and not class_name.startswith('I'):
                self._add_issue(
                    'NAMING_CONVENTION', 'INFO', file_path, 1,
                    f'Service 接口 {class_name} 建议以 I 开头',
                    f'建议重命名为 I{class_name}'
                )

    def _check_dependency_direction(self, file_path, content, lines):
        """检查依赖方向"""
        pkg = self._get_package(content)

        # 领域层不应依赖框架
        if 'domain' in pkg.lower():
            framework_imports = []
            for i, line in enumerate(lines, 1):
                if re.search(r'import\s+org\.springframework', line):
                    framework_imports.append((i, line.strip()))
                if re.search(r'import\s+com\.baomidou', line):
                    framework_imports.append((i, line.strip()))

            for line_no, import_line in framework_imports:
                # 允许少量注解
                if '@Transactional' not in import_line and '@Service' not in import_line:
                    if self.strict:
                        self._add_issue(
                            'DOMAIN_FRAMEWORK_DEPENDENCY', 'WARNING', file_path, line_no,
                            f'领域层引用了框架: {import_line}',
                            '领域层应保持纯净，不依赖外部框架'
                        )

    # ========== 辅助方法 ==========

    def _get_package(self, content: str) -> str:
        match = re.search(r'^package\s+([\w.]+);', content, re.MULTILINE)
        return match.group(1) if match else ""

    def _get_class_name(self, content: str) -> str:
        match = re.search(r'(?:class|interface|enum|record)\s+(\w+)', content)
        return match.group(1) if match else ""


def format_report(report: ValidationReport) -> str:
    """格式化验证报告"""
    lines = [
        "# DDD 模型验证报告",
        "",
        f"**扫描路径**: `{report.scan_path}`",
        f"**扫描文件数**: {report.total_files}",
        "",
        "## 验证结果概览",
        "",
        f"| 级别 | 数量 |",
        f"|------|------|",
        f"| ERROR | {len(report.errors)} |",
        f"| WARNING | {len(report.warnings)} |",
        f"| INFO | {len(report.infos)} |",
        "",
    ]

    if report.errors:
        lines += ["## 错误 (必须修复)", ""]
        for issue in report.errors:
            lines += [
                f"### [{issue.rule}] {issue.message}",
                f"- **文件**: `{issue.file}` (行 {issue.line})",
                f"- **建议**: {issue.suggestion}",
                "",
            ]

    if report.warnings:
        lines += ["## 警告 (建议修复)", ""]
        for issue in report.warnings:
            lines += [
                f"### [{issue.rule}] {issue.message}",
                f"- **文件**: `{issue.file}` (行 {issue.line})",
                f"- **建议**: {issue.suggestion}",
                "",
            ]

    if report.infos:
        lines += ["## 提示 (可选优化)", ""]
        for issue in report.infos:
            lines.append(f"- [{issue.rule}] {issue.message} (`{os.path.basename(issue.file)}`)")
        lines.append("")

    if not report.issues:
        lines += ["## 恭喜！", "", "未发现任何问题，模型设计符合 DDD 规范。", ""]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='DDD 模型验证脚本')
    parser.add_argument('path', help='要验证的代码路径')
    parser.add_argument('--strict', action='store_true', help='启用严格模式')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    print(f"正在验证: {args.path} {'(严格模式)' if args.strict else ''} ...")
    validator = DddValidator(strict=args.strict)
    report = validator.validate(args.path)

    output = format_report(report)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"验证报告已输出到: {args.output}")
    else:
        print(output)

    # 返回码: 有 ERROR 时返回非零
    sys.exit(1 if report.errors else 0)


if __name__ == '__main__':
    main()
