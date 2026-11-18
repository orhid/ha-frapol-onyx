from unittest.mock import AsyncMock, patch

import pytest

from custom_components.frapol_onyx.const import DOMAIN
from pytest_homeassistant.common import MockConfigEntry


@pytest.fixture
def mock_hub():
    """Mock Frapol Modbus hub."""

    with patch("custom_components.frapol_onyx.config_flow.FrapolHub") as mock:
        hub = mock.return_value

        hub.async_connect = AsyncMock()
        hub.async_close = AsyncMock()
        hub.async_read_register = AsyncMock(return_value=215)
        hub.async_write_register = AsyncMock()

        yield hub


@pytest.fixture
def mock_config_entry():
    """Create a Frapol configuration entry."""

    return MockConfigEntry(
        domain=DOMAIN,
        title="Frapol Onyx",
        unique_id="172.27.8.10:4196:1",
        data={
            "host": "172.27.8.10",
            "port": 4196,
        },
        options={
            "slave": 1,
            "timeout": 5,
            "retries": 3,
            "scan_interval": 30,
        },
    )
