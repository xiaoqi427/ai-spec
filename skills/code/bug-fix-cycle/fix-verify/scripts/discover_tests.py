#!/usr/bin/env python3
"""
测试发现脚本 - 根据修改的 Java 文件，自动发现对应的单元测试类。

匹配策略（按优先级）:
1. 精确类名匹配: XxxServiceImpl.java → XxxServiceImplTest.java
2. 包路径映射: src/main/java → src/test/java + Test 后缀
3. 同包递归查找: 同 test 包下所有 *Test.java
4. 模块内扫描: 同模块 src/test/ 下所有 *Test.java

用法:
  python3 discover_tests.py --files "File1.java,File2.java" --project-root <path>
  python3 discover_tests.py --files "File1.java" --project-root <path> --output json

@author: sevenxiao
"""

import argparse
import json
import os
import sys
from pathlib import Path


def find_file_in_project(filename: str, project_root: str) -> list[str]:
    """在项目中查找指定文件名的所有路径"""
    results = []
    for root, dirs, files in os.walk(project_root):
        # 跳过 target、.git、.idea 等目录
        dirs[:] = [d for d in dirs if d not in ('target', '.git', '.idea', 'node_modules', '.qoder')]
        if filename in files:
            results.append(os.path.join(root, filename))
    return results


def extract_module_path(file_path: str, project_root: str) -> str:
    """从文件路径中提取 Maven 模块路径

    例如:
    claim-otc/claim-otc-service/src/main/java/... → claim-otc/claim-otc-service
    """
    rel = os.path.relpath(file_path, project_root)
    parts = rel.split(os.sep)
    # 查找 src 目录的位置
    for i, part in enumerate(parts):
        if part == 'src':
            return os.sep.join(parts[:i])
    return ''


def strategy_exact_match(source_path: str, project_root: str) -> list[dict]:
    """策略1: 精确类名匹配

    XxxServiceImpl.java → XxxServiceImplTest.java
    Xxx.java → XxxTest.java
    """
    results = []
    source_name = Path(source_path).stem  # 不含扩展名
    test_name = f"{source_name}Test.java"

    # 查找测试文件
    found = find_file_in_project(test_name, project_root)
    for test_path in found:
        # 确保是 test 目录下的
        if 'src/test' in test_path or 'src' + os.sep + 'test' in test_path:
            results.append({
                'test_class': f"{source_name}Test",
                'test_path': os.path.relpath(test_path, project_root),
                'module': extract_module_path(test_path, project_root),
                'match_strategy': 'exact',
                'source_file': Path(source_path).name
            })
    return results


def strategy_path_mapping(source_path: str, project_root: str) -> list[dict]:
    """策略2: 包路径映射

    src/main/java/com/yili/.../Xxx.java → src/test/java/com/yili/.../XxxTest.java
    """
    results = []
    rel_path = os.path.relpath(source_path, project_root)

    # 替换 src/main/java → src/test/java
    test_rel = rel_path.replace(
        f'src{os.sep}main{os.sep}java',
        f'src{os.sep}test{os.sep}java'
    )

    if test_rel == rel_path:
        return results  # 没有匹配到 main/java 路径

    # 类名加 Test 后缀
    stem = Path(test_rel).stem
    test_rel = str(Path(test_rel).parent / f"{stem}Test.java")

    test_full = os.path.join(project_root, test_rel)
    if os.path.exists(test_full):
        results.append({
            'test_class': f"{stem}Test",
            'test_path': test_rel,
            'module': extract_module_path(test_full, project_root),
            'match_strategy': 'path_mapping',
            'source_file': Path(source_path).name
        })
    return results


def strategy_package_scan(source_path: str, project_root: str) -> list[dict]:
    """策略3: 同包递归查找

    找到源文件对应的 test 包目录，递归查找所有 *Test.java
    """
    results = []
    rel_path = os.path.relpath(source_path, project_root)

    # 计算 test 包路径
    test_pkg_path = rel_path.replace(
        f'src{os.sep}main{os.sep}java',
        f'src{os.sep}test{os.sep}java'
    )
    if test_pkg_path == rel_path:
        return results

    test_pkg_dir = os.path.join(project_root, str(Path(test_pkg_path).parent))

    if not os.path.isdir(test_pkg_dir):
        # 尝试向上找一级目录
        test_pkg_dir = os.path.join(project_root, str(Path(test_pkg_path).parent.parent))
        if not os.path.isdir(test_pkg_dir):
            return results

    # 递归查找 *Test.java
    already_found = set()
    for root, dirs, files in os.walk(test_pkg_dir):
        for f in files:
            if f.endswith('Test.java') and not f.startswith('.'):
                test_path = os.path.join(root, f)
                rel_test = os.path.relpath(test_path, project_root)
                if rel_test not in already_found:
                    already_found.add(rel_test)
                    results.append({
                        'test_class': Path(f).stem,
                        'test_path': rel_test,
                        'module': extract_module_path(test_path, project_root),
                        'match_strategy': 'package_scan',
                        'source_file': Path(source_path).name
                    })
    return results


def strategy_module_scan(source_path: str, project_root: str) -> list[dict]:
    """策略4: 模块内全量扫描

    扫描同模块 src/test/ 下所有 *Test.java（兜底方案）
    """
    results = []
    module = extract_module_path(source_path, project_root)
    if not module:
        return results

    test_dir = os.path.join(project_root, module, 'src', 'test')
    if not os.path.isdir(test_dir):
        return results

    already_found = set()
    for root, dirs, files in os.walk(test_dir):
        dirs[:] = [d for d in dirs if d not in ('target', '.git')]
        for f in files:
            if f.endswith('Test.java') and not f.startswith('.'):
                test_path = os.path.join(root, f)
                rel_test = os.path.relpath(test_path, project_root)
                if rel_test not in already_found:
                    already_found.add(rel_test)
                    results.append({
                        'test_class': Path(f).stem,
                        'test_path': rel_test,
                        'module': extract_module_path(test_path, project_root),
                        'match_strategy': 'module_scan',
                        'source_file': Path(source_path).name
                    })
    return results


def discover_tests(files: list[str], project_root: str) -> dict:
    """发现修改文件对应的测试类

    按策略优先级依次匹配，精确匹配优先。
    """
    all_discovered = []
    all_missing = []
    discovered_paths = set()

    for file_input in files:
        file_input = file_input.strip()
        if not file_input:
            continue

        # 如果是完整路径，直接使用；否则在项目中搜索
        if os.path.isabs(file_input) or os.path.exists(os.path.join(project_root, file_input)):
            source_paths = [os.path.join(project_root, file_input) if not os.path.isabs(file_input) else file_input]
        else:
            # 按文件名搜索
            source_paths = find_file_in_project(file_input, project_root)

        if not source_paths:
            all_missing.append({
                'source_file': file_input,
                'source_path': 'NOT_FOUND',
                'suggested_test_path': ''
            })
            continue

        for source_path in source_paths:
            # 跳过非 main/java 的文件
            if 'src/main/java' not in source_path and f'src{os.sep}main{os.sep}java' not in source_path:
                continue
            # 跳过测试文件本身
            if 'src/test' in source_path or f'src{os.sep}test' in source_path:
                continue

            found = False
            # 按优先级执行策略
            for strategy in [strategy_exact_match, strategy_path_mapping, strategy_package_scan]:
                matches = strategy(source_path, project_root)
                for m in matches:
                    if m['test_path'] not in discovered_paths:
                        discovered_paths.add(m['test_path'])
                        all_discovered.append(m)
                        found = True

                if found:
                    break  # 精确匹配成功就不再用低优先级策略

            if not found:
                # 没有找到测试
                rel_source = os.path.relpath(source_path, project_root)
                suggested = rel_source.replace(
                    f'src{os.sep}main{os.sep}java',
                    f'src{os.sep}test{os.sep}java'
                )
                stem = Path(suggested).stem
                suggested = str(Path(suggested).parent / f"{stem}Test.java")
                all_missing.append({
                    'source_file': Path(source_path).name,
                    'source_path': rel_source,
                    'suggested_test_path': suggested
                })

    # 汇总
    total_modified = len(files)
    tests_found = len(all_discovered)
    tests_missing = len(all_missing)
    coverage = f"{int(tests_found / max(total_modified, 1) * 100)}%"

    return {
        'modified_files': files,
        'discovered_tests': all_discovered,
        'missing_tests': all_missing,
        'summary': {
            'total_modified': total_modified,
            'tests_found': tests_found,
            'tests_missing': tests_missing,
            'coverage_ratio': coverage
        }
    }


def main():
    parser = argparse.ArgumentParser(description='发现修改文件对应的单元测试类')
    parser.add_argument('--files', required=True,
                        help='逗号分隔的修改文件列表（文件名或相对路径）')
    parser.add_argument('--project-root', required=True,
                        help='项目根目录（如 fssc-claim-service）')
    parser.add_argument('--output', choices=['json', 'table'], default='table',
                        help='输出格式: json 或 table（默认 table）')

    args = parser.parse_args()

    files = [f.strip() for f in args.files.split(',') if f.strip()]
    project_root = os.path.abspath(args.project_root)

    if not os.path.isdir(project_root):
        print(f"错误: 项目目录不存在: {project_root}", file=sys.stderr)
        sys.exit(1)

    result = discover_tests(files, project_root)

    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 表格输出
        summary = result['summary']
        print(f"\n=== 测试发现报告 ===")
        print(f"修改文件: {summary['total_modified']} 个")
        print(f"发现测试: {summary['tests_found']} 个")
        print(f"缺失测试: {summary['tests_missing']} 个")
        print(f"覆盖率:   {summary['coverage_ratio']}")

        if result['discovered_tests']:
            print(f"\n--- 发现的测试类 ---")
            for t in result['discovered_tests']:
                print(f"  [{t['match_strategy']}] {t['test_class']}")
                print(f"    路径: {t['test_path']}")
                print(f"    模块: {t['module']}")
                print(f"    源自: {t['source_file']}")

        if result['missing_tests']:
            print(f"\n--- 缺失测试的文件 ---")
            for m in result['missing_tests']:
                print(f"  {m['source_file']}")
                print(f"    源路径: {m['source_path']}")
                print(f"    建议创建: {m['suggested_test_path']}")

        # 生成 Maven 命令
        if result['discovered_tests']:
            modules = set()
            test_classes = []
            for t in result['discovered_tests']:
                modules.add(t['module'])
                test_classes.append(t['test_class'])
            print(f"\n--- 建议的 Maven 命令 ---")
            for module in modules:
                module_tests = [t['test_class'] for t in result['discovered_tests'] if t['module'] == module]
                tests_str = ','.join(module_tests)
                print(f"mvn test -pl {module} -Dtest={tests_str} -DskipTests=false -Dmaven.test.skip=false -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository -T 1C")


if __name__ == '__main__':
    main()
