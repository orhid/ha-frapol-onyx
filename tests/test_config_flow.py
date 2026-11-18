from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

from custom_components.frapol_onyx.const import DOMAIN


async def test_form(hass, mock_hub, enable_custom_integrations):
    """Test successful initial configuration."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    assert result["type"] == FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "host": "192.168.1.254",
            "port": 4196,
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Frapol Onyx"

    mock_hub.async_connect.assert_awaited_once()
    mock_hub.async_read_register.assert_awaited_once_with(201)
    mock_hub.async_close.assert_awaited_once()


async def test_cannot_connect(hass, mock_hub, enable_custom_integrations):
    """Test connection failure."""

    mock_hub.async_connect.side_effect = OSError("Connection refused")

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "host": "192.168.1.254",
            "port": 4196,
        },
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"]["base"] == "cannot_connect"


async def test_duplicate_device(hass, mock_hub, enable_custom_integrations):
    """Test duplicate device detection."""

    from pytest_homeassistant_custom_component.common import MockConfigEntry

    existing = MockConfigEntry(
        domain=DOMAIN,
        title="Frapol Onyx",
        unique_id="192.168.1.254:4196:1",
        data={
            "host": "192.168.1.254",
            "port": 4196,
        },
    )

    existing.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "host": "192.168.1.254",
            "port": 4196,
        },
    )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"
