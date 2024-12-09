"""DataCoordinator for Alertas INMET."""

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.alertas_inmet.const import (
    _LOGGER,
    ATTR_DESCRICAO,
    ATTR_ID,
    ATTR_SEVERIDADE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


class AlertasInmetCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """DataCoordinator for Alertas INMET."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize DataUpdateCoordinator with custom config for Alertas INMET."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
            update_method=self._async_update_alerts,
            always_update=True,
        )

    async def _async_update_alerts(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        return {
            ATTR_ID: None,
            ATTR_SEVERIDADE: None,
            ATTR_DESCRICAO: None,
        }
