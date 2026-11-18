from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    PLATFORMS,
    CONF_HOST,
    CONF_PORT,
    CONF_SLAVE,
    CONF_TIMEOUT,
    CONF_RETRIES,
    CONF_SCAN_INTERVAL,
    DEFAULT_SLAVE,
    DEFAULT_TIMEOUT,
    DEFAULT_RETRIES,
    DEFAULT_SCAN_INTERVAL,
)
from .hub import FrapolHub
from .coordinator import FrapolCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Set up Frapol Onyx."""

    options = entry.options

    hub = FrapolHub(
        host=entry.data[CONF_HOST],
        port=entry.data[CONF_PORT],
        slave=options.get(CONF_SLAVE, DEFAULT_SLAVE),
        timeout=options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
        retries=options.get(CONF_RETRIES, DEFAULT_RETRIES),
    )

    entry.async_on_unload(hub.async_close)

    await hub.async_connect()

    coordinator = FrapolCoordinator(
        hass,
        hub,
        options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        entry.unique_id,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Frapol Onyx."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
