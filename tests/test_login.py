import pytest
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import AUTH_URL, TEST_USER_CREDENTIALS, DEFAULT_TIMEOUT


def test_login_success(driver):
    # Go to login page
    driver.get(AUTH_URL)

    # Use LoginPage class to log in
    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    # Wait until URL changes after login
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_changes(AUTH_URL))

    # Assert login worked (URL is not the same anymore)
    assert driver.current_url != AUTH_URL
