""" Veolia IDF sensors. """
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry


from .const import (
    DOMAIN,
    CONF_LOGIN,
    API_DATA_TOTAL,
    API_DATA_DAILY
)
from .entities import (
    VeoliaIdfSensorIndex,
    VeoliaIdfSensorConso
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """ Setup sensor platform. """
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devname = entry.data.get(CONF_LOGIN).split("@")[0]
    async_add_devices([
        VeoliaIdfSensorTotal(coordinator, entry.entry_id, devname),
        VeoliaIdfSensorDaily(coordinator, entry.entry_id, devname)
    ])


class VeoliaIdfSensorTotal(VeoliaIdfSensorIndex):
    """ Veolia IDF index total. """

    def __init__(self, coordinator, uid: str, device: str):
        super().__init__(coordinator, uid, device, "total", "Index")

    @property
    def native_value(self) -> int:
        """ Get value. """
        return self.coordinator.data[API_DATA_TOTAL]


class VeoliaIdfSensorDaily(VeoliaIdfSensorConso):
    """ Veolia IDF daily consumption. """

    def __init__(self, coordinator, uid: str, device: str):
        super().__init__(coordinator, uid, device, "daily", "Jour")

    @property
    def native_value(self) -> int:
        """ Get value. """
        return self.coordinator.data[API_DATA_DAILY]
