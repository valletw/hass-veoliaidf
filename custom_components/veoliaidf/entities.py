""" Veolia IDF entities. """
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorEntity
)
from homeassistant.const import (
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_NAME,
    VOLUME_LITERS
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR,
    ICON,
    API_DATA_TIME
)


class VeoliaIdfEntity(CoordinatorEntity, SensorEntity):
    """ Veolia IDF entity. """

    _attr_native_value = None
    _attr_native_unit_of_measurement = VOLUME_LITERS
    _attr_icon = ICON

    def __init__(self, coordinator, uid: str, device: str, name: str, desc: str):
        super().__init__(coordinator)
        self.entity_id = f"{SENSOR}.{DOMAIN}_{device.lower()}_{name.lower()}"
        self._attr_unique_id = f"{uid}-{name.lower()}"
        self._attr_name = desc
        self._attr_device_info = {
            ATTR_IDENTIFIERS: {(DOMAIN, uid)},
            ATTR_NAME: device,
            ATTR_MANUFACTURER: "Veolia IDF",
        }

    @property
    def extra_state_attributes(self):
        """ Return state attributes. """
        return {
            "last_report": self.coordinator.data[API_DATA_TIME]
        }


class VeoliaIdfSensorIndex(VeoliaIdfEntity):
    """ Veolia IDF index sensor. """
    _attr_state_class = SensorStateClass.TOTAL_INCREASING


class VeoliaIdfSensorConso(VeoliaIdfEntity):
    """ Veolia IDF consumption sensor. """
    _attr_state_class = SensorStateClass.MEASUREMENT
