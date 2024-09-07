"""Adds config flow for WiiU."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    IntegrationWiiUApiClient,
    IntegrationWiiUApiClientAuthenticationError,
    IntegrationWiiUApiClientCommunicationError,
    IntegrationWiiUApiClientError,
)
from .const import DOMAIN, LOGGER


class WiiUFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for WiiU."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    ip=user_input[CONF_IP_ADDRESS],
                )
            except IntegrationWiiUApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except IntegrationWiiUApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except IntegrationWiiUApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_IP_ADDRESS],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IP_ADDRESS,
                        default=(user_input or {}).get(CONF_IP_ADDRESS, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    )
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, ip: str) -> None:
        """Validate credentials."""
        client = IntegrationWiiUApiClient(
            ip=ip,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
