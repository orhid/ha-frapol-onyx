import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from pymodbus.exceptions import ModbusException

from .const import DOMAIN
from .definitions import POWER_REGISTER, SENSORS
from .hub import FrapolHub

_LOGGER = logging.getLogger(__name__)


class FrapolCoordinator(DataUpdateCoordinator):
    """Coordinate Frapol Onyx data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        hub: FrapolHub,
        scan_interval: int,
        device_id,
    ) -> None:
        self.hub = hub
        self.device_id = device_id

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from the Frapol unit."""
        data = {}

        try:
            for sensor in SENSORS:
                raw_value = await self.hub.async_read_register(sensor.address)

                if sensor.signed and raw_value >= 32768:
                    raw_value -= 65536

                value = (raw_value * sensor.scale) + sensor.offset

                data[sensor.key] = round(
                    value,
                    sensor.precision,
                )

            # Power status
            data["power"] = (await self.hub.async_read_register(POWER_REGISTER)) == 1

            return data

        except (ModbusException, ConnectionError, OSError) as err:
            raise UpdateFailed(f"Error communicating with Frapol Onyx: {err}") from err
