from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.frapol_onyx.const import DOMAIN


@pytest.fixture
def mock_hub():
    """Mock Frapol Modbus hub."""

    with (
        patch("custom_components.frapol_onyx.config_flow.FrapolHub") as config_flow_hub,
        patch("custom_components.frapol_onyx.FrapolHub") as setup_hub,
    ):
        # Hub used by the initial configuration flow
        flow_instance = config_flow_hub.return_value
        flow_instance.async_connect = AsyncMock()
        flow_instance.async_close = AsyncMock()
        flow_instance.async_read_register = AsyncMock(return_value=215)
        flow_instance.async_write_register = AsyncMock()

        # Hub used by Home Assistant when setting up the config entry
        setup_instance = setup_hub.return_value
        setup_instance.async_connect = AsyncMock()
        setup_instance.async_close = AsyncMock()
        setup_instance.async_read_register = AsyncMock(return_value=215)
        setup_instance.async_write_register = AsyncMock()

        yield flow_instance


@pytest.fixture
def mock_config_entry():
    """Create a Frapol configuration entry."""

    return MockConfigEntry(
        domain=DOMAIN,
        title="Frapol Onyx",
        unique_id="192.168.1.254:4196:1",
        data={
            "host": "192.168.1.254",
            "port": 4196,
        },
        options={
            "slave": 1,
            "timeout": 5,
            "retries": 3,
            "scan_interval": 30,
        },
    )
