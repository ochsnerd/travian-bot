from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .core import Link, Id
from .driver import Driver

if TYPE_CHECKING:
    from .buildings import Building


@dataclass
class MapLocation:
    x: int
    y: int


@dataclass(frozen=True)
class Village:
    location: MapLocation

    def __str__(self) -> str:
        return f"Village at ({self.location.x}|{self.location.y})"


@dataclass(frozen=True)
class FarmVillage(Village):
    production: int  # total resources per hour


@dataclass(frozen=True)
class VillageId(Id):
    def to_querystr(self) -> str:
        return f"newdid={self.value}"


@dataclass(frozen=True)
class PlayerVillage(Village):
    id: VillageId

    buildings: dict[Building, Id]

    def localize(self, link: Link) -> Link:
        return Link(path=link.path, queries=[self.id.to_querystr()] + link.queries)

    def enter(self, driver: Driver, building: Building) -> Driver:
        driver.goto(
            Link(
                path="/build.php",
                queries=Id.to_querystrs(self.id, self.buildings[building]),
            )
        )
        return driver
