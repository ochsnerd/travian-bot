import time
from trabot.buildings import BuildingScreen, MarketPlace
from trabot.driver import Driver
from trabot.locations import PlayerVillage, Village
from trabot.resources import Resource


def send_resources(
    driver: Driver,
    source: PlayerVillage,
    target: Village,
    resources: dict[Resource, int],
) -> None:
    with BuildingScreen(driver, source, MarketPlace):
        print(f"Sending {resources} from {source} to {target}")
        for res, amount in resources.items():
            driver.retrieve(f"[id={res.id_in_market}]").send_keys(str(amount))

        driver.retrieve(f"[name=x]").send_keys(str(target.location.x))
        driver.retrieve(f"[name=y]").send_keys(str(target.location.y))

        driver.retrieve("[name=s1]").click()
        driver.retrieve("[name=s1]").click()
