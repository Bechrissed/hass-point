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
            _LOGGER.debug("Starting login process...")
            
            # First get the login page to extract any necessary tokens
            async with self.session.get(MINUT_LOGIN_URL) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to get login page: %s", response.status)
                    return False
                
                _LOGGER.debug("Got login page, status: %s", response.status)
                html = await response.text()
                _LOGGER.debug("Login page content length: %d", len(html))
                
                # Save HTML for debugging if needed
                _LOGGER.debug("Full login page HTML: %s", html)
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Try to find CSRF token in multiple ways
                csrf_token = None
                
                # Method 1: Look for a meta tag with name="csrf-token"
                meta = soup.find('meta', {'name': 'csrf-token'})
                if meta:
                    csrf_token = meta.get('content')
                    _LOGGER.debug("Found CSRF token in meta tag: %s", csrf_token)
                
                # Method 2: Look for hidden input with name containing csrf
                if not csrf_token:
                    for input_tag in soup.find_all('input', {'type': 'hidden'}):
                        if input_tag.get('name', '').lower().find('csrf') != -1:
                            csrf_token = input_tag.get('value')
                            _LOGGER.debug("Found CSRF token in hidden input: %s", csrf_token)
                            break
                
                # Method 3: Look for any form with data-csrf attribute
                if not csrf_token:
                    form = soup.find('form', {'data-csrf': True})
                    if form:
                        csrf_token = form.get('data-csrf')
                        _LOGGER.debug("Found CSRF token in form data-csrf: %s", csrf_token)
                
                # Method 4: Look for script tag containing csrf token
                if not csrf_token:
                    for script in soup.find_all('script'):
                        if script.string and 'csrf' in script.string.lower():
                            match = re.search(r'csrf["\']?\s*:\s*["\']([^"\']+)["\']', script.string)
                            if match:
                                csrf_token = match.group(1)
                                _LOGGER.debug("Found CSRF token in script tag: %s", csrf_token)
                                break
                
                if not csrf_token:
                    _LOGGER.error("Could not find CSRF token in page")
                    _LOGGER.debug("Available forms: %s", soup.find_all('form'))
                    _LOGGER.debug("Available meta tags: %s", soup.find_all('meta'))
                    _LOGGER.debug("Available hidden inputs: %s", soup.find_all('input', {'type': 'hidden'}))
                    return False

                # Find the form action URL
                form = soup.find('form', {'method': 'post'})
                if not form:
                    _LOGGER.error("Could not find login form")
                    return False

                login_url = form.get('action')
                if login_url:
                    if not login_url.startswith('http'):
                        login_url = f"https://web.minut.com{login_url}"
                else:
                    login_url = MINUT_LOGIN_URL

                _LOGGER.debug("Using login URL: %s", login_url)

            # Perform login
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRF-Token': csrf_token,
                'Origin': 'https://web.minut.com',
                'Referer': MINUT_LOGIN_URL,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
                'Cookie': f'XSRF-TOKEN={csrf_token}'
            }
            
            login_data = {
                'email': self.username,
                'password': self.password,
                '_csrf': csrf_token,
                'csrf_token': csrf_token,
                'remember': 'on'
            }
            
            _LOGGER.debug("Attempting login with data: %s", login_data)
            
            async with self.session.post(
                login_url,
                data=login_data,
                headers=headers,
                allow_redirects=True
            ) as response:
                _LOGGER.debug("Login response status: %s", response.status)
                _LOGGER.debug("Login response URL: %s", response.url)
                
                html = await response.text()
                _LOGGER.debug("Login response content length: %d", len(html))
                _LOGGER.debug("Login response HTML: %s", html)
                
                if response.status != 200:
                    _LOGGER.error("Login failed with status: %s", response.status)
                    return False
                
                # Check if we're logged in
                if '/login' in str(response.url):
                    soup = BeautifulSoup(html, 'html.parser')
                    error = soup.find('div', {'class': ['alert-danger', 'error', 'alert']})
                    if error:
                        _LOGGER.error("Login error: %s", error.text.strip())
                    else:
                        _LOGGER.error("Still on login page after login attempt")
                    return False
                
                # Verify we can access the dashboard
                async with self.session.get(MINUT_DASHBOARD_URL) as dash_response:
                    _LOGGER.debug("Dashboard response status: %s", dash_response.status)
                    dash_html = await dash_response.text()
                    _LOGGER.debug("Dashboard HTML: %s", dash_html)
                    
                    if dash_response.status != 200 or '/login' in str(dash_response.url):
                        _LOGGER.error("Could not access dashboard after login")
                        return False
                
                self._logged_in = True
                _LOGGER.debug("Successfully logged in to Minut Point")
                return True

        except Exception as err:
            _LOGGER.error("Login failed with exception: %s", str(err))
            _LOGGER.exception("Full exception details:")
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