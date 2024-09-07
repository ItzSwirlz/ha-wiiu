from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import *

from custom_components.nintendo_wiiu import api

from .data import IntegrationWiiUConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: IntegrationWiiUConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Sets up the device from the entry"""
    async_add_entities(
        [WiiUDevice(config_entry, "Wii U", config_entry.data[CONF_IP_ADDRESS])]
    )


class WiiUDevice(MediaPlayerEntity):
    _attr_supported_features = MediaPlayerEntityFeature.TURN_OFF

    def __init__(self, config: IntegrationWiiUConfigEntry, name: str, ip: str):
        super().__init__()
        self._attr_name = name
        self._attr_state = MediaPlayerState.ON
        self.config = config

    async def async_turn_off(self) -> None:
        return await self.config.runtime_data.client.async_shutdown()
