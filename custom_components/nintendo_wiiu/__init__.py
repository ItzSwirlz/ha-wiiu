"""
Custom integration to integrate nintendo_wiiu with Home Assistant.

For more details about this integration, please refer to
https://github.com/ItzSwirlz/nintendo_wiiu
"""

from __future__ import annotations

from pickle import TRUE
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration
from sqlalchemy import true

from .api import IntegrationWiiUApiClient
from .coordinator import WiiUDataUpdateCoordinator
from .data import IntegrationWiiUData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import IntegrationWiiUConfigEntry

PLATFORMS: list[Platform] = [
    Platform.MEDIA_PLAYER,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationWiiUConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = WiiUDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = IntegrationWiiUData(
        client=IntegrationWiiUApiClient(
            ip="192.168.1.195:8572",  # TODO: be configurable
            session=async_get_clientsession(hass, verify_ssl=False),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: IntegrationWiiUConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: IntegrationWiiUConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
