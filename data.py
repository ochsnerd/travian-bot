from trabot.core import Id
from trabot.locations import VillageId, PlayerVillage, FarmVillage, MapLocation
from trabot.buildings import Stable


something_nice = PlayerVillage(
    MapLocation(-3, -19), id=VillageId(24023), buildings={Stable: Id(28)}
)
davids_village_11 = PlayerVillage(
    MapLocation(-10, -23), id=VillageId(24834), buildings={Stable: Id(28)}
)


prairie = FarmVillage(MapLocation(5, 3), 48000)
total_prod = 7500 * 4
farm2 = FarmVillage(MapLocation(-40, -57), total_prod)
farm6 = FarmVillage(MapLocation(-57, -53), total_prod)
farm8 = FarmVillage(MapLocation(3, -68), total_prod)
farm9 = FarmVillage(MapLocation(-17, 38), total_prod)
farm11 = FarmVillage(MapLocation(56, 12), total_prod)
farm13 = FarmVillage(MapLocation(-4, -59), total_prod)
farm17 = FarmVillage(MapLocation(22, 10), total_prod)
farm18 = FarmVillage(MapLocation(-52, -24), total_prod)
