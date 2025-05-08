from datetime import datetime, timezone
from typing import Any, Optional

import requests
from loguru import logger


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        token_endpoint: Optional[str] = None,
        refresh_endpoint: Optional[str] = None,
        auth_payload: Optional[dict] = None,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        access_expires_at: Optional[datetime] = None,
        refresh_expires_at: Optional[datetime] = None,
    ) -> None:
        self._base_url: str = base_url.rstrip("/")
        self._token_endpoint: Optional[str] = token_endpoint
        self._refresh_endpoint: Optional[str] = refresh_endpoint
        self._auth_payload: Optional[dict] = auth_payload
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._access_expires_at = access_expires_at
        self._refresh_expires_at = refresh_expires_at

        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        self._session = session

    @property
    def _is_access_token_expired(self) -> bool:
        if not self._access_expires_at:
            return True
        return datetime.now(timezone.utc) >= self._access_expires_at

    @property
    def _is_refresh_token_expired(self) -> bool:
        if not self._refresh_expires_at:
            return True
        return datetime.now(timezone.utc) >= self._refresh_expires_at

    @property
    def _is_refresh_required(self) -> Optional[dict[str, Any]]:
        return self._refresh_endpoint and self._refresh_token

    @property
    def _refresh_payload(self) -> Optional[dict[str, Any]]:
        return {
            "refresh": self._refresh_token,
        } if self._refresh_endpoint and self._refresh_token else None

    def _authenticate(self) -> bool:
        if not all([self._token_endpoint, self._auth_payload]):
            self._access_token = None
            self._refresh_token = None
            self._access_expires_at = None
            self._refresh_expires_at = None
            return True

        # Check if the access token is expired
        if self._is_access_token_expired:
            auth_endpoint, payload = (
                (self._refresh_endpoint, self._refresh_payload)
                if self._is_refresh_required
                else (self._token_endpoint, self._auth_payload)
            )
            if self._is_refresh_token_expired:
                auth_endpoint, payload = (self._token_endpoint, self._auth_payload)

            url: str = f"{self._base_url}/{auth_endpoint.lstrip('/')}"

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Authentication response: {data}")

                self._access_token = data.get("access_token")
                self._refresh_token = data.get("refresh_token")
                self._access_expires_at = datetime.fromisoformat(
                    data.get("access_expires_at")
                )
                self._refresh_expires_at = datetime.fromisoformat(
                    data.get("refresh_expires_at")
                )
                self._session.headers.update({"Authorization": f"Bearer {self._access_token}"})
                return True
            except (TypeError, requests.RequestException) as error:
                logger.error(f"Authentication error: {error}")
                self._access_token = None
                self._refresh_token = None
                self._access_expires_at = None
                self._refresh_expires_at = None
                return False

        return True

    @property
    def session(self) -> requests.Session:
        self._authenticate()
        return self._session

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> requests.Response:
        url = f"{self._base_url}/{endpoint.lstrip("/")}"
        response = self.session.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[dict] = None) -> requests.Response:
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[dict] = None) -> requests.Response:
        return self._request("PUT", endpoint, data=data)

    def patch(self, endpoint: str, data: Optional[dict] = None) -> requests.Response:
        return self._request("PATCH", endpoint, data=data)

    def delete(self, endpoint: str) -> requests.Response:
        return self._request("DELETE", endpoint)

    def head(self, endpoint: str) -> requests.Response:
        return self._request("HEAD", endpoint)

    def options(self, endpoint: str) -> requests.Response:
        return self._request("OPTIONS", endpoint)

    def trace(self, endpoint: str) -> requests.Response:
        return self._request("TRACE", endpoint)

    def connect(self, endpoint: str) -> requests.Response:
        return self._request("CONNECT", endpoint)
