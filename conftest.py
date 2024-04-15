from logging import getLogger

from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service

from utils.config import BROWSER, BROWSER_PATH, URL

# Configure logging
logger = getLogger(__name__)


@pytest.fixture(scope='session', params=[BROWSER])
def start_browser(request):
    """
    Fixture to start the specified browser for testing.

    Parameters:
        request (FixtureRequest): Pytest fixture request object.

    Yields:
        WebDriver: Selenium WebDriver instance for the specified browser.
    """
    name = request.param.lower()
    driver = None

    try:
        if name == "firefox" or name == "ff":
            logger.info("Starting Firefox browser.")
            driver = webdriver.Firefox()
        elif name == "chrome":
            logger.info("Starting Chrome browser.")
            service = Service(executable_path=BROWSER_PATH)
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
        elif name == "ie":
            logger.info("Starting Internet Explorer browser.")
            driver = webdriver.Ie()
        elif name == "phantomjs":
            logger.info("Starting PhantomJS browser.")
            driver = webdriver.PhantomJS()
        else:
            raise ValueError(f"Unsupported browser: {name}. Supported options: 'firefox', 'chrome', 'ie', 'phantomjs'.")

        driver.maximize_window()  # Maximize browser window
        driver.get(URL)  # Navigate to the specified URL

        yield driver  # Provide the driver instance to the test function

    except Exception as e:
        logger.error(f"Error starting {name} browser: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info(f"Closing the {name} browser")




