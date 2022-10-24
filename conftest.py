import os
import logging
import configparser
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def pytest_addoption(parser):
    """
    Add options to the pyest command line.
    Default driver kept as chrome, at the moment.
    Args:
        parser (object): pytest cli parser object
    """

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Type in browser name, e.g. chrome or firefox or edge",
    )


@pytest.fixture(scope="class")
def getBrowser(request):
    """
    Fixture to get browser name from command line option.

    Args:
        request (object): pytest cli request object

    Returns:
        _browser: str
    """

    _browser = request.config.getoption("--browser")
    return _browser


@pytest.fixture(scope="class")
def setup(request, getBrowser):
    """
    Fixture for test setup.

    Args:
        request (object): pytest cli request object
        getBrowser (str): name of the browser
    """

    test_log_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "Reports", "logs", "test.log")
    )
    logging.basicConfig(
        filename=test_log_path,
        format="%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        filemode="w",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    # Setting up the driver and browser
    driver = _set_browser(getBrowser)

    confparse = configparser.ConfigParser(interpolation=None)
    conf_file_path = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "pytest-allure-test-automation-framework",
            "Resources",
            "config.ini",
        )
    )

    confparse.read(conf_file_path)

    # Load each of your sections from config.ini file as below.
    app = confparse["APP"]
    settings = confparse["SETTINGS"]

    wait = WebDriverWait(driver, int(settings.get("driver_wait")))
    logger.info(
        f"Launching {getBrowser} browser and settings wait time to {settings.get('driver_wait')} seconds"
    )
    driver.get(app.get("app_url"))
    driver.maximize_window()

    request.cls.logger = logger
    request.cls.driver = driver
    request.cls.wait = wait

    yield

    if driver is not None:
        logger.info(f"Closing {driver.name.upper()} browser")
        driver.close()
        logger.info(f"Quitting {driver.name.upper()} driver")
        driver.quit()


def _set_browser(browser):
    """
    Set webdriver options for given browser name
    and returns webdriver object.

    Args:
        browser (str): browser name
    Returns:
        driver: (object): webdriver object
    """

    # Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    # options.add_argument('--window-size=1920,1080')
    # options.add_argument('--allow-running-insecure-content')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")

    # Firefox options
    options_gecko = webdriver.FirefoxOptions()
    options_gecko.add_argument("--ignore-certificate-errors")
    options_gecko.add_argument("--ignore-ssl-errors")
    options_gecko.add_argument("--disable-infobars")
    options_gecko.add_argument("--disable-dev-shm-usage")
    options_gecko.add_argument("--no-sandbox")
    # options_gecko.add_argument('--headless')
    options_gecko.add_argument("--disable-gpu")
    # options_gecko.add_argument('--window-size=1920,1080')
    # options_gecko.add_argument('--allow-running-insecure-content')
    options_gecko.add_argument("--start-maximized")
    options_gecko.add_argument("--disable-popup-blocking")

    if browser.lower() == "chrome":
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
    elif browser.lower() == "firefox":
        driver = webdriver.Chrome(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options_gecko,
        )
    elif browser.lower() == "edge":
        driver = webdriver.Chrome(
            service=EdgeService(EdgeChromiumDriverManager().install())
        )
    else:
        pytest.fail(f"Invalid browser name {browser}")

    return driver
