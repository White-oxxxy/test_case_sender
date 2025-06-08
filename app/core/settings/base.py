from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import Field


class RmqSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    username: str = Field(alias="RMQ_USERNAME", default="RMQ_USERNAME")
    password: str = Field(alias="RMQ_PASSWORD", default="RMQ_PASSWORD")
    host: str = Field(alias="RMQ_HOST", default="localhost")
    port: int = Field(alias="RMQ_PORT", default=5672)

    @property
    def rabbit_broker_url(self) -> str:
        return rf"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"


class OtlpSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    host: str = Field(alias="OTLP_HOST", default="localhost")
    port: int = Field(alias="OTLP_PORT", default="4317")

    @property
    def otlp_url(self) -> str:
        return rf"http://{self.host}:{self.port}"


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    url: str = Field(alias="API_URL", default="http://localhost:8080")


class CommonSettings(BaseSettings):
    rmq: RmqSettings
    otlp: OtlpSettings
    api: ApiSettings