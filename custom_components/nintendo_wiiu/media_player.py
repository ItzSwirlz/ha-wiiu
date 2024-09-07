from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import *

from custom_components.nintendo_wiiu import api
from custom_components.nintendo_wiiu.coordinator import WiiUDataUpdateCoordinator

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
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_OFF | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(
        self,
        config: IntegrationWiiUConfigEntry,
        name: str,
        ip: str,
    ):
        self._attr_unique_id = config.runtime_data.coordinator.config_entry.entry_id
        self._attr_name = name
        self._attr_state = MediaPlayerState.ON
        self.config = config

    async def async_turn_off(self) -> None:
        return await self.config.runtime_data.client.async_shutdown()

    async def async_device_update(self, warning: bool = True) -> None:
        print("UPDATING")
        title = await self.config.runtime_data.client.async_get_current_title()
        self._attr_media_title = await title.text()
        self._attr_state = MediaPlayerState.PLAYING
        return await super().async_device_update(warning)
