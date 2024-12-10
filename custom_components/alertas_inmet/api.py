"""Sample API Client."""

import json
from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any

import requests
from homeassistant.core import HomeAssistant
from shapely.geometry import Point, shape

from .const import _LOGGER, ATTR_DESCRICAO, ATTR_ID, ATTR_SEVERIDADE, URL


class InmetAPI:
    """Sample API Client."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Sample API Client."""
        self.hass = hass

    def search_alerts(self, latitude: float, longitude: float) -> dict[str, Any]:
        """Sample API Client."""
        response = requests.get(URL, timeout=5)
        if response.status_code == HTTPStatus.ACCEPTED:
            data = response.json()
            _LOGGER.debug("Dados obtidos com sucesso.")
            _LOGGER.debug("Mostrando.")
            _LOGGER.info(data)

            for alert in data["hoje"]:
                _LOGGER.debug(f"Testando contra aviso: { alert[ATTR_ID]}")
                if self.is_alert_inside_zone(
                    alert["poligono"], latitude, longitude
                ) and self.is_alert_inside_time(alert["inicio"], alert["fim"]):
                    return {
                        ATTR_ID: alert[ATTR_ID],
                        ATTR_SEVERIDADE: alert[ATTR_SEVERIDADE],
                        ATTR_DESCRICAO: alert[ATTR_DESCRICAO],
                    }

        msg = f"Dados obtidos com sucesso. Codigo: {response.status_code}"
        _LOGGER.debug(msg)

        return {
            "id_aviso": None,
            "severidade": None,
            "descricao": None,
        }

    async def call_alerts(
        self, hass: HomeAssistant, latitude: float, longitude: float
    ) -> dict[str, Any]:
        """Sample API Client."""
        return await hass.async_add_executor_job(
            self.search_alerts, latitude, longitude
        )

    def is_alert_inside_time(self, inicio: str, fim: str) -> bool | None:
        """Sample API Client."""
        formato = "%Y-%m-%d %H:%M"

        inicio_dt = datetime.strptime(inicio, formato).replace(tzinfo=UTC)
        fim_dt = datetime.strptime(fim, formato).replace(tzinfo=UTC)
        agora_dt = datetime.now(tz=UTC)

        _LOGGER.debug(f"{ inicio_dt }, { agora_dt }, { fim_dt }")
        return inicio_dt <= agora_dt <= fim_dt

    def is_alert_inside_zone(
        self, polygon: str, latitude: float, longitude: float
    ) -> bool:
        """Sample API Client."""
        data_polygon = shape(json.loads(polygon))
        data_point = Point(longitude, latitude)
        is_inside = data_point.within(data_polygon)

        _LOGGER.debug(f"is inside { is_inside }")

        return is_inside
