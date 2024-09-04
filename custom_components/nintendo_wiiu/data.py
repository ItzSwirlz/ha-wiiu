"""Custom types for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import IntegrationWiiUApiClient
    from .coordinator import WiiUDataUpdateCoordinator


type IntegrationWiiUConfigEntry = ConfigEntry[IntegrationWiiUData]


@dataclass
class IntegrationWiiUData:
    """Data for the WiiU integration."""

    client: IntegrationWiiUApiClient
    coordinator: WiiUDataUpdateCoordinator
    integration: Integration
