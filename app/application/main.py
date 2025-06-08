import asyncio

from infra.taskiq.app import taskiq_broker


async def schedule_tasks():
    from infra.taskiq.sender_tasks import (
        add_new_texts,
        get_last_ten_texts_and_delete,
    )

    while True:
        await add_new_texts.kiq()
        await asyncio.sleep(1)
        await get_last_ten_texts_and_delete.kiq()
        await asyncio.sleep(5)


async def schedule_stats():
    from infra.taskiq.sender_tasks import print_deleted_texts

    while True:
        await asyncio.sleep(10)
        await print_deleted_texts.kiq()


async def main():
    await taskiq_broker.startup()

    try:
        await asyncio.gather(schedule_tasks(), schedule_stats())

    finally:
        await taskiq_broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())