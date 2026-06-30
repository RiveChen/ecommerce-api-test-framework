import pytest
import allure
from utils import assertion
from utils.data_loader import load_cases

pytestmark = allure.feature("Products 模块")

_get_by_id_cases = load_cases("product_cases.yaml", "get_by_id")
_limit_cases = load_cases("product_cases.yaml", "list_with_limit")


@allure.story("商品列表")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.products
@pytest.mark.smoke
def test_list_products_default(product_api):
    with allure.step("请求默认商品列表"):
        resp = product_api.list()
    with allure.step("验证响应结构"):
        assertion.assert_status_code(resp, 200)
        assertion.assert_json_key(resp, "products", "total", "skip", "limit")
        assert len(resp.json()["products"]) > 0
        assertion.assert_response_time(resp)


@allure.story("商品列表 — 分页参数")
@pytest.mark.products
@pytest.mark.parametrize("case", _limit_cases, ids=[c["id"] for c in _limit_cases])
def test_list_products_with_limit(product_api, case):
    with allure.step(f"{case['id']}: {case['description']}"):
        resp = product_api.list(limit=case["input"]["limit"])
    assertion.assert_status_code(resp, 200)
    assert len(resp.json()["products"]) == case["expected"]["count"]


@allure.story("查询单个商品")
@pytest.mark.products
@pytest.mark.parametrize(
    "case", _get_by_id_cases, ids=[c["id"] for c in _get_by_id_cases]
)
def test_get_product_by_id(product_api, case):
    with allure.step(f"{case['id']}: {case['description']}"):
        resp = product_api.get(case["input"]["product_id"])
    assertion.assert_status_code(resp, case["expected"]["status_code"])
    if case["expected"]["status_code"] == 200:
        assertion.assert_field_equals(resp, "id", case["input"]["product_id"])


@allure.story("商品搜索 — 有结果")
@pytest.mark.products
def test_search_products_found(product_api):
    resp = product_api.search("phone")
    assertion.assert_status_code(resp, 200)
    assert resp.json()["total"] > 0


@allure.story("商品搜索 — 无结果")
@pytest.mark.products
def test_search_products_not_found(product_api):
    resp = product_api.search("xyzxyznonexistent999")
    assertion.assert_status_code(resp, 200)
    assert resp.json()["total"] == 0
