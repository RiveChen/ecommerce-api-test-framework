import logging
import requests

logger = logging.getLogger(__name__)


class BaseClient:
    """
    requests.Session 封装层。

    管理 Session 生命周期、拼接 URL、统一记录请求日志。
    """

    def __init__(
        self, base_url: str, timeout: int = 10, headers: dict | None = None
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def update_headers(self, headers: dict) -> None:
        self.session.headers.update(headers)

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("→ %s %s", method.upper(), url)

        if kwargs.get("json"):
            logger.debug("  body: %s", kwargs["json"])

        response = self.session.request(
            method=method, url=url, timeout=self.timeout, **kwargs
        )

        logger.info(
            "← %s  %.3fs", response.status_code, response.elapsed.total_seconds()
        )
        return response

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict | None = None) -> requests.Response:
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: dict | None = None) -> requests.Response:
        return self._request("PUT", endpoint, json=json)

    def patch(self, endpoint: str, json: dict | None = None) -> requests.Response:
        return self._request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> requests.Response:
        return self._request("DELETE", endpoint)
