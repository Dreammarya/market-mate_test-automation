# conftest.py
import configparser
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


@pytest.fixture(scope="session")
def config() -> configparser.SectionProxy:
    """
    Read configuration (e.g. auth credentials) from config.ini.
    Expects a [auth] section with 'email' and 'password'.
    """
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    return parser["auth"]


@pytest.fixture(scope="function")
def driver():
    """
    Function-scoped WebDriver: creates a fresh Chrome instance for each test.
    """
    options = Options()
    options.add_argument("--start-maximized")
    driver_instance = webdriver.Chrome(options=options)
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(autouse=True)
def clear_browser_state(driver):
    """
    Before each test:
      - Clear cookies
      - Clear localStorage (if possible)
    """
    driver.delete_all_cookies()
    try:
        driver.execute_script("window.localStorage.clear();")
    except WebDriverException:
        # happens e.g. on about:blank
        pass
    yield
