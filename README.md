# HACS Minut Point Integration


![Minut Point integration](https://raw.githubusercontent.com/Bechrissed/hass-point/main/docs/assets/minutliar.png "Minut point liar liar")

A long long time ago (2017 :p) there was a swedish startup called Minut....

 Minut’s created a Kickstarter project to fund the development of their first “Point” devices. After successfully obtaining the initial investment(s) minut released the Point devices with limited features. Promised features and services where added later on or never added at all. Unfortunately, Minut has been quite disappointing toward its early backers, failing to deliver on several promises made during the campaign. One of these was a lifetime subscription for early backers, which has never been fully honored.
 
 To use Minut’s API, backers must subscribe to a monthly plan. Minut initially offered API access to early backers through customer support, enabling it on request. However, when I asked a few times for them to enable it on my account, they refused without any clear explanation. Coupled with their poor communication, it feels like Minut views those who helped them get started as suckers.
 
 In response, I created this HACS integrationt to be able to use the Point devices in Home Assistant without the need of a subscription. The integration utilizes the same logic Minut.com we get for free through the web dashboard pages. Configure the required details of your minut account and you’re good to go.
 
 This is a very quick and dirty approach, where half of the code came from modified Ai generated code, there’s plenty of room for improvement. It works for my needs right now, but I might refine it in the future. If you’d like to contribute, feel free to fork the project or send a pull request to add features or fix any issues.
 
 Cheerio!



**Minut Point integration usage**

This is a custom integration for Home Assistant that allows you to monitor and control your Minut Point devices. It provides access to various sensors including temperature, humidity, sound level, motion detection, and device status. No subscription is needed. It works for the original point devices but I didn't test it on newer versions or other minut devices as I don't own any.

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

[hass-point]: https://github.com/Bechrissed/hass-point/
[commits-shield]: https://img.shields.io/github/commit-activity/y/Bechrissed/hass-point.svg?style=for-the-badge
[commits]: https://github.com/Bechrissed/hass-point/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/Bechrissed/hass-point.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Bechrissed/hass-point.svg?style=for-the-badge
[releases]: https://github.com/Bechrissed/hass-point/releases
[download-latest-shield]: https://img.shields.io/github/downloads/Bechrissed/hass-point/latest/total?style=for-the-badge