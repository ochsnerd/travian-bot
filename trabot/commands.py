import math
import random
from pathlib import Path

from .buildings import upgrade_or_build
from .plan import peek, pop
from .core import Id
from .driver import Driver
from .resources import ResourceScreen, get_resource_production, Crop
from .locations import PlayerVillage, FarmVillage
from .troops import SendTroopsScreen, SendTroopsSpecification, StableScreen, Unit, Raid


def train_in_stable(driver: Driver, village: PlayerVillage, n: int, kind: Unit) -> None:
    if get_resource_production(driver, village, Crop) < 10:
        print(f"Not Crop production in {village} to build {kind}.")
        return
    with StableScreen(driver, village) as ss:
        ss.select(n, kind)
        ss.start()
        print(f"Building {n} {kind}.")


def upgrade_random_resource(driver: Driver, village: PlayerVillage) -> None:
    fieldId = Id(random.randrange(1, 19))
    print(f"Upgrading Resource at Id={fieldId.value} in {village}")
    with ResourceScreen(driver, village, fieldId) as rs:
        rs.upgrade()


def raid(
    driver: Driver,
    order: SendTroopsSpecification,
) -> float:
    print(f"Raiding {order.target} with {order.units}.")
    return 5 + 2 * SendTroopsScreen.execute(driver, order)


def build_next(driver: Driver, village: PlayerVillage, plan: Path) -> None:
    building = peek(plan)
    print(f"Building {building} in {village}.")
    upgrade_or_build(driver, village, building)
    pop(plan)


def saturate_raid(
    driver: Driver,
    source: PlayerVillage,
    unit: Unit,
    target: FarmVillage,
    saturation_factor: float = 1,
    interval: float = 300,
) -> float:
    production = target.production / 3600
    units_to_send = math.ceil(
        saturation_factor * production * interval / unit.carrying_capacity
    )
    time_to_return = 2 * raid(
        driver,
        SendTroopsSpecification(source, Raid, [(units_to_send, unit)], target),
    )
    print(
        f"Need {units_to_send * time_to_return / interval:5.1f} {unit} in {source} for {saturation_factor:2.1f} saturation"
    )
    return interval
