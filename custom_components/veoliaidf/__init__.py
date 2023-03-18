""" Veolia IDF integration. """
import asyncio
import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)

from .api import VeoliaIdfApiClient
from .const import (
    DOMAIN,
    SENSOR,
    SCAN_INTERVAL,
    CONF_LOGIN,
    CONF_PASS,
    CONF_WEBDRIVER,
    CONF_INSTALL,
    API_DATA_TIME
)


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """ Setup integration from YAML (not supported). """
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Setup integration from UI. """
    # Setup data if not registered.
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.debug("Create integration")
    # Initialise integration with user configuration.
    login = entry.data.get(CONF_LOGIN)
    password = entry.data.get(CONF_PASS)
    driver = entry.data.get(CONF_WEBDRIVER)
    # FIXME: remove system dependencies installation.
    install = entry.data.get(CONF_INSTALL)
    try:
        os.system(f"{install} firefox-esr")
    except BaseException as exc:
        _LOGGER.error("Dependencies installation failed: %s", exc)
        return
    coordinator = VeoliaIdfCoordinator(hass, login, password, driver)
    hass.data[DOMAIN][entry.entry_id] = coordinator
    # Get first data.
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady
    # Forward the setup to the sensor platform.
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(entry, SENSOR)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Unload a config entry. """
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, SENSOR)]
        )
    )
    # Remove config entry from domain.
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug("Delete integration")
    return unload_ok


class VeoliaIdfCoordinator(DataUpdateCoordinator):
    """ Veolia IDF coordinator. """

    def __init__(self, hass: HomeAssistant, login: str, password: str, driver: str):
        super().__init__(
            hass, _LOGGER, name=login,
            update_interval=SCAN_INTERVAL,
            update_method=self.fetch_data
        )
        self._client = VeoliaIdfApiClient(login, password, driver)

    async def fetch_data(self) -> dict:
        """ Fetch data from Veolia IDF website. """
        # Fetch data and sort by date.
        try:
            data = await self._client.async_fetch_data()
        except Exception as exc:
            raise UpdateFailed from exc
        data_sort = sorted(data, key=lambda d: d[API_DATA_TIME])
        # Get most recent value.
        return data_sort[-1]
