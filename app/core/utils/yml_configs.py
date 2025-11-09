import yaml

from app.core.settings.app import load_settings

_app_setting = load_settings()


def load_yaml_config(name: str) -> dict:
    with open(_app_setting.CONFIGS_PATH / f"{name}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
