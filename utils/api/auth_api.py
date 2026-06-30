import requests
from utils.base_client import BaseClient


class AuthAPI:
    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def login(self, username: str, password: str) -> requests.Response:
        """POST /auth/login — 返回 accessToken 和 refreshToken"""
        return self.client.post(
            "/auth/login",
            json={"username": username, "password": password, "expiresInMins": 30},
        )

    def get_me(self) -> requests.Response:
        """GET /auth/me — 获取当前登录用户信息（需要 Authorization header）"""
        return self.client.get("/auth/me")

    def refresh(self, refresh_token: str) -> requests.Response:
        """POST /auth/refresh — 刷新 accessToken"""
        return self.client.post(
            "/auth/refresh",
            json={"refreshToken": refresh_token, "expiresInMins": 30},
        )
