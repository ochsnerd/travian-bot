import math
from .driver import Driver
from .resources import get_resource_production, Crop
from .locations import PlayerVillage, FarmVillage
from .troops import SendTroopsScreen, SendTroopsSpecification, StableScreen, Unit, Raid


def build_in_stable(driver: Driver, village: PlayerVillage, n: int, kind: Unit) -> None:
    if get_resource_production(driver, village, Crop) < 10:
        print(f"Not Crop production in {village} to build {kind}.")
        return
    with StableScreen(driver, village) as ss:
        ss.select(n, kind)
        ss.start()
        print(f"Building {n} {kind}.")


def raid(
    driver: Driver,
    order: SendTroopsSpecification,
) -> float:
    print(f"Raiding {order.target} with {order.units}.")
    return 5 + 2 * SendTroopsScreen.execute(driver, order)


def saturate_raid(
    driver: Driver,
    source: PlayerVillage,
    unit: Unit,
    target: FarmVillage,
    interval: float = 300,
) -> float:
    production = target.production / 3600
    units_to_send = math.ceil(production * interval / unit.carrying_capacity)
    time_to_return = 2 * raid(
        driver,
        SendTroopsSpecification(source, Raid, [(units_to_send, unit)], target),
    )
    print(
        f"Need {units_to_send * time_to_return / interval:5.1f} {unit} in {source} for full saturation"
    )
    return interval
