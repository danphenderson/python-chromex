from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from asyncio import Future



from chromex.base.abstract import BaseModel
from chromex.base.conf import conf
from chromex.models.edge import HRef, href
from chromex.models.node import HPage, hpage

BaseModel.Config.arbitrary_types_allowed = True

class ChromeX(BaseModel):
    _browser : Chrome

    @property
    def page_source(self) -> str:
        return self._browser.page_source

    @property
    def current_url(self) -> str:
        return self._browser.current_url

    @property
    def title(self) -> str:
        return self._browser.title       

    async def google(self) -> HRef:
        return await href(url="https://www.google.com")

    
    async def get(self, edge: HRef, wait: int = 0) -> None:
        await self.run_async(lambda: self._browser.get(edge.url))
        if wait > 0:
            await self.wait(wait)


    async def page(self) -> HPage:
        soup = await self.run_async(lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser"))
        if not isinstance(soup, BeautifulSoup):
            raise ValueError(f"Unable to parse page source")
        return await hpage(self.title, soup.get_text())


    async def element(self, value: str, by: str = "id") -> Future[WebElement]:
        return await self.run_async(lambda: self._browser.find_element(by=by, value=value))
        
    
    async def elements(self, value: str, by: str = "id") -> Future[list[WebElement]]:
        return await self.run_async(lambda: self._browser.find_elements(by=by, value=value))

    
    async def send_element_keys(self, value: str, keys: str, by: str = "id", key = Keys.ENTER) -> None:
        element = await self.element(value, by)
        if not isinstance(element, WebElement):
            raise ValueError(f"Element {value} not found, search by {by}")
        await self.run_async(lambda: element.send_keys(keys, key))


    async def google_search(self, query: str) -> None:
        await self.google()
        await self.send_element_keys("q", query, key=Keys.RETURN)

async def driver() -> ChromeX:
    async with ChromeX(_browser=Chrome(conf.driver_path, options=conf.options)) as chromex:
        return chromex