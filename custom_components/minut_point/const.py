"""Constants for the Minut Point integration."""
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_SOUND_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    TEMP_CELSIUS,
    SOUND_PRESSURE_DB,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

DOMAIN = "minut_point"
MANUFACTURER = "Minut"

# Configuration
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# URLs
MINUT_BASE_URL = "https://web.minut.com"
MINUT_LOGIN_URL = f"{MINUT_BASE_URL}/login"
MINUT_DASHBOARD_URL = f"{MINUT_BASE_URL}/dashboard"

# Sensor Types
SENSOR_TEMPERATURE = "temperature"
SENSOR_HUMIDITY = "humidity"
SENSOR_SOUND = "sound_level"
SENSOR_BATTERY = "battery_level"
SENSOR_WIFI = "wifi_strength"
SENSOR_MOTION = "motion_detected"
SENSOR_ONLINE = "online"
SENSOR_CHARGING = "charging"
SENSOR_MOUNTED = "mounted"

# Attributes
ATTR_DEVICE_ID = "device_id"
ATTR_DEVICE_NAME = "device_name"

# Units
UNIT_CELSIUS = TEMP_CELSIUS
UNIT_PERCENT = PERCENTAGE
UNIT_DB = SOUND_PRESSURE_DB
UNIT_WIFI = SIGNAL_STRENGTH_DECIBELS_MILLIWATT

# Device Classes
DEVICE_CLASS_TEMPERATURE = SensorDeviceClass.TEMPERATURE
DEVICE_CLASS_HUMIDITY = SensorDeviceClass.HUMIDITY
DEVICE_CLASS_SOUND = SensorDeviceClass.SOUND_PRESSURE
DEVICE_CLASS_BATTERY = SensorDeviceClass.BATTERY
DEVICE_CLASS_WIFI = SensorDeviceClass.SIGNAL_STRENGTH
DEVICE_CLASS_MOTION = BinarySensorDeviceClass.MOTION
DEVICE_CLASS_CONNECTIVITY = BinarySensorDeviceClass.CONNECTIVITY
DEVICE_CLASS_PLUG = BinarySensorDeviceClass.PLUG
DEVICE_CLASS_TAMPER = BinarySensorDeviceClass.TAMPER

# State Classes
STATE_CLASS_MEASUREMENT = SensorStateClass.MEASUREMENT

# Icons
ICON_TEMPERATURE = "mdi:thermometer"
ICON_HUMIDITY = "mdi:water-percent"
ICON_SOUND = "mdi:volume-high"
ICON_BATTERY = "mdi:battery"
ICON_WIFI = "mdi:wifi"
ICON_MOTION = "mdi:motion-sensor"
ICON_ONLINE = "mdi:cloud-check"
ICON_CHARGING = "mdi:battery-charging"
ICON_MOUNTED = "mdi:wall"

SENSOR_TYPES = {
    SENSOR_TEMPERATURE: {
        "name": "Temperature",
        "unit": UNIT_CELSIUS,
        "icon": ICON_TEMPERATURE,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_HUMIDITY: {
        "name": "Humidity",
        "unit": UNIT_PERCENT,
        "icon": ICON_HUMIDITY,
        "device_class": DEVICE_CLASS_HUMIDITY,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_SOUND: {
        "name": "Sound Level",
        "unit": UNIT_DB,
        "icon": ICON_SOUND,
        "device_class": DEVICE_CLASS_SOUND,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_BATTERY: {
        "name": "Battery",
        "unit": UNIT_PERCENT,
        "icon": ICON_BATTERY,
        "device_class": DEVICE_CLASS_BATTERY,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_WIFI: {
        "name": "WiFi Signal",
        "unit": UNIT_WIFI,
        "icon": ICON_WIFI,
        "device_class": DEVICE_CLASS_WIFI,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_MOTION: {
        "name": "Motion",
        "unit": None,
        "icon": ICON_MOTION,
        "device_class": DEVICE_CLASS_MOTION,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_ONLINE: {
        "name": "Online",
        "unit": None,
        "icon": ICON_ONLINE,
        "device_class": None,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_CHARGING: {
        "name": "Charging",
        "unit": None,
        "icon": ICON_CHARGING,
        "device_class": None,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
    SENSOR_MOUNTED: {
        "name": "Mounted",
        "unit": None,
        "icon": ICON_MOUNTED,
        "device_class": None,
        "state_class": STATE_CLASS_MEASUREMENT,
    },
}

# Binary sensor types
BINARY_SENSOR_TYPES = {
    "motion_detected": {
        "name": "Motion",
        "device_class": "motion",
        "icon": "mdi:motion-sensor",
    },
    "online": {
        "name": "Online",
        "device_class": "connectivity",
        "icon": "mdi:cloud-check",
    },
    "charging": {
        "name": "Charging",
        "device_class": "battery_charging",
        "icon": "mdi:battery-charging",
    },
    "mounted": {
        "name": "Mounted",
        "device_class": "tamper",
        "icon": "mdi:shield-check",
    },
} 