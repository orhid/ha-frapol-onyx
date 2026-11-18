from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .definitions import SENSORS
from .entity import FrapolEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Frapol sensors."""

    coordinator = entry.runtime_data

    async_add_entities(FrapolSensor(coordinator, definition) for definition in SENSORS)


class FrapolSensor(FrapolEntity, SensorEntity):
    """Representation of a Frapol sensor."""

    def __init__(
        self,
        coordinator,
        definition,
    ) -> None:
        super().__init__(
            coordinator,
            definition.key,
        )

        self.entity_description = SensorEntityDescription(
            key=definition.key,
            translation_key=definition.key,
            device_class=definition.device_class,
            state_class=definition.state_class,
            native_unit_of_measurement=definition.unit,
            suggested_display_precision=definition.precision,
        )

    @property
    def native_value(self):
        """Return sensor value."""
        return self.coordinator.data.get(self.entity_description.key)
