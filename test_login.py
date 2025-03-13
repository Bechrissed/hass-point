#!/usr/bin/env python3
"""Test script for Minut Point login."""
import asyncio
import json
import logging
import sys
from urllib.parse import urlencode

import aiohttp

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

async def test_login(email: str, password: str) -> None:
    """Test login to Minut Point."""
    async with aiohttp.ClientSession() as session:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Attempt OAuth2 password grant login
        login_data = {
            "client_id": "c1b451955a86f46f",
            "client_secret": "63c6688c313bc9485edebbc0bfa8336f",
            "username": email,
            "password": password,
            "grant_type": "password",
        }

        try:
            async with session.post(
                "https://api.minut.com/v8/oauth/token",
                headers=headers,
                data=urlencode(login_data),
            ) as response:
                if response.status == 401:
                    _LOGGER.error("Invalid credentials")
                    return
                elif response.status != 200:
                    _LOGGER.error("Login failed with status %s", response.status)
                    return

                try:
                    data = await response.json()
                    _LOGGER.debug("Login response: %s", json.dumps(data))
                    access_token = data.get("access_token")
                    if not access_token:
                        _LOGGER.error("No access token in response")
                        return
                except json.JSONDecodeError:
                    text = await response.text()
                    _LOGGER.debug("Login response (text): %s", text[:200])
                    _LOGGER.error("Invalid response from server")
                    return

                _LOGGER.info("Successfully logged in")

                # Get devices
                headers["Authorization"] = f"Bearer {access_token}"
                async with session.get(
                    "https://api.minut.com/v8/devices",
                    headers=headers,
                ) as response:
                    if response.status != 200:
                        _LOGGER.error("Failed to get devices: %s", response.status)
                        return

                    try:
                        data = await response.json()
                        devices = data.get("devices", [])
                        _LOGGER.debug("Devices response: %s", json.dumps(data))

                        # Save devices to file
                        with open("hass_devices.json", "w") as f:
                            json.dump(devices, f, indent=2)
                            _LOGGER.info("Saved device data to hass_devices.json")

                    except json.JSONDecodeError:
                        _LOGGER.error("Invalid devices response")
                        return

        except aiohttp.ClientError as err:
            _LOGGER.error("Error during login: %s", err)
            return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_login.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    asyncio.run(test_login(email, password)) 