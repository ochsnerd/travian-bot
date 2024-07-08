from pathlib import Path
from shutil import copyfile

from .buildings import ALL_BUILDINGS, Building


def copy(source: Path, target: Path) -> None:
    copyfile(source, target)


def peek(plan: Path) -> Building:
    with open(plan, "r") as f:
        building = f.readlines()[0]
    return parse(building)


def pop(plan: Path) -> Building:
    with open(plan, "r") as f:
        buildings = f.readlines()
    building = parse(buildings[0])
    with open(plan, "w") as f:
        f.writelines(buildings[1:])
    return building


def parse(s: str) -> Building:
    return ALL_BUILDINGS[s.strip()]
