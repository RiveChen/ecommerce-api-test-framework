import requests
from utils.base_client import BaseClient


class UserAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def list(self) -> requests.Response:
        """GET /users — 用户列表"""
        return self.client.get("/users")

    def get(self, user_id: int) -> requests.Response:
        """GET /users/{id} — 单个用户信息"""
        return self.client.get(f"/users/{user_id}")

    def search(self, query: str) -> requests.Response:
        """GET /users/search?q= — 用户搜索"""
        return self.client.get("/users/search", params={"q": query})

    def get_carts(self, user_id: int) -> requests.Response:
        """GET /users/{id}/carts — 用户的购物车"""
        return self.client.get(f"/users/{user_id}/carts")
