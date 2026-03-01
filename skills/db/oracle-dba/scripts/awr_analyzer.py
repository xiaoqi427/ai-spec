#!/usr/bin/env python3
"""
AWR报告自动分析工具
功能: 解析AWR报告HTML文件，提取关键性能指标并生成分析建议
作者: sevenxiao
日期: 2025-02-28

使用方法:
    python awr_analyzer.py awr_report.html
    python awr_analyzer.py awr_report.html --output analysis.txt
"""

import re
import sys
import argparse
from html.parser import HTMLParser
from typing import Dict, List, Tuple


class AWRParser(HTMLParser):
    """AWR报告HTML解析器"""
    
    def __init__(self):
        super().__init__()
        self.current_section = None
        self.data = {
            'db_info': {},
            'load_profile': {},
            'top_events': [],
            'top_sql': [],
            'instance_efficiency': {},
            'time_model': {}
        }
        self.current_table = []
        self.current_row = []
        self.in_table = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
            self.current_table = []
            
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            self._process_table()
            
    def handle_data(self, data):
        data = data.strip()
        if data and self.in_table:
            self.current_row.append(data)
            
    def _process_table(self):
        """处理表格数据"""
        # 这里简化处理，实际需要根据AWR报告的具体格式解析
        pass


def extract_metrics_from_text(awr_text: str) -> Dict:
    """
    从AWR报告文本中提取关键指标
    """
    metrics = {
        'db_time': 0,
        'db_cpu': 0,
        'load_profile': {},
        'top_events': [],
        'top_sql': [],
        'instance_efficiency': {}
    }
    
    # 提取DB Time
    db_time_match = re.search(r'DB Time[:\s]+([0-9,]+\.?\d*)', awr_text)
    if db_time_match:
        metrics['db_time'] = float(db_time_match.group(1).replace(',', ''))
    
    # 提取DB CPU
    db_cpu_match = re.search(r'DB CPU[:\s]+([0-9,]+\.?\d*)', awr_text)
    if db_cpu_match:
        metrics['db_cpu'] = float(db_cpu_match.group(1).replace(',', ''))
        
    return metrics


def analyze_load_profile(metrics: Dict) -> List[str]:
    """
    分析负载概况
    """
    issues = []
    
    if 'db_time' in metrics and 'db_cpu' in metrics:
        db_time = metrics['db_time']
        db_cpu = metrics['db_cpu']
        
        if db_cpu > 0:
            cpu_ratio = (db_cpu / db_time) * 100 if db_time > 0 else 0
            
            if cpu_ratio < 50:
                issues.append(
                    f"⚠️ CPU使用率偏低 ({cpu_ratio:.1f}%), "
                    "大量时间在等待事件上，需要分析Top等待事件"
                )
            elif cpu_ratio > 90:
                issues.append(
                    f"✅ CPU密集型负载 ({cpu_ratio:.1f}%), "
                    "主要优化方向是SQL执行效率"
                )
    
    return issues


def analyze_top_events(events: List[Dict]) -> List[str]:
    """
    分析Top等待事件
    """
    issues = []
    
    critical_events = {
        'db file sequential read': '单块读等待，通常是索引扫描，可能缺索引或索引选择性差',
        'db file scattered read': '多块读等待，通常是全表扫描，考虑添加索引',
        'direct path read': '直接路径读，可能是大表扫描或并行查询',
        'enq: TX - row lock contention': '行锁争用，检查是否有长事务或热点数据',
        'log file sync': '日志同步等待，可能是commit频繁或日志I/O慢',
        'log file parallel write': '日志并行写等待，检查LGWR进程和存储性能',
        'latch: cache buffers chains': 'Buffer cache竞争，可能是热点块',
        'library cache lock': '库缓存锁，可能是DDL或硬解析问题',
    }
    
    for event in events:
        event_name = event.get('name', '').lower()
        for critical_event, suggestion in critical_events.items():
            if critical_event in event_name:
                wait_time_pct = event.get('wait_time_pct', 0)
                issues.append(
                    f"⚠️ {event['name']}: {wait_time_pct:.1f}% - {suggestion}"
                )
    
    return issues


def analyze_top_sql(sql_list: List[Dict]) -> List[str]:
    """
    分析Top SQL
    """
    issues = []
    
    for sql in sql_list[:10]:  # 分析前10条SQL
        sql_id = sql.get('sql_id', 'Unknown')
        
        # 检查逻辑读
        buffer_gets = sql.get('buffer_gets', 0)
        executions = sql.get('executions', 1)
        gets_per_exec = buffer_gets / executions if executions > 0 else 0
        
        if gets_per_exec > 100000:
            issues.append(
                f"🔍 SQL_ID: {sql_id} - "
                f"单次执行逻辑读过高 ({gets_per_exec:,.0f}), 检查是否全表扫描"
            )
        
        # 检查物理读比例
        disk_reads = sql.get('disk_reads', 0)
        if buffer_gets > 0:
            physical_read_pct = (disk_reads / buffer_gets) * 100
            if physical_read_pct > 10:
                issues.append(
                    f"💾 SQL_ID: {sql_id} - "
                    f"物理读比例过高 ({physical_read_pct:.1f}%), 考虑增加buffer cache"
                )
    
    return issues


def generate_report(metrics: Dict) -> str:
    """
    生成分析报告
    """
    report = []
    report.append("=" * 80)
    report.append("                    AWR报告自动分析结果")
    report.append("=" * 80)
    report.append("")
    
    # 负载分析
    report.append(">>> 1. 负载概况分析")
    report.append("")
    load_issues = analyze_load_profile(metrics)
    if load_issues:
        report.extend(load_issues)
    else:
        report.append("✅ 负载概况正常")
    report.append("")
    
    # 等待事件分析
    report.append(">>> 2. 等待事件分析")
    report.append("")
    if metrics.get('top_events'):
        event_issues = analyze_top_events(metrics['top_events'])
        if event_issues:
            report.extend(event_issues)
        else:
            report.append("✅ 未发现严重等待事件")
    else:
        report.append("⚠️ 无等待事件数据")
    report.append("")
    
    # SQL分析
    report.append(">>> 3. Top SQL分析")
    report.append("")
    if metrics.get('top_sql'):
        sql_issues = analyze_top_sql(metrics['top_sql'])
        if sql_issues:
            report.extend(sql_issues)
        else:
            report.append("✅ Top SQL未发现明显问题")
    else:
        report.append("⚠️ 无SQL数据")
    report.append("")
    
    # 优化建议
    report.append(">>> 4. 总体优化建议")
    report.append("")
    report.append("1. 检查并优化Top SQL的执行计划")
    report.append("2. 关注Top等待事件，针对性优化")
    report.append("3. 定期收集统计信息，保持准确性")
    report.append("4. 监控表空间增长，及时扩容")
    report.append("5. 评估是否需要调整系统参数（buffer cache、shared pool等）")
    report.append("")
    
    report.append("=" * 80)
    report.append("                         分析完成")
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='AWR报告自动分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    %(prog)s awr_report.html
    %(prog)s awr_report.html --output analysis.txt
        """
    )
    
    parser.add_argument('awr_file', help='AWR报告HTML文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（可选，默认输出到控制台）')
    
    args = parser.parse_args()
    
    try:
        # 读取AWR报告
        with open(args.awr_file, 'r', encoding='utf-8') as f:
            awr_content = f.read()
        
        # 解析指标
        metrics = extract_metrics_from_text(awr_content)
        
        # 生成报告
        report = generate_report(metrics)
        
        # 输出报告
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 分析报告已保存到: {args.output}")
        else:
            print(report)
            
    except FileNotFoundError:
        print(f"❌ 错误: 文件不存在 - {args.awr_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
