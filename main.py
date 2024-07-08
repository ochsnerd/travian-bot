import asyncio
from pathlib import Path

from selenium.webdriver import ChromeOptions
from trabot.driver import Driver
from trabot.core import login, run_all
from trabot.strategies import build_city, expand_army, farm, support, upgrade_resources

from data import *
from credentials import username, password


if __name__ == "__main__":
    saturation = 1
    targets1 = [
        farm17,
        farm18,
        farm8,
        farm9,
        farm6,
    ]
    targets2 = [
        prairie,
        farm13,
        farm2,
        farm6,
        farm7,
        farm4,
        farm1,
    ]
    o = ChromeOptions()
    o.add_argument("--headless=new")
    d = Driver(options=o)
    login(d, username, password)
    asyncio.run(
        run_all(
            build_city(d, caemlyn, Path("something_nice.txt"), 30 * 60),
            farm(d, caemlyn, targets1),
            support(d, caemlyn, fal_moran, 4000),
            support(d, caemlyn, fal_dara, 4000),
            expand_army(d, cairhien),
            build_city(d, cairhien, Path("village11.txt"), 30 * 60),
            farm(d, cairhien, targets2),
            upgrade_resources(d, fal_moran, 5 * 60),
            build_city(d, fal_moran, Path("fal_moran.txt"), 2 * 60),
            upgrade_resources(d, fal_dara, 5 * 60),
            build_city(d, fal_dara, Path("fal_dara.txt"), 2 * 60),
        )
    )
