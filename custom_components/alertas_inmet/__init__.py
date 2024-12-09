"""Sample API Client."""

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE, CONF_ZONE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import InmetAPI
from .const import _LOGGER, DEFAULT_SCAN_INTERVAL, DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Sample API Client."""
    inmet_api = InmetAPI(hass)

    async def async_update_alerts() -> dict[str, Any]:
        if (zone := hass.states.get(config_entry.data[CONF_ZONE])) is None:
            msg = f"Zone '{config_entry.data[CONF_ZONE]}' not found"
            raise UpdateFailed(msg)

        return await inmet_api.call_alerts(
            hass,
            latitude=zone.attributes[ATTR_LATITUDE],
            longitude=zone.attributes[ATTR_LONGITUDE],
        )

    coordinator: DataUpdateCoordinator[dict[str, Any]] = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{config_entry.data[CONF_ZONE]}",
        update_interval=DEFAULT_SCAN_INTERVAL,
        update_method=async_update_alerts,
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Sample API Client."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    if unload_ok:
        del hass.data[DOMAIN][config_entry.entry_id]
    return unload_ok
