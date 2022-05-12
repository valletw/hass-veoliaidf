""" Constants for veoliaidf. """
from datetime import timedelta
from homeassistant.const import (
    CONF_USERNAME, CONF_PASSWORD
)

# Base constants.
NAME = "Veolia IDF"
DOMAIN = "veoliaidf"
DOMAIN_DATA = f"{DOMAIN}_data"
ATTRIBUTION = "Data provided by Veolia IDF website (French water provider)."
ICON = "mdi:water"

# Platforms.
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options.
CONF_LOGIN = CONF_USERNAME
CONF_PASS = CONF_PASSWORD
CONF_WEBDRIVER = "webdriver"
CONF_INSTALL = "install"

# Defaults.
DEFAULT_INSTALL = "apk add"
SCAN_INTERVAL = timedelta(hours=4)
CONNECTION_TIMEOUT = timedelta(minutes=10)

# API data field.
API_DATA_TIME = "time"
API_DATA_TOTAL = "total_l"
API_DATA_DAILY = "daily_l"
