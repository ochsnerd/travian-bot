from __future__ import annotations
from dataclasses import dataclass
from typing import Self

from .driver import Driver, By
from .core import HOME, Id, upgrade
from .locations import PlayerVillage


@dataclass(frozen=True)
class Resource:
    name: str
    id_in_market: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


Lumber = Resource("Lumber", "r1")
Clay = Resource("Clay", "r2")
Iron = Resource("Iron", "r3")
Crop = Resource("Crop", "r4")


def get_resource_production(
    driver: Driver, village: PlayerVillage, kind: Resource
) -> int:
    driver.goto(village.localize(HOME))
    return int(
        driver.retrieve(
            f"//td[@class='res' and contains(text(),'{kind.name}')]", By.XPATH
        )
        .find_element(By.XPATH, "./following-sibling::td[@class='num']")
        .text
    )


class ResourceScreen:
    village: PlayerVillage
    driver: Driver
    resId: Id

    def __init__(self, driver: Driver, village: PlayerVillage, resId: Id) -> None:
        self.driver = driver
        self.village = village
        self.resId = resId

    def __enter__(self) -> Self:
        self.village.enter_res_field(self.driver, self.resId)
        return self

    def __exit__(self, *_):
        self.driver.goto(HOME)

    def upgrade(self) -> None:
        upgrade(self.driver, f"Res at {self.resId.value}", str(self.village))
