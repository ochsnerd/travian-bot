from dataclasses import dataclass

from .driver import Driver, By
from .core import HOME
from .locations import PlayerVillage


@dataclass(frozen=True)
class Resource:
    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


Lumber = Resource("Lumber")
Clay = Resource("Clay")
Iron = Resource("Iron")
Crop = Resource("Crop")


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
