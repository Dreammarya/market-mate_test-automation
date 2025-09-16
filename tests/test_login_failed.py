import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from config import AUTH_URL, TEST_USER_CREDENTIALS, DEFAULT_TIMEOUT


def test_login_fail_wrong_password(driver):
    #  Negative test - user enters wrong password

    # Open login page
    driver.get(AUTH_URL)

    # Try to login with correct email but WRONG password
    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], "wrongpassword123")

    # Wait until error message is shown
    error_message = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Invalid email or password')]")
        )
    )

    # Check that the error message text is correct
    assert "Invalid email or password" in error_message.text
