from trabot.core import Id
from trabot.locations import VillageId, PlayerVillage, FarmVillage, MapLocation
from trabot.buildings import Stable


something_nice = PlayerVillage(
    MapLocation(-3, -19), id=VillageId(24023), buildings={Stable: Id(28)}
)
davids_village_11 = PlayerVillage(
    MapLocation(-10, -23), id=VillageId(24834), buildings={Stable: Id(28)}
)

prairie = FarmVillage(MapLocation(5, 3), 12_000)
farm8 = FarmVillage(MapLocation(3, -68), 7500)
farm9 = FarmVillage(MapLocation(-17, 38), 7500)
farm11 = FarmVillage(MapLocation(56, 12), 7500)
farm13 = FarmVillage(MapLocation(-4, -59), 7500)
farm17 = FarmVillage(MapLocation(22, 10), 7500)
farm18 = FarmVillage(MapLocation(-52, -24), 7500)
