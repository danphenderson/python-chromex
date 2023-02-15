
from pydantic import BaseSettings
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Conf(BaseSettings):
    """
    Configuration for a Google Chrome web driver.
    
    See https://pypi.org/project/selenium/, `ChromeOptions` for more information.
    """
    driver_path: str = "/opt/homebrew/bin/chromedriver"
    headless_option: bool = False
    incognito_option: bool = True
    dump_dom_option: bool = False
    disable_gpu_option: bool = False

    @property
    def options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        if self.incognito_option:
            options.add_argument("--incognito")
        if self.headless_option:
            options.add_argument("--headless")
        if self.disable_gpu_option:
            options.add_argument("--disable-gpu") # set to true for Windows OS
        if self.dump_dom_option:
            options.add_argument("--dump-dom")
        return options

conf = Conf()