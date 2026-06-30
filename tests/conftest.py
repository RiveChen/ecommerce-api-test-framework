import os
import yaml
import pytest
from utils.base_client import BaseClient
from utils.api.auth_api import AuthAPI
from utils.api.product_api import ProductAPI
from utils.api.user_api import UserAPI


def _load_config() -> dict:
    env = os.getenv("ENV", "test")
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)[env]


@pytest.fixture(scope="session")
def client() -> BaseClient:
    cfg = _load_config()
    return BaseClient(
        base_url=cfg["base_url"],
        timeout=cfg["timeout"],
        headers=cfg["headers"],
    )


@pytest.fixture(scope="session")
def token(client: BaseClient) -> str:
    """登录一次，token 注入 Session header，全局所有用例共享。"""
    resp = AuthAPI(client).login("emilys", "emilyspass")
    assert resp.status_code == 200, f"登录失败：{resp.text}"
    t = resp.json()["accessToken"]
    client.update_headers({"Authorization": f"Bearer {t}"})
    return t


@pytest.fixture(scope="session")
def auth_api(client: BaseClient, token: str) -> AuthAPI:
    return AuthAPI(client)


@pytest.fixture(scope="session")
def product_api(client: BaseClient, token: str) -> ProductAPI:
    return ProductAPI(client)


@pytest.fixture(scope="session")
def user_api(client: BaseClient, token: str) -> UserAPI:
    return UserAPI(client)
