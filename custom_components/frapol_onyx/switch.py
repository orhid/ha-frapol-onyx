from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from pymodbus.exceptions import ModbusException

from .const import DOMAIN
from .definitions import POWER_REGISTER
from .entity import FrapolEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Frapol switches."""

    coordinator = entry.runtime_data

    async_add_entities([
        FrapolPowerSwitch(coordinator),
    ])


class FrapolPowerSwitch(FrapolEntity, SwitchEntity):
    """Frapol unit power switch."""


    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            "unit_power",
        )
        self._attr_translation_key = "unit_power"


    @property
    def is_on(self) -> bool:
        """Return power state."""
        return self.coordinator.data.get("power", False)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the unit on."""
        await self.coordinator.hub.async_write_register(
            POWER_REGISTER,
            1,
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the unit off."""
        await self.coordinator.hub.async_write_register(
            POWER_REGISTER,
            0,
        )
        await self.coordinator.async_request_refresh()
        
