
from asyncio import sleep, gather, get_event_loop, Future, ensure_future
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from chromex.conf import conf


class AsyncDriver:
    
    
    @staticmethod
    async def _run_sync(func, *args) -> Future:
        loop = get_event_loop()
        return await loop.run_in_executor(None, func, *args)

    
    def __init__(self):
        self._driver = webdriver.Chrome(conf.driver_path, options=conf.options)
        self._tasks = []


    async def __aenter__(self):
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with
        return self


    async def __aexit__(self, exc_type, exc_value, traceback):
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with
        pass


    async def __await__(self):
        return self._run_sync(lambda: self).__await__()


    async def run_async(self, func, *args) -> Future:
        task = ensure_future(self._run_sync(func, *args))
        self._tasks.append(task)
        return await task


    async def get(self, url: str, wait: int = 0) -> None:
        await self.run_async(lambda: self._driver.get(url))
        if wait > 0:
            await self.wait(wait)

    
    async def wait(self, seconds: int) -> None:
        await self.run_async(sleep, seconds)

    
    async def close(self) -> None:
        if self._tasks:
            await gather(*self._tasks)
        await self.run_async(self._driver.close)


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
        

async def async_driver():
    async with AsyncDriver() as driver:
        return driver
