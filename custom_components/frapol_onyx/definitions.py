from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature


@dataclass(frozen=True)
class SensorDefinition:
    """Definition of a Frapol sensor."""

    key: str
    address: int
    signed: bool = False
    scale: float = 1.0
    offset: float = 0.0
    precision: int = 0
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None
    unit: str | None = None


SENSORS = (
    SensorDefinition(
        key="comfort_temperature",
        address=201,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
    SensorDefinition(
        key="outdoor_temperature",
        address=202,
        signed=True,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
    SensorDefinition(
        key="leading_temperature",
        address=203,
        signed=True,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
    SensorDefinition(
        key="intake_temperature",
        address=206,
        signed=True,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
    SensorDefinition(
        key="exhaust_temperature",
        address=207,
        signed=True,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
    SensorDefinition(
        key="supply_temperature",
        address=208,
        signed=True,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
    SensorDefinition(
        key="extract_temperature",
        address=209,
        signed=True,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
    ),
)

POWER_REGISTER = 59
