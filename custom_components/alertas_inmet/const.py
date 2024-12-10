"""Sample API Client."""

import logging
from datetime import timedelta

from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "alertas_inmet"
PLATFORMS = [Platform.BINARY_SENSOR]
CONFIG_USER_STEP = "user"

DEFAULT_ICON = "mdi:alert"
DEFAULT_RADIUS = 500.0
DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

CONF_ENTRY_TITLE = "Alertas Meteorológicos INMET"
DEVICE_TITLE = "Alerta INMET"
MANUFACTURER_TITLE = "INMET"

URL = "https://apiprevmet3.inmet.gov.br/avisos/ativos"

ATTR_ID = "id_aviso"
ATTR_SEVERIDADE = "severidade_ids"
ATTR_DESCRICAO = "descricao"
