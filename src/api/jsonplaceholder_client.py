from __future__ import annotations
from collections.abc import Mapping
from typing import Any
import requests
from requests import Response, Session


class ApiClientError(RuntimeError):
    """Raised when an API request fails before receiving a response."""


class JsonPlaceholderClient:
    """Small client that centralizes base URL, headers, and timeouts."""

    def __init__(
        self,
        base_url: str,
        timeout_seconds: float,
        default_headers: Mapping[str, str] | None = None,
        session: Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                **(default_headers or {}),
            },
        )

    def get_posts(self) -> Response:
        return self.request("GET", "/posts")

    def get_post(self, post_id: int) -> Response:
        return self.request("GET", f"/posts/{post_id}")

    def create_post(self, payload: Mapping[str, Any]) -> Response:
        return self.request("POST", "/posts", json=payload)

    def update_post(self, post_id: int, payload: Mapping[str, Any]) -> Response:
        return self.request("PUT", f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id: int) -> Response:
        return self.request("DELETE", f"/posts/{post_id}")

    def close(self) -> None:
        self.session.close()

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Send a request and return the response for status assertions."""

        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout_seconds)

        try:
            return self.session.request(method=method, url=url, **kwargs)
        except requests.RequestException as exc:
            raise ApiClientError(
                f"{method.upper()} {url} failed before receiving a response",
            ) from exc
