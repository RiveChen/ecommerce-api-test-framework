# 注意：DummyJSON 是 fake API，写操作返回成功但不真实持久化，适合测试框架的请求/响应逻辑
import pytest
import allure
from utils import assertion

pytestmark = allure.feature("Products 模块")

_NEW_PRODUCT = {
    "title": "pytest-auto-test",
    "price": 9.99,
    "stock": 10,
    "category": "test-category",
}


@allure.story("新增商品")
@pytest.mark.products
def test_add_product(product_api):
    resp = product_api.add(_NEW_PRODUCT)
    assert resp.status_code in (
        200,
        201,
    ), f"Expected 2xx, got {resp.status_code}: {resp.text}"
    assertion.assert_json_key(resp, "id", "title")
    assertion.assert_field_equals(resp, "title", _NEW_PRODUCT["title"])


@allure.story("全量更新商品")
@pytest.mark.products
def test_update_product(product_api):
    resp = product_api.update(1, {"price": 19.99})
    assertion.assert_status_code(resp, 200)
    assertion.assert_field_equals(resp, "price", 19.99)


@allure.story("部分更新商品")
@pytest.mark.products
def test_patch_product(product_api):
    resp = product_api.patch(1, {"title": "Patched by pytest"})
    assertion.assert_status_code(resp, 200)
    assertion.assert_field_equals(resp, "title", "Patched by pytest")


@allure.story("删除商品")
@pytest.mark.products
def test_delete_product(product_api):
    resp = product_api.delete(1)
    assertion.assert_status_code(resp, 200)
    assert resp.json().get("isDeleted") is True
