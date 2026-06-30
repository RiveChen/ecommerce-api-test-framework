import pytest
import allure
from utils import assertion

pytestmark = allure.feature("Products 模块")


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
@pytest.mark.parametrize("limit", [5, 10, 20])
def test_list_products_with_limit(product_api, limit):
    resp = product_api.list(limit=limit)
    assertion.assert_status_code(resp, 200)
    assert len(resp.json()["products"]) == limit


@allure.story("查询单个商品")
@pytest.mark.products
@pytest.mark.parametrize(
    "product_id,expected_status",
    [
        (1, 200),
        (2, 200),
        (99999, 404),
    ],
)
def test_get_product_by_id(product_api, product_id, expected_status):
    resp = product_api.get(product_id)
    assertion.assert_status_code(resp, expected_status)
    if expected_status == 200:
        assertion.assert_field_equals(resp, "id", product_id)


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
