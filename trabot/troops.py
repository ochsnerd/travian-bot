from dataclasses import dataclass

from .locations import PlayerVillage, Village
from .buildings import Building, Stable, Barracks, BuildingScreen
from .driver import Driver, By
from .core import StaticScreen, ResourceException, SEND_TROOPS

from selenium.common.exceptions import NoSuchElementException


@dataclass(frozen=True)
class Unit:
    name: str
    send_troops_name: str
    carrying_capacity: int

    built_in: Building

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


Legionnaire = Unit("Legionnaire", "t1", 50, Barracks)
EquitesImperatoris = Unit("Equites Imperatoris", "t5", 100, Stable)


@dataclass(frozen=True)
class MoveType:
    value: str


Reinforcement = MoveType("2")
NormalAttack = MoveType("3")
Raid = MoveType("4")


@dataclass
class SendTroopsSpecification:
    source: PlayerVillage
    kind: MoveType
    units: list[tuple[int, Unit]]
    target: Village


class StableScreen(BuildingScreen):
    def __init__(self, driver: Driver, village: PlayerVillage) -> None:
        super().__init__(driver, village, Stable)

    def select(self, n: int, kind: Unit) -> None:
        self.driver.retrieve(f"[name={kind.send_troops_name}]").send_keys(n)

    def start(self) -> None:
        self.driver.retrieve("[name=s1]").click()


class SendTroopsScreen(StaticScreen):

    def __init__(self, driver: Driver, village: PlayerVillage) -> None:
        super().__init__(driver, village, SEND_TROOPS)

    def troops(self, n: int, kind: Unit) -> None:
        # Fixme: multiple calls to this should not override
        self.driver.retrieve(f"[name={kind.send_troops_name}]").send_keys(n)

    def target(self, village: Village) -> None:
        self.driver.retrieve("[name=x]").send_keys(village.location.x)
        self.driver.retrieve("[name=y]").send_keys(village.location.y)

    def order(self, kind: MoveType):
        self.driver.retrieve(f"[value='{kind.value}']").click()

    def send(self) -> float:
        self.driver.retrieve("[name=s1]").click()
        try:
            arrives_in = self.parse_timestamp(self.driver.retrieve(".in").text)
            self.driver.retrieve("[name=s1]").click()
        except NoSuchElementException:
            raise ResourceException(
                f"Problem sending troops: {self.driver.retrieve( '.error').text}"
            )
        return arrives_in

    @staticmethod
    def parse_timestamp(s: str) -> float:
        hours, minutes, seconds = map(int, s.split()[1].split(":"))
        return 3600 * hours + 60 * minutes + seconds

    @staticmethod
    def execute(driver: Driver, spec: SendTroopsSpecification) -> float:
        with SendTroopsScreen(driver, spec.source) as s:
            for n, k in spec.units:
                s.troops(n, k)
            s.target(spec.target)
            s.order(spec.kind)
            return s.send()
