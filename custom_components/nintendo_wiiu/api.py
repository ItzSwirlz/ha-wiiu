"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout
from sqlalchemy import false


class IntegrationWiiUApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntegrationWiiUApiClientCommunicationError(
    IntegrationWiiUApiClientError,
):
    """Exception to indicate a communication error."""


class IntegrationWiiUApiClientAuthenticationError(
    IntegrationWiiUApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise IntegrationWiiUApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class IntegrationWiiUApiClient:
    """Sample API Client."""

    def __init__(
        self,
        ip: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._ip = ip
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    async def async_get_device_serial(self) -> str | None:
        return await self._api_wrapper(
            method="get", url="http://" + self._ip + "/device/serial_id"
        )

    async def async_shutdown(self):
        return await self._api_wrapper(
            method="post", url="http://" + self._ip + "/power/shutdown"
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                # We don't use SSL
                response = await self._session.request(
                    method=method, url=url, headers=headers, json=data, ssl=False
                )
                _verify_response_or_raise(response)

                # Not all Ristretto requests return information, prevent an exception being thrown
                if data:
                    return await response.json()
                return await response.json(content_type=None)

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise IntegrationWiiUApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise IntegrationWiiUApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise IntegrationWiiUApiClientError(
                msg,
            ) from exception
