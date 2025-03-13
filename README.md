# Minut Point Custom Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

A custom integration for Home Assistant that integrates with Minut Point devices through the official Minut API v8.

## Features

- Temperature sensor (°C)
- Humidity sensor (%)
- Sound level sensor (dB)
- Battery level sensor (%)
- WiFi signal strength sensor (dBm)
- Motion detection (binary sensor)
- Online status (binary sensor)
- Charging status (binary sensor)
- Mount status (binary sensor)

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository:
   - URL: `https://github.com/bechrissed/hass-point`
   - Category: Integration

2. Search for "Minut Point Custom" in HACS and install it.

3. Restart Home Assistant.

### Manual Installation

1. Copy the `custom_components/minut_point` directory to your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.

## Configuration

1. Go to Settings -> Devices & Services
2. Click the "+ ADD INTEGRATION" button
3. Search for "Minut Point Custom"
4. Enter your Minut Point credentials (email and password)

## How it Works

This integration uses the official Minut API v8 to:
1. Authenticate using OAuth2 password grant flow
2. Retrieve device information and sensor data
3. Update sensor states in real-time
4. Handle token refresh automatically

## Troubleshooting

If you experience any issues:

1. Check that your credentials are correct
2. Ensure you can log in to the Minut Point web interface
3. Check the Home Assistant logs for any error messages
4. If issues persist, please open an issue on GitHub

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Creating pull requests

## Disclaimer

This is a third-party integration and is not officially supported by Minut. Use at your own risk.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

[hass-point]: https://github.com/Bechrissed/hass-point/
[commits-shield]: https://img.shields.io/github/commit-activity/y/Bechrissed/hass-point.svg?style=for-the-badge
[commits]: https://github.com/Bechrissed/hass-point/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/Bechrissed/hass-point.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Bechrissed/hass-point.svg?style=for-the-badge
[releases]: https://github.com/Bechrissed/hass-point/releases
