from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .core import (
    HOME,
    BuildingException,
    Id,
    NoBuildingThereException,
    PremiumFeatureException,
    build,
    upgrade,
)
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


RallyPoint = Building("Rally Point")
Stable = Building("Stable")
Barracks = Building("Barracks")
Workshop = Building("Workshop")
Academy = Building("Academy")
BlackSmith = Building("Blacksmith")
Armoury = Building("Armoury")
HorseDrinkingTrough = Building("Horse Drinking Trough")
HerosMansion = Building("Hero's Mansion")
Wall = Building("Wall")

Sawmill = Building("Sawmill")
Brickyard = Building("Brickyard")
IronFoundry = Building("Iron Foundry")
GrainMill = Building("Grain Mill")
Bakery = Building("Bakery")
MarketPlace = Building("Marketplace")
Granary = Building("Granary")
Warehouse = Building("Warehouse")

MainBuilding = Building("Main Building")
Embassy = Building("Embassy")
Residence = Building("Residence")

ALL_BUILDINGS = {
    str(b): b
    for b in [
        RallyPoint,
        Stable,
        Barracks,
        Academy,
        BlackSmith,
        Armoury,
        HorseDrinkingTrough,
        Wall,
        Sawmill,
        Brickyard,
        IronFoundry,
        GrainMill,
        Bakery,
        MarketPlace,
        Granary,
        Warehouse,
        MainBuilding,
        HerosMansion,
        Embassy,
        Residence,
    ]
}


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
        self.village.enter_building(self.driver, self.building)
        return self

    def __exit__(self, *_):
        self.driver.goto(HOME)

    def upgrade(self) -> None:
        upgrade(self.driver, str(self.building), str(self.village))


class EmptyPlotScreen:
    village: PlayerVillage
    driver: Driver
    plotId: Id

    def __init__(self, driver: Driver, village: PlayerVillage, plotId: Id) -> None:
        self.driver = driver
        self.village = village
        self.plotId = plotId

    def __enter__(self) -> Self:
        self.village.enter_empty_plot(self.driver, self.plotId)
        return self

    def __exit__(self, *_):
        self.driver.goto(HOME)

    def build(self, building: Building) -> None:
        try:
            build(
                self.driver.retrieve(
                    # Bug: This will match "Greater Stable" when trying to build a "Stable"
                    f"//h2[contains(text(), '{building.name}')]",
                    By.XPATH,
                ).find_element(By.XPATH, "./following::a[contains(@class, 'build')]")
            )
        except NoSuchElementException:
            raise BuildingException(
                f"Cannot build {building} in plot {self.plotId} in {self.village}."
            )
        except PremiumFeatureException:
            raise BuildingException(
                f"No free workers to build {building} in {self.plotId} in {self.village}."
            )


def upgrade_or_build(
    driver: Driver, village: PlayerVillage, building: Building
) -> None:
    try:
        with BuildingScreen(driver, village, building) as bs:
            bs.upgrade()
    except NoBuildingThereException:
        with EmptyPlotScreen(driver, village, village.buildings[building]) as ep:
            ep.build(building)
