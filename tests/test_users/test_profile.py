import pytest
import allure
from utils import assertion
from utils.data_loader import load_cases

pytestmark = allure.feature("Users 模块")

_get_by_id_cases = load_cases("user_cases.yaml", "get_by_id")


@allure.story("用户列表")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.users
@pytest.mark.smoke
def test_list_users(user_api):
    with allure.step("请求用户列表"):
        resp = user_api.list()
    with allure.step("验证响应结构"):
        assertion.assert_status_code(resp, 200)
        assertion.assert_json_key(resp, "users", "total")
        assert len(resp.json()["users"]) > 0
        assertion.assert_response_time(resp)


@allure.story("查询单个用户")
@pytest.mark.users
@pytest.mark.parametrize(
    "case", _get_by_id_cases, ids=[c["id"] for c in _get_by_id_cases]
)
def test_get_user_by_id(user_api, case):
    with allure.step(f"{case['id']}: {case['description']}"):
        resp = user_api.get(case["input"]["user_id"])
    assertion.assert_status_code(resp, case["expected"]["status_code"])
    if case["expected"]["status_code"] == 200:
        assertion.assert_json_key(resp, "id", "username")


@allure.story("用户搜索")
@pytest.mark.users
def test_search_users(user_api):
    resp = user_api.search("Emily")
    assertion.assert_status_code(resp, 200)
    assert resp.json()["total"] > 0


@allure.story("获取用户购物车")
@pytest.mark.users
def test_get_user_carts(user_api):
    resp = user_api.get_carts(1)
    assertion.assert_status_code(resp, 200)
    assertion.assert_json_key(resp, "carts")
