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
    """
    Asynchronous driver class for automating web browser actions using Selenium and Chrome.

    Attributes:
        _browser (Chrome): An instance of Selenium's Chrome WebDriver.
        _tasks (list): A list to track asynchronous tasks.
    """

    def __init__(self, **data):
        """
        Initializes the Driver instance with a Chrome WebDriver and an empty tasks list.
        """

        super().__init__(**data)
        self._browser = Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=conf.options,
            )
        self._tasks = []

     
    @staticmethod
    async def _run_sync(func) -> Awaitable[Any]:
        """
        Executes a synchronous function asynchronously using asyncio.

        Args:
            func (function): The synchronous function to run.

        Returns:
            Awaitable[Any]: The result of the asynchronous execution of the function.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func)
    
        
    async def run_async(self, func) -> Awaitable[Any]:
        """
        Executes a given function asynchronously.

        This method is used internally to run synchronous Selenium commands in an asynchronous manner.

        Args:
            func (function): The synchronous function to be run asynchronously.

        Returns:
            Awaitable[Any]: The result of the asynchronous execution.
        """
        logger.debug(f"Running async function {func.__name__}")
        task = asyncio.create_task(self._run_sync(func))
        self._tasks.append(task)
        logger.debug(f"Task {task} added to {len(self._tasks)} tasks")
        return await task
    
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

    async def get(self, url: str, wait: int = 0) -> None:
        """
        Asynchronously navigates to a specified URL.

        Optionally waits for a specified number of seconds after loading the page.

        Args:
            url (str): The URL to navigate to.
            wait (int, optional): The number of seconds to wait after navigating to the URL. Defaults to 0.
        """
        logger.info(f"Getting {url}")
        await self.run_async(lambda: self._browser.get(url))
        if wait > 0:
            await self.wait(wait)

    async def page_soup(self) -> Awaitable[BeautifulSoup]:
        """
        Asynchronously gets the BeautifulSoup object of the current page.

        Returns:
            Awaitable[BeautifulSoup]: The BeautifulSoup object of the current page source.
        """
        logger.info("Getting page soup")
        return await self.run_async(
            lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser")
        )

    async def element(self, value: str, by: str = "id") -> Awaitable[WebElement]:
        """
        Asynchronously finds a web element on the current page.

        Args:
            value (str): The value of the element to find.
            by (str, optional): The type of search to perform (e.g., by 'id' or 'name'). Defaults to 'id'.

        Returns:
            Awaitable[WebElement]: The web element found on the page.
        """
        logger.info(f"Getting element {value} by {by}")
        return await self.run_async(
            lambda: self._browser.find_element(by=by, value=value)
        )


    async def elements(self, value: str, by: str = "id") -> Awaitable[list[WebElement]]:
        """
        Asynchronously finds multiple web elements on the current page.

        Args:
            value (str): The value of the elements to find.
            by (str, optional): The type of search to perform (e.g., by 'id' or 'name'). Defaults to 'id'.

        Returns:
            Awaitable[list[WebElement]]: A list of web elements found on the page.
        """
        logger.info(f"Getting elements {value} by {by}")
        return await self.run_async(
            lambda: self._browser.find_elements(by=by, value=value)
        )

    async def send_element_keys(
        self, value: str, keys: str, by: str = "id", key=Keys.ENTER
    ) -> None:
        """
        Sends keys to a web element found on the page.

        Args:
            value (str): The value of the element to send keys to.
            keys (str): The keys to send to the element.
            by (str, optional): The type of search to perform (e.g., by 'id'). Defaults to 'id'.
            key (Keys, optional): The special key to be sent (e.g., Keys.ENTER). Defaults to Keys.ENTER.

        Raises:
            ValueError: If the specified element is not found.
        """
        logger.info(f"Sending keys {keys} to element {value} by {by}")
        element = await self.element(value, by)
        if not isinstance(element, WebElement):
            logger.error(f"Element {value} not found, search by {by}")
            raise ValueError(f"Element {value} not found, search by {by}")
        await self.run_async(lambda: element.send_keys(keys, key))

    async def wait(self, seconds) -> None:
        """
        Asynchronously waits for a specified number of seconds.

        This method is used to pause the execution for a given duration.

        Args:
            seconds (int): The number of seconds to wait.
        """
        logger.info(
            f"Waiting {seconds} seconds; there are {len(self._tasks)} tasks queued"
        )
        await asyncio.sleep(seconds)


    async def close(self) -> None:
        """
        Closes the Chrome WebDriver instance and logs the action.

        This method should be called to ensure proper cleanup of resources.
        """
        logger.critical(
            f"Closing Chrome Driver with {len(self._tasks)} tasks remaining"
        )
        await self.run_async(self._browser.close)

    async def google(self):
        """
        Navigates to the Google homepage.
        """
        return await self.get(url="https://www.google.com")

    async def page(self) -> str:
        """
        Retrieves the text content of the current page.

        Returns:
            str: The text content of the current page.
        """
        soup = await self.run_async(lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser"))
        if not isinstance(soup, BeautifulSoup):
            raise ValueError(f"Unable to parse page source")
        return soup.get_text()

    async def google_search(self, query: str) -> None:
        """
        Performs a Google search for the specified query.

        Args:
            query (str): The search query.
        """
        await self.google()
        await self.send_element_keys("q", query, key=Keys.RETURN)


async def get_driver() -> Awaitable[Driver]:
    """
    Asynchronously creates and returns a new Driver instance.

    Returns:
        Awaitable[Driver]: A new Driver instance.
    """
    return await Driver() # type: ignore
