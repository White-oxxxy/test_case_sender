from dotenv import dotenv_values
from functools import lru_cache
from pathlib import Path

from core.settings.base import (
    RmqSettings,
    OtlpSettings,
    ApiSettings,
    CommonSettings,
)


class ProdSettings(CommonSettings):
    def __init__(self, **data):
        env_file = Path(__file__).resolve().parents[3] / ".prod.env"
        env_data = dotenv_values(env_file)

        data["rmq"] = RmqSettings.model_validate(env_data)
        data["otlp"] = OtlpSettings.model_validate(env_data)
        data["api"] = ApiSettings.model_validate(env_data)

        super().__init__(**data)


@lru_cache(1)
def get_settings() -> ProdSettings:
    return ProdSettings()