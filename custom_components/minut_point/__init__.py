"""The Minut Point integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import MinutPointDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=1)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Minut Point component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Minut Point from a config entry."""
    coordinator = MinutPointDataUpdateCoordinator(
        hass,
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await coordinator.async_close()
        raise

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        await hass.data[DOMAIN][entry.entry_id].async_close()

    return unload_ok 