
from asyncio import Future
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from chromex.conf import conf

from chromex.abstract import BaseModel

class Driver(BaseModel):
    _driver: Chrome = Chrome(conf.driver_path, options=conf.options)

    async def get(self, url: str, wait: int = 0) -> None:
        await self.run_async(lambda: self._driver.get(url))
        if wait > 0:
            await self.wait(wait)

    async def page_soup_html(self) -> Future[BeautifulSoup]:
        return await self.run_async(lambda: BeautifulSoup(self._driver.page_source.strip(), "html.parser"))

    async def element(self, value: str, by: str = "id") -> Future[WebElement]:
        return await self.run_async(lambda: self._driver.find_element(by=by, value=value))
        
    
    async def elements(self, value: str, by: str = "id") -> Future[list[WebElement]]:
        return await self.run_async(lambda: self._driver.find_elements(by=by, value=value))

    
    async def send_element_keys(self, value: str, keys: str, by: str = "id", key = Keys.ENTER) -> None:
        element = await self.element(value, by)
        if not isinstance(element, WebElement):
            raise ValueError(f"Element {value} not found, search by {by}")
        await self.run_async(lambda: element.send_keys(keys, key))
        

async def driver():
    async with Driver() as driver:
        return driver
