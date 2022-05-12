""" Veolia IDF API Client. """
import asyncio
import logging
import traceback
from datetime import datetime
from typing import TypedDict, List
import pyveoliaidf

from .const import (
    API_DATA_TIME,
    API_DATA_TOTAL,
    API_DATA_DAILY,
    CONNECTION_TIMEOUT
)


_LOGGER = logging.getLogger(__name__)


class VeoliaIdfApiData(TypedDict):
    """ Veolia IDF API data. """
    API_DATA_TIME: datetime
    API_DATA_TOTAL: int
    API_DATA_DAILY: int


class VeoliaIdfApiClient:
    """ Veolia IDF API Client. """

    def __init__(self, login: str, password: str, driver: str):
        self._login = login
        self._password = password
        self._driver = driver

    async def async_fetch_data(self) -> List[VeoliaIdfApiData]:
        """ Fetch data from Veolia IDF website. """
        _LOGGER.debug("Fetching new data")
        export: List[VeoliaIdfApiData] = []
        try:
            # Connect to website.
            client = pyveoliaidf.Client(
                self._login, self._password, self._driver,
                int(CONNECTION_TIMEOUT.total_seconds()), "/tmp"
            )
            await asyncio.gather(
                asyncio.to_thread(client.update)
            )
            # Format data.
            for data in client.data():
                _LOGGER.debug("data=%s", data)
                export.append({
                    API_DATA_TIME: datetime.fromisoformat(data["time"]),
                    API_DATA_TOTAL: int(data["total_liter"]),
                    API_DATA_DAILY: int(data["daily_liter"])
                })
            _LOGGER.debug("Fetching new data succeed")
        except Exception as exc:
            _LOGGER.error("Fetch new data failed: %s", exc)
            _LOGGER.error(traceback.format_exc())
            raise ConnectionError from exc
        return export
