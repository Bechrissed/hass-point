"""Support for Minut Point sensors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfSoundPressure,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    SENSOR_TEMPERATURE,
    SENSOR_HUMIDITY,
    SENSOR_SOUND,
    SENSOR_MOTION,
    SENSOR_BATTERY,
)
from .coordinator import MinutPointDataUpdateCoordinator

@dataclass
class MinutPointSensorEntityDescription(SensorEntityDescription):
    """Class describing Minut Point sensor entities."""

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Minut Point sensor based on a config entry."""
    coordinator: MinutPointDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Wait for first update
    await coordinator.async_config_entry_first_refresh()

    entities = []
    
    # Create sensor entities for each device and sensor type
    for device_id, device_data in coordinator.data.items():
        for sensor_type, sensor_info in SENSOR_TYPES.items():
            if device_data.get(sensor_type) is not None:
                description = MinutPointSensorEntityDescription(
                    key=sensor_type,
                    name=sensor_info["name"],
                    native_unit_of_measurement=sensor_info["unit"],
                    icon=sensor_info["icon"],
                    device_class=sensor_info["device_class"],
                    state_class=sensor_info["state_class"],
                )
                entities.append(
                    MinutPointSensor(
                        coordinator,
                        description,
                        device_id,
                        device_data["name"],
                    )
                )

    async_add_entities(entities)

class MinutPointSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Minut Point sensor."""

    entity_description: MinutPointSensorEntityDescription

    def __init__(
        self,
        coordinator: MinutPointDataUpdateCoordinator,
        description: MinutPointSensorEntityDescription,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the sensor."""
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
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
            
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
            
        return device_data.get(self.entity_description.key) 