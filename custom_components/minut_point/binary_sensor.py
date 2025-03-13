"""Support for Minut Point binary sensors."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_MOTION,
    SENSOR_ONLINE,
    SENSOR_CHARGING,
    SENSOR_MOUNTED,
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_PLUG,
    DEVICE_CLASS_TAMPER,
    ICON_MOTION,
    ICON_ONLINE,
    ICON_CHARGING,
    ICON_MOUNTED,
)
from .coordinator import MinutPointDataUpdateCoordinator

@dataclass
class MinutPointBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing Minut Point binary sensor entities."""

BINARY_SENSOR_TYPES = {
    SENSOR_MOTION: {
        "name": "Motion",
        "icon": ICON_MOTION,
        "device_class": DEVICE_CLASS_MOTION,
    },
    SENSOR_ONLINE: {
        "name": "Online",
        "icon": ICON_ONLINE,
        "device_class": DEVICE_CLASS_CONNECTIVITY,
    },
    SENSOR_CHARGING: {
        "name": "Charging",
        "icon": ICON_CHARGING,
        "device_class": DEVICE_CLASS_PLUG,
    },
    SENSOR_MOUNTED: {
        "name": "Mounted",
        "icon": ICON_MOUNTED,
        "device_class": DEVICE_CLASS_TAMPER,
    },
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Minut Point binary sensors based on a config entry."""
    coordinator: MinutPointDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Wait for first update
    await coordinator.async_config_entry_first_refresh()

    entities = []

    # Create binary sensor entities for each device
    for device_id, device_data in coordinator.data.items():
        metrics = device_data.get("metrics", {})
        for sensor_type, sensor_info in BINARY_SENSOR_TYPES.items():
            if sensor_type in metrics:
                description = MinutPointBinarySensorEntityDescription(
                    key=sensor_type,
                    name=sensor_info["name"],
                    icon=sensor_info["icon"],
                    device_class=sensor_info["device_class"],
                )
                entities.append(
                    MinutPointBinarySensor(
                        coordinator,
                        description,
                        device_id,
                        device_data["name"],
                    )
                )

    async_add_entities(entities)

class MinutPointBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Minut Point binary sensor."""

    entity_description: MinutPointBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: MinutPointDataUpdateCoordinator,
        description: MinutPointBinarySensorEntityDescription,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Minut",
            model="Point",
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.coordinator.data is None:
            return None

        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None or "metrics" not in device_data:
            return None

        metrics = device_data["metrics"]
        return metrics.get(self.entity_description.key, False) 