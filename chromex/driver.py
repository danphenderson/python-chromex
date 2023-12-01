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

    :ivar _browser: An instance of Selenium's Chrome WebDriver.
    :vartype _browser: Chrome
    :ivar _tasks: A list to track asynchronous tasks.
    :vartype _tasks: list
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

        :param func: The synchronous function to run.
        :type func: function
        :return: The result of the asynchronous execution of the function.
        :rtype: Awaitable[Any]
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func)
    
        
    async def run_async(self, func) -> Awaitable[Any]:
        """
        Executes a given function asynchronously.

        This method is used internally to run synchronous Selenium commands in an asynchronous manner.

        :param func: The synchronous function to be run asynchronously.
        :type func: function
        :return: The result of the asynchronous execution.
        :rtype: Awaitable[Any]
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

        :param url: The URL to navigate to.
        :type url: str
        :param wait: The number of seconds to wait after navigating to the URL. Defaults to 0.
        :type wait: (int, optional)
        """
        logger.info(f"Getting {url}")
        await self.run_async(lambda: self._browser.get(url))
        if wait > 0:
            await self.wait(wait)

    async def page_soup(self) -> Awaitable[BeautifulSoup]:
        """
        Asynchronously gets the BeautifulSoup object of the current page.

        :return: The BeautifulSoup object of the current page source.
        :rtype: Awaitable[BeautifulSoup]
        """
        logger.info("Getting page soup")
        return await self.run_async(
            lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser")
        )

    async def element(self, value: str, by: str = "id") -> Awaitable[WebElement]:
        """
        Asynchronously finds a web element on the current page.

        This method searches for a single web element based on the provided value and search criteria (e.g., by 'id' or 'name') and returns the first matching element.

        :param value: The value of the element to find.
        :type value: str
        :param by: The type of search to perform (e.g., by 'id' or 'name'). Defaults to 'id'.
        :type by: str
        :return: The first web element found on the page.
        :rtype: Awaitable[WebElement]
        """
        logger.info(f"Getting element {value} by {by}")
        return await self.run_async(
            lambda: self._browser.find_element(by=by, value=value)
        )


    async def elements(self, value: str, by: str = "id") -> Awaitable[list[WebElement]]:
        """
        Asynchronously finds multiple web elements on the current page.

        This method searches for web elements based on the provided value and search criteria (e.g., by 'id' or 'name'). It returns a list of all matching elements.

        :param value: The value of the elements to find.
        :type value: str
        :param by: The type of search to perform (e.g., by 'id' or 'name'). Defaults to 'id'.
        :type by: str
        :return: A list of web elements found on the page.
        :rtype: Awaitable[list[WebElement]]
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

        This method locates a web element based on the given search criteria and sends the specified keys to it. It can also handle special keys like 'Enter'.

        :param value: The value of the element to send keys to.
        :type value: str
        :param keys: The keys to send to the element.
        :type keys: str
        :param by: The type of search to perform (e.g., by 'id'). Defaults to 'id'.
        :type by: str
        :param key: The special key to be sent (e.g., Keys.ENTER). Defaults to Keys.ENTER.
        :type key: Keys
        :raises ValueError: If the specified element is not found.
        """
        logger.info(f"Sending keys {keys} to element {value} by {by}")
        element = await self.element(value, by)
        if not isinstance(element, WebElement):
            logger.error(f"Element {value} not found, search by {by}")
            raise ValueError(f"Element {value} not found, search by {by}")
        await self.run_async(lambda: element.send_keys(keys, key))

    async def wait(self, seconds: int) -> None:
        """
        Asynchronously waits for a specified number of seconds.

        This method is used to pause the execution for a given duration.

        :param seconds: The number of seconds to wait.
        :type seconds: int
        """
        if seconds <= 0:
            return # for convience of calling code
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

        This method is a convenience method for navigating to the Google homepage.
        """
        return await self.get(url="https://www.google.com")

    async def page(self) -> str:
        """
        Retrieves the text content of the current page.

        :return The text content of the current page.
        :rtype str
        """
        soup = await self.run_async(lambda: BeautifulSoup(self._browser.page_source.strip(), "html.parser"))
        if not isinstance(soup, BeautifulSoup):
            raise ValueError(f"Unable to parse page source")
        return soup.get_text()

    async def google_search(self, query: str) -> None:
        """
        Performs a Google search for the specified query.

        This method navigates to the Google homepage, enters the given query into the search bar, and submits the search.

        :param query: The search query.
        :type query: str
        """
        await self.google()
        await self.send_element_keys("q", query, key=Keys.RETURN)

async def get_driver() -> Awaitable[Driver]:
    """
    Asynchronously creates and returns a new Driver instance.

    :return: A new Driver instance.
    :rtype: Awaitable[Driver]
    """
    return await Driver() # type: ignore
