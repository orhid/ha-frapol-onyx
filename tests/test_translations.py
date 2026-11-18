import json
from pathlib import Path

from custom_components.frapol_onyx.definitions import SENSORS


BASE_PATH = Path(__file__).parent.parent / "custom_components" / "frapol_onyx"


def load_translation(language):
    """Load a translation file."""

    path = BASE_PATH / "translations" / f"{language}.json"

    with path.open(encoding="utf-8") as file:
        return json.load(file)


def test_all_sensors_have_translations():
    """Ensure every sensor has EN and PL names."""

    for language in ("en", "pl"):
        translations = load_translation(language)

        entities = translations["entity"]["sensor"]

        for sensor in SENSORS:
            assert sensor.key in entities, (
                f"Missing {language} translation: {sensor.key}"
            )

            assert entities[sensor.key].get("name"), (
                f"Missing {language} name: {sensor.key}"
            )


def test_power_switch_has_translations():
    """Ensure power switch has EN and PL names."""

    for language in ("en", "pl"):
        translations = load_translation(language)

        assert translations["entity"]["switch"]["unit_power"]["name"]
