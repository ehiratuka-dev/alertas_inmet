"""DataCoordinator for Alertas INMET."""

from typing import Any

import voluptuous as vol
from homeassistant.components.zone.const import DOMAIN as ZONE_DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_ZONE
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import CONF_ENTRY_TITLE, CONFIG_USER_STEP, DOMAIN


class AlertasInmetConfigFlow(ConfigFlow, domain=DOMAIN):
    """DataCoordinator for Alertas INMET."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """DataCoordinator for Alertas INMET."""
        if user_input is None:
            return self.async_show_form(
                step_id=CONFIG_USER_STEP,
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_ZONE): EntitySelector(
                            EntitySelectorConfig(domain=ZONE_DOMAIN),
                        ),
                    }
                ),
            )

        identifier = user_input[CONF_ZONE]
        state = self.hass.states.get(identifier)
        if state is None:
            return self.async_create_entry(
                title=f"{ CONF_ENTRY_TITLE }", data=user_input
            )

        title = f"{ CONF_ENTRY_TITLE } em { state.name }"

        await self.async_set_unique_id(identifier)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=title, data=user_input)
