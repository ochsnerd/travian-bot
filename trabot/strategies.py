import asyncio
from pathlib import Path
from typing import Callable

from trabot.core import HOME, login

from .commands import (
    build_next,
    saturate_raid,
    train_in_stable,
    upgrade_random_resource,
)
from .resources import Clay, Crop, Iron, Lumber
from .trade import send_resources
from .troops import EquitesImperatoris
from .driver import Driver
from .locations import FarmVillage, PlayerVillage, Village


async def forever(f: Callable[[], float], backoff_base: float = 10, quiet: bool = True):
    fails = 0
    while True:
        try:
            t = f()
            fails = 0
        except Exception as e:
            print(f"Problem: {e}")
            fails += 1
            t = backoff_base * fails
        if not quiet:
            print(f"Waiting for {t}s")
        await asyncio.sleep(t)


async def forever_static[T](f: Callable[[], T], interval: float, backoff_base: float = 10):
    def fun():
        f()
        return interval

    await forever(fun, backoff_base)


async def farm(
    driver: Driver,
    village: PlayerVillage,
    targets: list[FarmVillage],
):
    unit = EquitesImperatoris
    async with asyncio.TaskGroup() as tg:
        for t in targets:
            tg.create_task(
                forever(lambda t=t: saturate_raid(driver, village, unit, t, 1.1, 15 * 60))
            )


async def expand_army(driver: Driver, village: PlayerVillage):
    await forever_static(
        lambda: train_in_stable(driver, village, 1, EquitesImperatoris),
        71,
    )


async def upgrade_resources(driver: Driver, village: PlayerVillage, interval: float):
    await forever_static(lambda: upgrade_random_resource(driver, village), interval, 30)


async def build_city(driver: Driver, village: PlayerVillage, plan: Path, interval: float):
    await forever_static(lambda: build_next(driver, village, plan), interval, 30)


async def support(driver: Driver, source: PlayerVillage, target: Village, amount: int):
    res = {Lumber: amount, Clay: amount, Iron: amount, Crop: amount}
    await forever_static(lambda: send_resources(driver, source, target, res), 15 * 60)

async def keep_logged_in(driver: Driver, username: str, password: str):
    login(driver, username, password)
    await forever_static(lambda: driver.goto(HOME), 60)

