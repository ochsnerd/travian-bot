from __future__ import annotations
import asyncio
from urllib.parse import urlunparse
from dataclasses import dataclass, field
from typing import Coroutine, Self, Callable, TYPE_CHECKING

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

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


def login(driver: Driver, username: str, password: str) -> Driver:
    driver.goto(HOME)
    driver.retrieve("[name=user]").send_keys(username)
    driver.retrieve("[name=pw]").send_keys(password)
    driver.retrieve("[name=s1]").click()
    return driver


async def run_all(*tasks: Coroutine):
    async with asyncio.TaskGroup() as tg:
        for task in tasks:
            tg.create_task(task)


class TravianBotException(Exception):
    pass


class ResourceException(TravianBotException):
    pass


class BuildingException(TravianBotException):
    pass


class UnexpectedBuildingException(BuildingException):
    pass


class NoBuildingThereException(BuildingException):
    pass


class PlotNotEmptyException(BuildingException):
    pass


class PremiumFeatureException(TravianBotException):
    pass


def upgrade(driver: Driver, what: str, where: str) -> None:
    # TODO: Check nicca solution in discord to extract time
    try:
        build(driver.retrieve("a.build"))
    except NoSuchElementException:
        raise BuildingException(f"Cannot upgrade {what} in {where}.")
    except PremiumFeatureException:
        raise BuildingException(f"No free workers to upgrade {what} in {where}.")


def build(link: WebElement) -> None:
    if "master builder" in link.text:
        raise PremiumFeatureException("Master builder")
    link.click()
