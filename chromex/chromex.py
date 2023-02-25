from chromex.base.conf import conf
from selenium.webdriver import Chrome

from chromex.models.driver import ChromeX
from chromex.models.edge import href
from chromex.models.node import hpage


async def driver() -> ChromeX:
    async with ChromeX(_browser=Chrome(conf.driver_path, options=conf.options)) as chromex:
        return chromex