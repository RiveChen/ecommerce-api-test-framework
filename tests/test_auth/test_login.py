import pytest
import allure
from utils import assertion

pytestmark = allure.feature("Auth 模块")


@allure.story("登录成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.auth
@pytest.mark.smoke
def test_login_success(auth_api):
    with allure.step("发送正确凭证"):
        resp = auth_api.login("emilys", "emilyspass")
    with allure.step("验证状态码和 token 字段"):
        assertion.assert_status_code(resp, 200)
        assertion.assert_json_key(resp, "accessToken", "refreshToken")
        assertion.assert_response_time(resp)


@allure.story("登录失败 — 凭证错误")
@pytest.mark.auth
@pytest.mark.parametrize(
    "username,password,desc",
    [
        ("emilys", "wrongpassword", "密码错误"),
        ("no_such_user_xyz", "anypassword", "用户不存在"),
    ],
)
def test_login_invalid_credentials(auth_api, username, password, desc):
    resp = auth_api.login(username, password)
    assert resp.status_code != 200, f"{desc}: 应返回非 200，实际 {resp.status_code}"


@allure.story("获取当前用户信息")
@pytest.mark.auth
def test_get_me(auth_api):
    resp = auth_api.get_me()
    assertion.assert_status_code(resp, 200)
    assertion.assert_json_key(resp, "id", "username", "email")
    assertion.assert_response_time(resp)
