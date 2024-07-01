from __future__ import annotations
import asyncio
from urllib.parse import urlunparse
from dataclasses import dataclass, field
from typing import Coroutine, Self, Callable, TYPE_CHECKING

# TODO: ugly
if TYPE_CHECKING:
    from .locations import PlayerVillage
    from .driver import Driver


@dataclass(frozen=True)
class Id:
    value: int

    def to_querystr(self) -> str:
        return f"id={self.value}"

    @staticmethod
    def to_querystrs(*args: Id) -> list[str]:
        return [id.to_querystr() for id in args]


@dataclass(frozen=True)
class Link:
    path: str  # e.g. dorf1.php
    queries: list[str] = field(default_factory=list)  # e.g. id=2
    scheme: str = "http"
    netloc: str = "192.168.1.162"
    params: str = ""
    fragment: str = ""

    def to_url(self) -> str:
        return urlunparse(
            [
                self.scheme,
                self.netloc,
                self.path,
                self.params,
                "&".join(self.queries),
                self.fragment,
            ]
        )


SEND_TROOPS: Link = Link("a2b.php")
HOME: Link = Link("dorf1.php")


class StaticScreen:
    village: PlayerVillage
    driver: Driver
    location: Link

    def __init__(self, driver: Driver, village: PlayerVillage, link: Link) -> None:
        self.driver = driver
        self.village = village
        self.location = link

    def __enter__(self) -> Self:
        self.driver.goto(self.village.localize(self.location))
        return self

    def __exit__(self, *_):
        self.driver.goto(HOME)


async def forever(f: Callable[[], float], backoff_base: float = 10, quiet: bool = True):
    fails = 0
    while True:
        try:
            t = f()
            fails = 0
        except Exception as e:
            print(f"Problem: {e}")
            fails += 1
            t = backoff_base * fails
        if not quiet:
            print(f"Waiting for {t}s")
        await asyncio.sleep(t)


async def forever_static(
    f: Callable[[], None], interval: float, backoff_base: float = 10
):
    def fun():
        f()
        return interval

    await forever(fun, backoff_base)


def login(driver: Driver, username: str, password: str) -> Driver:
    driver.goto(HOME)
    driver.retrieve("[name=user]").send_keys(username)
    driver.retrieve("[name=pw]").send_keys(password)
    driver.retrieve("[name=s1]").click()
    return driver


async def keep_logged_in(driver: Driver, username: str, password: str):
    login(driver, username, password)
    await forever_static(lambda: driver.goto(HOME), 60)


async def run_all(*tasks: Coroutine):
    async with asyncio.TaskGroup() as tg:
        for task in tasks:
            tg.create_task(task)


class ResourceException(Exception):
    pass
