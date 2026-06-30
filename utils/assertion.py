"""
共享断言方法。测试文件通过 from utils import assertion 调用。
"""

from typing import Any
import requests


def assert_status_code(response: requests.Response, expected: int) -> None:
    actual = response.status_code
    assert actual == expected, (
        f"Status {actual} ≠ {expected} | "
        f"{response.request.method} {response.url}\n"
        f"Body: {response.text[:300]}"
    )


def assert_response_time(response: requests.Response, max_seconds: float = 2.0) -> None:
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, f"耗时 {elapsed:.3f}s 超过阈值 {max_seconds}s"


def assert_json_key(response: requests.Response, *keys: str) -> None:
    """验证响应 JSON 包含指定字段"""
    data = response.json()
    for key in keys:
        assert key in data, f"响应缺少字段 '{key}'，实际字段：{list(data.keys())}"


def assert_field_equals(response: requests.Response, key: str, expected: Any) -> None:
    """验证响应 JSON 某字段的值"""
    actual = response.json().get(key)
    assert actual == expected, f"字段 '{key}': expected={expected!r}, actual={actual!r}"
