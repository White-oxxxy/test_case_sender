from dishka import AsyncContainer
from dishka.integrations.taskiq import setup_dishka
from taskiq_aio_pika import AioPikaBroker

from .middlewares import MetricsMiddleWares
from di import get_container
from core.settings.dev import get_settings


settings = get_settings()

def create_broker() -> AioPikaBroker:
    broker = AioPikaBroker(
        url=settings.rmq.rabbit_broker_url,
        queue_name="sender-queue",
    ).with_middlewares(MetricsMiddleWares())

    container: AsyncContainer = get_container()

    setup_dishka(container=container, broker=broker)

    return broker

taskiq_broker: AioPikaBroker = create_broker()


