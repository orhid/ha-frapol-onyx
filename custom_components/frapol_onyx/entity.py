from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import FrapolCoordinator


class FrapolEntity(CoordinatorEntity[FrapolCoordinator]):
    """Base class for Frapol entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        unique_id: str,
    ) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = unique_id

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.device_id)},
            name="Frapol Onyx",
            manufacturer=MANUFACTURER,
            model=MODEL,
        )
