from dishka import (
    Provider,
    Scope,
    provide,
)

from core.settings import (
    CommonSettings,
    DevSettings,
)


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def create_broker(self) -> CommonSettings:
        settings = DevSettings()

        return settings