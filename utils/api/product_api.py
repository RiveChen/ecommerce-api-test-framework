import requests
from utils.base_client import BaseClient


class ProductAPI:
    def __init__(self, client: BaseClient):
        self.client = client

    def list(self, limit: int = 30, skip: int = 0) -> requests.Response:
        """GET /products — 商品列表，支持分页"""
        return self.client.get("/products", params={"limit": limit, "skip": skip})

    def get(self, product_id: int) -> requests.Response:
        """GET /products/{id} — 单个商品详情"""
        return self.client.get(f"/products/{product_id}")

    def search(self, query: str) -> requests.Response:
        """GET /products/search?q= — 关键词搜索"""
        return self.client.get("/products/search", params={"q": query})

    def add(self, data: dict) -> requests.Response:
        """POST /products/add — 新增商品（DummyJSON 不真实持久化）"""
        return self.client.post("/products/add", json=data)

    def update(self, product_id: int, data: dict) -> requests.Response:
        """PUT /products/{id} — 全量更新"""
        return self.client.put(f"/products/{product_id}", json=data)

    def patch(self, product_id: int, data: dict) -> requests.Response:
        """PATCH /products/{id} — 部分更新"""
        return self.client.patch(f"/products/{product_id}", json=data)

    def delete(self, product_id: int) -> requests.Response:
        """DELETE /products/{id} — 删除商品"""
        return self.client.delete(f"/products/{product_id}")
