""" Config flow setup. """
from os.path import exists
from typing import Optional, Dict, Any
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .api import VeoliaIdfApiClient
from .const import (
    CONF_LOGIN,
    CONF_PASS,
    CONF_WEBDRIVER,
    CONF_INSTALL,
    DEFAULT_INSTALL,
    DOMAIN
)


SCHEMA = vol.Schema({
    vol.Required(CONF_LOGIN, default=""): str,
    vol.Required(CONF_PASS, default=""): str,
    vol.Required(CONF_WEBDRIVER, default=""): str,
    vol.Optional(CONF_INSTALL, default=DEFAULT_INSTALL): str
})


async def _validate_credentials(login: str, password: str, driver: str) -> bool:
    """ Validate credentials by fetching data. """
    try:
        client = VeoliaIdfApiClient(login, password, driver)
        data = await client.async_fetch_data()
        return len(data) != 0
    except Exception:
        pass
    return False


class VeoliaIdfFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """ Config flow handler for Veolia IDF. """

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """ Manage user flow. """
        errors: Dict[str, str] = {}
        if user_input is not None:
            # Check if webdriver exists.
            if not exists(user_input[CONF_WEBDRIVER]):
                errors["base"] = "invalid_path"
            # Check credentials.
            valid = await _validate_credentials(
                user_input[CONF_LOGIN], user_input[CONF_PASS],
                user_input[CONF_WEBDRIVER]
            )
            if not valid:
                errors["base"] = "auth"
            if not errors:
                # Input validated, configuration done, create entry.
                return self.async_create_entry(
                    title=user_input[CONF_LOGIN],
                    data=user_input
                )
        # No user input, ask parameters.
        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """ Get options flow. """
        return VeoliaIdfOptionsFlowHandler(config_entry)


class VeoliaIdfOptionsFlowHandler(config_entries.OptionsFlow):
    """ Options flow handler for Veolia IDF. """

    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None):
        """ Manage the options. """
        errors: Dict[str, str] = {}
        if user_input is not None:
            # Check if webdriver exists.
            if not exists(user_input[CONF_WEBDRIVER]):
                errors["base"] = "invalid_path"
            # Check credentials.
            valid = await _validate_credentials(
                user_input[CONF_LOGIN], user_input[CONF_PASS],
                user_input[CONF_WEBDRIVER]
            )
            if not valid:
                errors["base"] = "auth"
            if not errors:
                # Input validated, configuration update done, create entry.
                return self.async_create_entry(
                    title=self.config_entry.data.get(CONF_LOGIN),
                    data=user_input
                )
        return self.async_show_form(
            step_id="init",
            data_schema=SCHEMA,
            errors=errors
        )
