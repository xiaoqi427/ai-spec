"""流程编排模块：串联 Excel读取 → HTTP请求 → 结果写出"""
from __future__ import annotations

import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

from .config_loader import AppConfig
from .excel_io import read_test_inputs, write_test_results
from .http_client import HttpClient
from .login_handler import LoginHandler
from .models import TestInput, TestResult

logger = logging.getLogger(__name__)


class TestPipeline:
    """submitValidate 批量测试流程编排器"""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.http_client = HttpClient(
            server_config=config.server,
            auth_config=config.auth,
            retry_config=config.retry,
            url_template=config.url.template,
            routing_config=config.routing,
        )

    def _ensure_dirs(self) -> None:
        """确保输出和日志目录存在"""
        os.makedirs(self.config.output.output_dir, exist_ok=True)
        log_dir = os.path.dirname(self.config.log.log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

    def run(self) -> List[TestResult]:
        """执行完整的测试流程

        Returns:
            所有测试结果列表
        """
        self._ensure_dirs()
        cfg = self.config

        # 0. 登录流程（当 auth.type=login 时）
        if cfg.auth.type.lower() == "login" and cfg.login.enabled:
            login_handler = LoginHandler(
                login_config=cfg.login,
                server_config=cfg.server,
            )
            login_ok = login_handler.login_and_inject(self.http_client.session)
            if not login_ok:
                print("\n  登录失败，测试终止\n")
                logger.error("登录失败，测试终止")
                return []

        # 1. 读取测试输入
        logger.info(f"正在读取 Excel: {cfg.excel.input_path}")
        inputs = read_test_inputs(
            excel_path=cfg.excel.input_path,
            sheet_name=cfg.excel.sheet_name,
            claim_id_column=cfg.excel.columns.claim_id,
            item_id_column=cfg.excel.columns.item_id,
        )

        if not inputs:
            logger.warning("未读取到测试数据，流程结束")
            return []

        logger.info(f"读取到 {len(inputs)} 条测试数据，开始执行...")
        print(f"\n{'='*60}")
        print(f"  submitValidate 批量测试")
        print(f"  目标服务器: {cfg.server.base_url}")
        print(f"  测试数据: {len(inputs)} 条")
        print(f"  并发模式: {'开启 (max_workers={})'.format(cfg.concurrency.max_workers) if cfg.concurrency.enabled else '关闭（顺序执行）'}")
        print(f"{'='*60}\n")

        # 2. 执行测试
        start_time = time.time()
        if cfg.concurrency.enabled:
            results = self._run_concurrent(inputs)
        else:
            results = self._run_sequential(inputs)
        elapsed = time.time() - start_time

        # 3. 写出结果
        output_path = write_test_results(
            results=results,
            output_path=cfg.output.output_path,
        )

        # 4. 打印统计
        self._print_summary(results, elapsed, output_path)

        # 5. 关闭资源
        self.http_client.close()

        return results

    def _run_sequential(self, inputs: List[TestInput]) -> List[TestResult]:
        """顺序执行所有测试"""
        results: List[TestResult] = []
        total = len(inputs)
        interval = self.config.concurrency.request_interval

        for i, test_input in enumerate(inputs, start=1):
            logger.info(
                f"[{i}/{total}] 测试 {test_input.item_id} claimId={test_input.claim_id}"
            )
            service_name = self.http_client.resolve_service_name(test_input.item_id)
            print(f"  [{i}/{total}] {test_input.item_id}({service_name}) claimId={test_input.claim_id} ... ", end="", flush=True)

            start = time.time()
            result = self.http_client.execute(test_input)
            result.response_time_ms = int((time.time() - start) * 1000)
            results.append(result)

            status = self._format_status(result)
            print(f"{status} ({result.response_time_ms}ms)")

            # 请求间隔
            if i < total and interval > 0:
                time.sleep(interval)

        return results

    def _run_concurrent(self, inputs: List[TestInput]) -> List[TestResult]:
        """并发执行测试"""
        max_workers = self.config.concurrency.max_workers
        results: List[TestResult] = [None] * len(inputs)
        total = len(inputs)
        completed = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {}
            for idx, test_input in enumerate(inputs):
                future = executor.submit(self._execute_single, test_input)
                future_to_idx[future] = idx

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                test_input = inputs[idx]
                completed += 1

                try:
                    result = future.result()
                    results[idx] = result
                    status = self._format_status(result)
                    print(
                        f"  [{completed}/{total}] {test_input.item_id}"
                        f"({self.http_client.resolve_service_name(test_input.item_id)}) "
                        f"claimId={test_input.claim_id} ... {status} "
                        f"({result.response_time_ms}ms)"
                    )
                except Exception as e:
                    error_result = TestResult(
                        claim_id=test_input.claim_id,
                        item_id=test_input.item_id,
                        url=self.http_client.build_url(test_input.item_id),
                        error=str(e),
                    )
                    results[idx] = error_result
                    print(
                        f"  [{completed}/{total}] {test_input.item_id}"
                        f"({self.http_client.resolve_service_name(test_input.item_id)}) "
                        f"claimId={test_input.claim_id} ... ERROR: {e}"
                    )

        return results

    def _execute_single(self, test_input: TestInput) -> TestResult:
        """执行单个测试（供并发调用）"""
        start = time.time()
        result = self.http_client.execute(test_input)
        result.response_time_ms = int((time.time() - start) * 1000)
        return result

    @staticmethod
    def _format_status(result: TestResult) -> str:
        """格式化测试结果状态标签"""
        if result.error:
            return "ERROR"
        if result.passed:
            return "PASS"
        return "FAIL"

    @staticmethod
    def _print_summary(
        results: List[TestResult], elapsed: float, output_path: str
    ):
        """打印测试统计摘要"""
        total = len(results)
        success = sum(1 for r in results if r.success)
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if r.success and not r.passed)
        errors = sum(1 for r in results if r.error)
        avg_time = sum(r.response_time_ms for r in results) / total if total else 0

        print(f"\n{'='*60}")
        print(f"  测试完成！")
        print(f"  总耗时:     {elapsed:.1f}s")
        print(f"  总测试数:   {total}")
        print(f"  请求成功:   {success}")
        print(f"  校验通过:   {passed}")
        print(f"  校验不通过: {failed}")
        print(f"  请求异常:   {errors}")
        print(f"  平均响应:   {avg_time:.0f}ms")
        print(f"  结果文件:   {output_path}")
        print(f"{'='*60}\n")
