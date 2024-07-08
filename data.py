from typing import Dict
from trabot.core import Id
from trabot.locations import VillageId, PlayerVillage, FarmVillage, MapLocation
from trabot.buildings import *


def make_blueprint() -> Dict[Building, Id]:
    return {
        GrainMill: Id(20),
        Brickyard: Id(21),
        Sawmill: Id(22),
        Bakery: Id(23),
        HorseDrinkingTrough: Id(24),
        HerosMansion: Id(25),
        MainBuilding: Id(26),
        IronFoundry: Id(27),
        Stable: Id(28),
        MarketPlace: Id(29),
        Barracks: Id(30),
        BlackSmith: Id(32),
        Embassy: Id(33),
        Armoury: Id(34),
        Academy: Id(35),
        Granary: Id(36),
        Residence: Id(37),
        Warehouse: Id(38),
        RallyPoint: Id(39),
        Wall: Id(40),
    }


caemlyn = PlayerVillage(
    MapLocation(-3, -19),
    id=VillageId(24023),
    name="Caemlyn",
    buildings=make_blueprint() | {Workshop: Id(31)},
)
cairhien = PlayerVillage(
    MapLocation(-10, -23),
    id=VillageId(24834),
    name="Cairhien",
    buildings=make_blueprint(),
)
fal_moran = PlayerVillage(
    MapLocation(44, 40),
    id=VillageId(12117),
    name="Fal Moran",
    buildings=make_blueprint(),
)

fal_dara = PlayerVillage(
    MapLocation(50, 40),
    id=VillageId(12111),
    name="Fal Dara",
    buildings=make_blueprint(),
)


prairie = FarmVillage(MapLocation(5, 3), 48000)
total_prod = 7500 * 4
farm1 = FarmVillage(MapLocation(-58, -73), total_prod)
farm2 = FarmVillage(MapLocation(-40, -57), total_prod)

farm4 = FarmVillage(MapLocation(65, -44), total_prod)

farm6 = FarmVillage(MapLocation(-31, 35), total_prod)
farm7 = FarmVillage(MapLocation(-38, 75), total_prod)
farm8 = FarmVillage(MapLocation(3, -68), total_prod)
farm9 = FarmVillage(MapLocation(-17, 38), total_prod)
farm10 = FarmVillage(MapLocation(-45, 53), total_prod)
farm11 = FarmVillage(MapLocation(56, 12), total_prod)
farm12 = FarmVillage(MapLocation(-83, -47), total_prod)
farm13 = FarmVillage(MapLocation(-4, -59), total_prod)
farm14 = FarmVillage(MapLocation(-4, 81), total_prod)
farm15 = FarmVillage(MapLocation(61, -56), total_prod)
farm16 = FarmVillage(MapLocation(45, 86), total_prod)
farm17 = FarmVillage(MapLocation(22, 10), total_prod)
farm18 = FarmVillage(MapLocation(-52, -24), total_prod)
