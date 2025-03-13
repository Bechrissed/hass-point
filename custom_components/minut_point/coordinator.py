"""DataUpdateCoordinator for Minut Point integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
import json
import re
import aiohttp
from bs4 import BeautifulSoup
import async_timeout
from urllib.parse import urlencode

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import (
    DOMAIN,
    MINUT_BASE_URL,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

class MinutPointDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Minut Point data."""

    def __init__(
        self,
        hass: HomeAssistant,
        username: str,
        password: str,
    ) -> None:
        """Initialize the coordinator."""
        self.username = username
        self.password = password
        self.devices = {}
        self.session = aiohttp.ClientSession()
        self.logged_in = False
        self.access_token = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def async_validate_credentials(self) -> bool:
        """Validate the user credentials."""
        try:
            await self._login()
            return True
        except ConfigEntryAuthFailed:
            return False

    async def _login(self) -> None:
        """Login to Minut Point."""
        _LOGGER.debug("Attempting to log in to Minut Point")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            # Attempt to log in using OAuth2 password grant
            login_data = {
                "client_id": "c1b451955a86f46f",
                "client_secret": "63c6688c313bc9485edebbc0bfa8336f",
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
            }

            async with self.session.post(
                "https://api.minut.com/v8/oauth/token",
                headers=headers,
                data=urlencode(login_data),
            ) as response:
                if response.status == 401:
                    _LOGGER.error("Invalid credentials")
                    raise ConfigEntryAuthFailed("Invalid credentials")
                elif response.status != 200:
                    _LOGGER.error("Login failed with status %s", response.status)
                    raise ConfigEntryAuthFailed(f"Login failed with status {response.status}")

                # Try to parse response as JSON
                try:
                    data = await response.json()
                    _LOGGER.debug("Login response: %s", json.dumps(data))
                    self.access_token = data.get("access_token")
                    if not self.access_token:
                        raise ConfigEntryAuthFailed("No access token in response")
                except json.JSONDecodeError:
                    text = await response.text()
                    _LOGGER.debug("Login response (text): %s", text[:200])
                    raise ConfigEntryAuthFailed("Invalid response from server")

            self.logged_in = True
            _LOGGER.info("Successfully logged in to Minut Point")

        except aiohttp.ClientError as err:
            _LOGGER.error("Error during login: %s", err)
            raise ConfigEntryAuthFailed(f"Error during login: {err}")

    async def _get_device_details(self, device_id: str) -> dict:
        """Get detailed metrics for a device."""
        if not self.logged_in:
            await self._login()

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        try:
            async with self.session.get(
                f"https://api.minut.com/v8/devices/{device_id}/metrics",
                headers=headers,
            ) as response:
                if response.status == 401:
                    self.logged_in = False
                    await self._login()
                    return await self._get_device_details(device_id)
                elif response.status != 200:
                    raise UpdateFailed(f"Error {response.status} while getting device details")

                try:
                    data = await response.json()
                    _LOGGER.debug("Device details response: %s", json.dumps(data))
                    return data
                except json.JSONDecodeError:
                    text = await response.text()
                    _LOGGER.debug("Device details response (text): %s", text[:200])
                    raise UpdateFailed("Invalid response from server")

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def _get_devices(self) -> dict:
        """Get list of devices and their basic info."""
        if not self.logged_in:
            await self._login()

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        try:
            async with self.session.get(
                "https://api.minut.com/v8/devices",
                headers=headers,
            ) as response:
                if response.status == 401:
                    self.logged_in = False
                    await self._login()
                    return await self._get_devices()
                elif response.status != 200:
                    raise UpdateFailed(f"Error {response.status} while getting devices")

                try:
                    data = await response.json()
                    _LOGGER.debug("Devices response: %s", json.dumps(data))
                    return data.get("devices", [])
                except json.JSONDecodeError:
                    text = await response.text()
                    _LOGGER.debug("Devices response (text): %s", text[:200])
                    raise UpdateFailed("Invalid response from server")

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with async_timeout.timeout(30):
                devices = await self._get_devices()
                if not devices:
                    return {}

                # Get details for each device
                for device in devices:
                    device_id = device["device_id"]
                    device["metrics"] = await self._get_device_details(device_id)

                return devices

        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout error: {err}")

    async def async_unload(self):
        """Clean up resources when unloading the integration."""
        if self.session:
            await self.session.close() 