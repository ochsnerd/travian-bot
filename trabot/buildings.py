from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from .core import HOME
from .driver import Driver

if TYPE_CHECKING:
    from .locations import PlayerVillage


@dataclass(frozen=True)
class Building:
    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


Stable = Building("Stable")
Barracks = Building("Barracks")


class BuildingScreen:
    village: PlayerVillage
    driver: Driver
    building: Building

    def __init__(
        self, driver: Driver, village: PlayerVillage, building: Building
    ) -> None:
        self.driver = driver
        self.village = village
        self.building = building

    def __enter__(self) -> Self:
        self.village.enter(self.driver, self.building)
        return self

    def __exit__(self, *_):
        self.driver.goto(HOME)
