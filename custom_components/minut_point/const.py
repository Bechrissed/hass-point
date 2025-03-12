"""Constants for the Minut Point integration."""

DOMAIN = "minut_point"

# Base URLs
MINUT_LOGIN_URL = "https://web.minut.com/login"
MINUT_DASHBOARD_URL = "https://web.minut.com/dashboard"
MINUT_DEVICES_URL = "https://web.minut.com/devices"

# Sensor types
SENSOR_TEMPERATURE = "temperature"
SENSOR_HUMIDITY = "humidity"
SENSOR_SOUND = "sound"
SENSOR_MOTION = "motion"
SENSOR_BATTERY = "battery"
SENSOR_WIFI = "wifi_signal"

SENSOR_TYPES = {
    SENSOR_TEMPERATURE: {
        "name": "Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    SENSOR_HUMIDITY: {
        "name": "Humidity",
        "unit": "%",
        "icon": "mdi:water-percent",
        "device_class": "humidity",
        "state_class": "measurement",
    },
    SENSOR_SOUND: {
        "name": "Sound Level",
        "unit": "dB",
        "icon": "mdi:volume-high",
        "device_class": "sound_level",
        "state_class": "measurement",
    },
    SENSOR_MOTION: {
        "name": "Motion",
        "unit": None,
        "icon": "mdi:motion-sensor",
        "device_class": "motion",
        "state_class": "measurement",
    },
    SENSOR_BATTERY: {
        "name": "Battery",
        "unit": "%",
        "icon": "mdi:battery",
        "device_class": "battery",
        "state_class": "measurement",
    },
    SENSOR_WIFI: {
        "name": "WiFi Signal",
        "unit": "dBm",
        "icon": "mdi:wifi",
        "device_class": "signal_strength",
        "state_class": "measurement",
    },
} 