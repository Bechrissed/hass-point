# Home Assistant Minut Point Integration

This is a custom integration for Home Assistant that allows you to monitor and control your Minut Point devices. It provides access to various sensors including temperature, humidity, sound level, motion detection, and device status.

## Features

- Temperature monitoring
- Humidity monitoring
- Sound level detection
- Motion detection
- Battery level and charging status
- WiFi signal strength
- Device mount status
- Online/offline status

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed in your Home Assistant instance
2. Go to HACS > Integrations
3. Click on the three dots in the top right corner
4. Click "Custom repositories"
5. Add `https://github.com/bechrissed/hass-point` as a custom repository
6. Select "Integration" as the category
7. Click "Add"
8. Find and install "Minut Point" in HACS
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/bechrissed/hass-point)
2. Copy the `custom_components/minut_point` directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Home Assistant's Configuration > Integrations
2. Click the "+" button to add a new integration
3. Search for "Minut Point"
4. Click on it and follow the configuration steps
5. Enter your Minut Point account credentials (email and password)

## Supported Entities

Each Minut Point device will create the following entities:

### Sensors
- Temperature (°C)
- Humidity (%)
- Sound Level (dB)
- Battery Level (%)
- WiFi Signal Strength (dBm)

### Binary Sensors
- Online Status
- Charging Status
- Mount Status
- Motion Detection

## Troubleshooting

### Common Issues

1. **Integration Not Found**: Make sure you've installed the integration correctly and restarted Home Assistant
2. **Authentication Failed**: Double-check your Minut Point credentials
3. **No Devices Found**: Ensure your devices are properly set up in the Minut Point app

### Debug Logging

To enable debug logging for the integration:

1. Add the following to your `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.minut_point: debug
```
2. Restart Home Assistant

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This integration is not affiliated with Minut AB. Minut Point is a trademark of Minut AB. 