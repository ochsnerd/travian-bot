from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .core import (
    BuildingException,
    Link,
    Id,
    NoBuildingThereException,
    PlotNotEmptyException,
    UnexpectedBuildingException,
)
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
    production: int  # total resources per hour, all types added


@dataclass(frozen=True)
class VillageId(Id):
    def to_querystr(self) -> str:
        return f"newdid={self.value}"


@dataclass(frozen=True)
class PlayerVillage(Village):
    id: VillageId
    name: str

    buildings: dict[Building, Id]

    def localize(self, link: Link) -> Link:
        return Link(path=link.path, queries=[self.id.to_querystr()] + link.queries)

    def enter(self, driver: Driver, id: Id) -> Driver:
        driver.goto(
            Link(
                path="/build.php",
                queries=Id.to_querystrs(self.id, id),
            )
        )
        return driver

    def enter_building(self, driver: Driver, building: Building) -> Driver:
        self.enter(driver, self.buildings[building])

        # check that correct building was entered
        if not str(building) in (text := driver.retrieve("h1").text):
            if "new building" in text:
                raise NoBuildingThereException()
            raise UnexpectedBuildingException(
                f"{self}: Entered {text} insted of {building}."
            )

        return driver

    def enter_res_field(self, driver: Driver, resId: Id) -> Driver:
        assert 1 <= resId.value <= 18
        return self.enter(driver, resId)

    def enter_empty_plot(self, driver: Driver, plotId: Id) -> Driver:
        self.enter(driver, plotId)

        # check that no building exists there
        if not "new building" in (text := driver.retrieve("h1").text):
            raise PlotNotEmptyException(
                f"{self}: Entered {text} insted of empty plot {plotId.value}."
            )

        return driver

    def __str__(self) -> str:
        return self.name
