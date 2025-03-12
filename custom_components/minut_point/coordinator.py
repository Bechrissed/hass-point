"""DataUpdateCoordinator for Minut Point integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
import json
import aiohttp
from bs4 import BeautifulSoup
import re

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import (
    DOMAIN,
    MINUT_LOGIN_URL,
    MINUT_DASHBOARD_URL,
    MINUT_DEVICES_URL,
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
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession()
        self._devices = {}
        self._logged_in = False

    async def _async_update_data(self):
        """Update data via web scraping."""
        try:
            if not self._logged_in and not await self._login():
                raise ConfigEntryAuthFailed("Failed to authenticate with Minut Point")

            devices_data = await self._fetch_devices_data()
            if not devices_data:
                _LOGGER.debug("No devices found, trying to re-login")
                self._logged_in = False
                if not await self._login():
                    raise ConfigEntryAuthFailed("Failed to re-authenticate with Minut Point")
                devices_data = await self._fetch_devices_data()
                
            return devices_data
        except Exception as err:
            _LOGGER.error("Error updating Minut Point data: %s", err)
            raise

    async def _login(self) -> bool:
        """Login to Minut Point dashboard."""
        try:
            # First get the login page to extract any necessary tokens
            async with self.session.get(MINUT_LOGIN_URL) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to get login page: %s", response.status)
                    return False
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find the CSRF token
                csrf_token = None
                for meta in soup.find_all('meta'):
                    if meta.get('name') == 'csrf-token':
                        csrf_token = meta.get('content')
                        break
                
                if not csrf_token:
                    _LOGGER.error("Could not find CSRF token")
                    return False

                # Find the form action URL
                form = soup.find('form', {'action': True})
                if not form:
                    _LOGGER.error("Could not find login form")
                    return False

            # Perform login
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRF-Token': csrf_token,
                'Origin': 'https://web.minut.com',
                'Referer': MINUT_LOGIN_URL
            }
            
            login_data = {
                'email': self.username,
                'password': self.password,
                '_csrf': csrf_token
            }
            
            async with self.session.post(
                MINUT_LOGIN_URL,
                data=login_data,
                headers=headers,
                allow_redirects=True
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Login failed with status: %s", response.status)
                    return False
                
                # Check if we're logged in by looking for specific elements
                html = await response.text()
                if '/login' in str(response.url):
                    _LOGGER.error("Still on login page after login attempt")
                    return False
                
                self._logged_in = True
                _LOGGER.debug("Successfully logged in to Minut Point")
                return True

        except Exception as err:
            _LOGGER.error("Login failed: %s", err)
            return False

    async def _fetch_devices_data(self) -> dict:
        """Fetch device data from the devices page."""
        devices = {}
        
        try:
            # First get the devices overview page
            async with self.session.get(MINUT_DEVICES_URL) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to fetch devices page: %s", response.status)
                    return {}
                
                html = await response.text()
                if '/login' in str(response.url):
                    _LOGGER.debug("Session expired, need to re-login")
                    self._logged_in = False
                    return {}
                    
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all device links
                device_links = []
                for a in soup.find_all('a', href=True):
                    if '/devices/' in a['href'] and not a['href'].endswith('/devices/'):
                        device_links.append(a['href'])
                
                # Fetch data for each device
                for device_link in device_links:
                    device_url = f"https://web.minut.com{device_link}"
                    device_data = await self._fetch_device_detail(device_url)
                    if device_data:
                        device_id = device_link.split('/')[-1]
                        devices[device_id] = device_data
                
                return devices

        except Exception as err:
            _LOGGER.error("Failed to fetch devices data: %s", err)
            return {}

    async def _fetch_device_detail(self, device_url: str) -> dict | None:
        """Fetch detailed data for a specific device."""
        try:
            async with self.session.get(device_url) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to fetch device detail: %s", response.status)
                    return None
                
                html = await response.text()
                if '/login' in str(response.url):
                    _LOGGER.debug("Session expired while fetching device details")
                    self._logged_in = False
                    return None
                    
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract device name
                name_element = soup.find('h1')
                if not name_element:
                    return None
                
                device_data = {
                    'name': name_element.text.strip()
                }
                
                # Extract sensor values
                # Temperature
                temp_element = soup.find(string=re.compile(r'°C'))
                if temp_element:
                    try:
                        device_data['temperature'] = float(re.search(r'([\d.]+)°C', temp_element).group(1))
                    except (AttributeError, ValueError):
                        pass
                
                # Humidity
                humidity_element = soup.find(string=re.compile(r'%.*humidity', re.IGNORECASE))
                if humidity_element:
                    try:
                        device_data['humidity'] = float(re.search(r'([\d.]+)%', humidity_element).group(1))
                    except (AttributeError, ValueError):
                        pass
                
                # Sound level
                sound_element = soup.find(string=re.compile(r'dB'))
                if sound_element:
                    try:
                        device_data['sound'] = float(re.search(r'([\d.]+)\s*dB', sound_element).group(1))
                    except (AttributeError, ValueError):
                        pass
                
                # Motion
                motion_element = soup.find(string=re.compile(r'motion', re.IGNORECASE))
                if motion_element:
                    device_data['motion'] = 1 if 'detected' in motion_element.lower() else 0
                
                # Battery
                battery_element = soup.find(string=re.compile(r'%.*battery', re.IGNORECASE))
                if battery_element:
                    try:
                        device_data['battery'] = float(re.search(r'([\d.]+)%', battery_element).group(1))
                    except (AttributeError, ValueError):
                        pass
                
                return device_data

        except Exception as err:
            _LOGGER.error("Failed to fetch device detail: %s", err)
            return None

    async def async_validate_credentials(self) -> bool:
        """Validate credentials."""
        return await self._login()

    async def async_close(self) -> None:
        """Close the session."""
        await self.session.close() 