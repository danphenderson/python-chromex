
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Conf:
    """
    Configuration class for setting up a Google Chrome web driver.

    This class provides various options to configure the behavior of a Selenium Chrome WebDriver. 
    It allows setting options like headless browsing, incognito mode, disabling GPU, and more.

    The configuration can be accessed via the `options` property, which returns an instance of `ChromeOptions` configured as per the set attributes.

    For more information on `ChromeOptions`, see: https://pypi.org/project/selenium/

    :ivar driver_path: The file system path to the ChromeDriver executable. Default is "/opt/homebrew/bin/chromedriver".
    :vartype driver_path: str
    :ivar headless_option: Enable or disable headless mode. Default is False.
    :vartype headless_option: bool
    :ivar incognito_option: Enable or disable incognito mode. Default is True.
    :vartype incognito_option: bool
    :ivar dump_dom_option: Enable or disable dumping the DOM. Default is False.
    :vartype dump_dom_option: bool
    :ivar disable_gpu_option: Enable or disable GPU. Useful especially for Windows OS. Default is False.
    :vartype disable_gpu_option: bool
    """
    driver_path: str = "/opt/homebrew/bin/chromedriver" # TODO: Change, maybe read BREW_PATH from env
    headless_option: bool = False
    incognito_option: bool = True
    dump_dom_option: bool = False
    disable_gpu_option: bool = False

    @property
    def options(self) -> ChromeOptions:
        """
        Constructs and returns ChromeOptions based on the configuration.

        This property method initializes a `ChromeOptions` instance and configures it based on the class attributes like headless mode, incognito mode, etc.

        :return: An instance of `ChromeOptions` configured as per the set attributes.
        :rtype: ChromeOptions
        """
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