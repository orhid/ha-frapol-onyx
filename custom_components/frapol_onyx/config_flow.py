import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_SLAVE,
    CONF_TIMEOUT,
    CONF_RETRIES,
    CONF_SCAN_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_SLAVE,
    DEFAULT_TIMEOUT,
    DEFAULT_RETRIES,
    DEFAULT_SCAN_INTERVAL,
)
from .hub import FrapolHub


class FrapolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Frapol Onyx configuration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle initial setup."""

        errors = {}

        if user_input is not None:
            hub = FrapolHub(
                host=user_input[CONF_HOST],
                port=user_input[CONF_PORT],
                slave=DEFAULT_SLAVE,
                timeout=DEFAULT_TIMEOUT,
                retries=DEFAULT_RETRIES,
            )

            try:
                await hub.async_connect()
                await hub.async_read_register(201)

            except Exception:
                errors["base"] = "cannot_connect"

            finally:
                await hub.async_close()

            if not errors:
                unique_id = (
                    f"{user_input[CONF_HOST]}:"
                    f"{user_input[CONF_PORT]}"
                    f":{DEFAULT_SLAVE}"
                )

                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="Frapol Onyx",
                    data=user_input,
                )

        schema = vol.Schema({
            vol.Required(
                CONF_HOST,
                default="192.168.1.254",
            ): str,
            vol.Required(
                CONF_PORT,
                default=DEFAULT_PORT,
            ): vol.All(int, vol.Range(min=1, max=65535)),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return FrapolOptionsFlow()


class FrapolOptionsFlow(config_entries.OptionsFlowWithReload):
    """Handle advanced configuration options."""

    async def async_step_init(self, user_input=None):
        """Manage advanced options."""

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        options = self.config_entry.options

        schema = vol.Schema({
            vol.Optional(
                CONF_SLAVE,
                default=options.get(CONF_SLAVE, DEFAULT_SLAVE),
            ): vol.All(int, vol.Range(min=1, max=247)),

            vol.Optional(
                CONF_TIMEOUT,
                default=options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
            ): vol.All(int, vol.Range(min=1, max=60)),

            vol.Optional(
                CONF_RETRIES,
                default=options.get(CONF_RETRIES, DEFAULT_RETRIES),
            ): vol.All(int, vol.Range(min=0, max=10)),

            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=options.get(
                    CONF_SCAN_INTERVAL,
                    DEFAULT_SCAN_INTERVAL,
                ),
            ): vol.All(int, vol.Range(min=5, max=3600)),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
