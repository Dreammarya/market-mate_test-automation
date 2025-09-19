from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
import pytest
import time
from config import AUTH_URL, TEST_USER_CREDENTIALS, INVALID_DOB
from pages.shopping_page import ShopPage
from datetime import datetime, timedelta

# Age Verification Test Cases (1st, 2nd, 3rd)
@pytest.mark.parametrize("birth_date, expected", [
    ((datetime.now() - timedelta(days=18*365)).strftime("%d-%m-%Y"), "store"),
    ((datetime.now() - timedelta(days=17*365)).strftime("%d-%m-%Y"), "underage"),
    ((datetime.now() - timedelta(days=19*365)).strftime("%d-%m-%Y"), "store"),
])
def test_age_verification(driver, birth_date, expected):
    driver.get(AUTH_URL)

    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    shopping_page = ShopPage(driver)
    shopping_page.complete_age_verification(birth_date)  
    time.sleep(2)

    if expected == "store":
        assert "store" in driver.current_url
    elif expected == "underage":
        assert "underage" in shopping_page.read_error_message()  

# Age Verification 4th Test Case
def test_age_verification_empty_date(driver):
    driver.get(AUTH_URL)

    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    shopping_page = ShopPage(driver)
    shopping_page.try_empty_date_submission()   

    assert "underage" in shopping_page.read_error_message() 

# Age Verification 5th Test Case
def test_age_verification_invalid_format(driver):
    driver.get(AUTH_URL)

    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    shopping_page = ShopPage(driver)
    shopping_page.open_store_page()
    shopping_page.fill_birth_date(INVALID_DOB)  
    shopping_page.click_confirm_button()          

    assert "underage" in shopping_page.read_error_message()  