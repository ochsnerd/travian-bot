import asyncio
from trabot.driver import Driver
from trabot.core import forever_static, run_all, keep_logged_in, forever
from trabot.commands import saturate_raid, build_in_stable
from trabot.troops import EquitesImperatoris

from data import *
from credentials import username, password


if __name__ == "__main__":
    targets = [prairie, farm17, farm8, farm18, farm11, farm9]
    d = Driver()
    asyncio.run(
        run_all(
            keep_logged_in(d, username, password),
            forever_static(
                lambda: build_in_stable(d, davids_village_11, 1, EquitesImperatoris),
                160,
            ),
            forever_static(
                lambda: build_in_stable(d, something_nice, 1, EquitesImperatoris),
                71,
            ),
            forever(
                lambda: saturate_raid(d, davids_village_11, EquitesImperatoris, farm13)
            ),
            *[
                forever(
                    lambda t=t: saturate_raid(d, something_nice, EquitesImperatoris, t)
                )
                for t in targets
            ],
        )
    )
