from functools import lru_cache

from dishka import (
    make_async_container,
    AsyncContainer,
)
from dishka.integrations.taskiq import TaskiqProvider

from .providers import SettingsProvider


@lru_cache(1)
def get_container() -> AsyncContainer:
    container: AsyncContainer = make_async_container(
        TaskiqProvider(),
        SettingsProvider(),
    )

    return container