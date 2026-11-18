import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed
from pymodbus.exceptions import ModbusException

from custom_components.frapol_onyx.coordinator import (
    FrapolCoordinator,
)


class MockHub:
    """Mock Frapol Modbus communication."""

    def __init__(self, values):
        self.values = values

    async def async_read_register(self, address):
        if address not in self.values:
            raise ModbusException(f"Register {address} unavailable")

        return self.values[address]


@pytest.mark.asyncio
async def test_temperature_decoding(hass):
    """Test temperature register decoding."""

    values = {
        201: 215,
        202: 65526,
        203: 225,
        206: 180,
        207: 190,
        208: 210,
        209: 200,
        59: 1,
    }

    hub = MockHub(values)

    coordinator = FrapolCoordinator(
        hass,
        hub,
        30,
        device_id="test-frapol-onyx",
    )

    data = await coordinator._async_update_data()

    assert data["comfort_temperature"] == 215
    assert data["outdoor_temperature"] == -1.0
    assert data["leading_temperature"] == 22.5
    assert data["intake_temperature"] == 18.0
    assert data["exhaust_temperature"] == 19.0
    assert data["supply_temperature"] == 21.0
    assert data["extract_temperature"] == 20.0

    assert data["power"] is True


@pytest.mark.asyncio
async def test_power_off(hass):
    """Test power register interpretation."""

    values = {
        201: 215,
        202: 0,
        203: 0,
        206: 0,
        207: 0,
        208: 0,
        209: 0,
        59: 0,
    }

    coordinator = FrapolCoordinator(
        hass,
        MockHub(values),
        30,
        device_id="test-frapol-onyx",
    )

    data = await coordinator._async_update_data()

    assert data["power"] is False


@pytest.mark.asyncio
async def test_modbus_failure(hass):
    """Test communication failure handling."""

    hub = MockHub({})

    coordinator = FrapolCoordinator(
        hass,
        hub,
        30,
        device_id="test-frapol-onyx",
    )

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
