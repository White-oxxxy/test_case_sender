import random
from typing import Any

from dishka.integrations.taskiq import (
    FromDishka,
    inject,
)
from httpx import (
    AsyncClient,
    Response,
    TimeoutException,
)

from .utils import generate_random_strings
from core.settings import CommonSettings
from infra.taskiq.app import taskiq_broker


deleted_count = 0


@taskiq_broker.task(task_name="add_new_texts",)
@inject(patch_module=True)
async def add_new_texts(settings: FromDishka[CommonSettings]) -> None:
    async with AsyncClient() as client:
        items_count: int = random.randint(10, 100)
        items: list[str] = generate_random_strings(n=items_count)

        try:
            response: Response = await client.post(
                url=f"{settings.api.url}/new",
                json={"contents": items},
                timeout=15.0,
            )

            if response.status_code != 201:
                print(f"[SEND FAIL] Статус: {response.status_code}, ответ: {response.text}")

        except TimeoutException:
            print("[SEND FAIL]")


@taskiq_broker.task(task_name="get_last_ten_texts_and_delete")
@inject(patch_module=True)
async def get_last_ten_texts_and_delete(settings: FromDishka[CommonSettings]) -> None:
    global deleted_count

    async with AsyncClient() as client:
        count = 10

        try:
            get_response: Response = await client.get(
                url=f"{settings.api.url}/by_count/{str(count)}",
                timeout=15.0,
            )

            if get_response.status_code == 200:
                data: dict[str, Any] = get_response.json()

                texts: list[dict[str, Any]] = data.get("texts", [])

                for text in texts:
                    oid: str = text.get("oid")

                    try:
                        delete_response: Response = await client.delete(
                            url=f"{settings.api.url}/{oid}",
                            timeout=15.0,
                        )

                        if delete_response.status_code != 204:
                            print(f"[DELETE FAIL] Статус: {delete_response.status_code}, ответ: {delete_response.text}")

                        deleted_count += 1

                    except TimeoutException:
                        print("[DELETE FAIL]")



            else:
                print(f"[GET FAIL] Статус: {get_response.status_code}, ответ: {get_response.text}")

        except TimeoutException:
            print("[GET FAIL]")


@taskiq_broker.task(task_name="print_deleted_texts")
async def print_deleted_texts() -> None:
    global deleted_count

    print(f"Удалено записей: {deleted_count}")

    deleted_count = 0

