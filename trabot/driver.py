from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from trabot.core import Link


# TODO: Are you a Monad?
class Driver(Chrome):

    def goto(self, link: Link):
        super().get(link.to_url())

    def retrieve(self, selector: str, by=By.CSS_SELECTOR) -> WebElement:
        return super().find_element(by, selector)

    def get(self, url: str) -> None:
        print("Use Driver.goto()")
        super().get(url)

    def find_element(self, by=By.ID, value: str | None = None) -> WebElement:
        print("Use Driver.retrieve()")
        return super().find_element(by, value)
