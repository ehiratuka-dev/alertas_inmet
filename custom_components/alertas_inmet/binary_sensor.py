"""DataCoordinator for Alertas INMET."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import ATTR_DESCRICAO, ATTR_ID, ATTR_SEVERIDADE, DOMAIN, MANUFACTURER_TITLE

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """DataCoordinator for Alertas INMET."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([InmetAlertBinarySensor(config_entry, coordinator)])


class InmetAlertBinarySensor(
    CoordinatorEntity[DataUpdateCoordinator[dict[str, Any]]], BinarySensorEntity
):
    """DataCoordinator for Alertas INMET."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: DataUpdateCoordinator[dict[str, Any]],
    ) -> None:
        """DataCoordinator for Alertas INMET."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = config_entry.entry_id
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer=MANUFACTURER_TITLE,
            name=config_entry.title,
        )

    @property
    def is_on(self) -> bool:
        """DataCoordinator for Alertas INMET."""
        _LOGGER.info(self.coordinator.data)
        return not (
            self.coordinator.data is None or self.coordinator.data[ATTR_ID] is None
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """DataCoordinator for Alertas INMET."""
        if self.coordinator.data is None or self.coordinator.data[ATTR_ID] is None:
            return {}

        return {
            ATTR_ID: self.coordinator.data[ATTR_ID],
            ATTR_SEVERIDADE: self.coordinator.data[ATTR_SEVERIDADE],
            ATTR_DESCRICAO: self.coordinator.data[ATTR_DESCRICAO],
        }
