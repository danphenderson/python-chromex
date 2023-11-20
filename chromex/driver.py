import asyncio
from typing import Awaitable, Any
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from chromex.base.logging import logger

from chromex.base.conf import conf

class Driver:
     
    @staticmethod
    async def _run_sync(func) -> Awaitable[Any]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func)
    

    def __init__(self, **data):
        super().__init__(**data)
        self._browser = Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=conf.options,
            )
        self._tasks = []


    def __aenter__(self):
        return self

    def __await__(self):
        return self._run_sync(lambda: self).__await__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger.info(f"Closing Chrome Driver with {len(self._tasks)} tasks remaining")
        await self.close()
 
    @property
    def page_source(self) -> str:
        return self._browser.page_source

    @property
    def current_url(self) -> str:
        return self._browser.current_url

    @property
    def title(self) -> str:
        return self._browser.title       

    async def run_async(self, func) -> Awaitable[Any]:
        logger.debug(f"Running async function {func.__name__}")
        task = asyncio.create_task(self._run_sync(func))
        self._tasks.append(task)
        logger.debug(f"Task {task} added to {len(self._tasks)} tasks")
        return await task

    async def get(self, url: str, wait: int = 0) -> None:
        logger.info(f"Getting {url}")
        await self.run_async(lambda: self._browser.get(url))
        if wait > 0:
            await self.wait(wait)

    async def page_soup(self) -> Awaitable[BeautifulSoup]:
        logger.info("Getting page soup")
        return await self.run_async(
            lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser")
        )

    async def element(self, value: str, by: str = "id") -> Awaitable[WebElement]:
        logger.info(f"Getting element {value} by {by}")
        return await self.run_async(
            lambda: self._browser.find_element(by=by, value=value)
        )

    async def elements(self, value: str, by: str = "id") -> Awaitable[list[WebElement]]:
        logger.info(f"Getting elements {value} by {by}")
        return await self.run_async(
            lambda: self._browser.find_elements(by=by, value=value)
        )

    async def send_element_keys(
        self, value: str, keys: str, by: str = "id", key=Keys.ENTER
    ) -> None:
        logger.info(f"Sending keys {keys} to element {value} by {by}")
        element = await self.element(value, by)
        if not isinstance(element, WebElement):
            logger.error(f"Element {value} not found, search by {by}")
            raise ValueError(f"Element {value} not found, search by {by}")
        await self.run_async(lambda: element.send_keys(keys, key))

    async def wait(self, seconds) -> None:
        logger.info(
            f"Waiting {seconds} seconds; there are {len(self._tasks)} tasks queued"
        )
        await asyncio.sleep(seconds)

    async def close(self) -> None:
        logger.critical(
            f"Closing Chrome Driver with {len(self._tasks)} tasks remaining"
        )
        await self.run_async(self._browser.close)

    async def google(self):
        return await self.get(url="https://www.google.com")

    async def page(self) -> str:
        soup = await self.run_async(lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser"))
        if not isinstance(soup, BeautifulSoup):
            raise ValueError(f"Unable to parse page source")
        return soup.get_text()

    async def google_search(self, query: str) -> None:
        await self.google()
        await self.send_element_keys("q", query, key=Keys.RETURN)


async def get_driver() -> Awaitable[Driver]:
    return await Driver() # type: ignore
