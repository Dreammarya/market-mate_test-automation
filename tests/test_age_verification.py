# test_age_verification.py
import pytest
import time
from datetime import datetime, timedelta
from pages.login_page import LoginPage
from pages.shopping_page import ShopPage
from config import AUTH_URL, TEST_USER_CREDENTIALS, INVALID_DOB


@pytest.mark.parametrize("birth_date, expected", [
    # exactly 18 years old
    ((datetime.now() - timedelta(days=18*365)).strftime("%d-%m-%Y"), "You are of age"),
    # under 18
    ((datetime.now() - timedelta(days=17*365)).strftime("%d-%m-%Y"), "You are underage"),
    # older than 18
    ((datetime.now() - timedelta(days=19*365)).strftime("%d-%m-%Y"), "You are of age"),
])
def test_age_verification(driver, birth_date, expected):
    driver.get(AUTH_URL)

    # login first
    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    # open shop modal and enter DOB
    shopping_page = ShopPage(driver)
    shopping_page.open_shop_modal()
    shopping_page.handle_age_verification(birth_date)

    # check toast result
    assert expected in shopping_page.get_toast_message()


def test_age_verification_empty_date(driver):
    driver.get(AUTH_URL)

    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    shopping_page = ShopPage(driver)
    shopping_page.open_shop_modal()
    shopping_page.handle_age_verification("")  # empty DOB

    assert "Please enter your birth date" in shopping_page.get_toast_message()


def test_age_verification_invalid_format(driver):
    driver.get(AUTH_URL)

    login_page = LoginPage(driver)
    login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    shopping_page = ShopPage(driver)
    shopping_page.open_shop_modal()
    shopping_page.handle_age_verification(INVALID_DOB)  # e.g. "1999/01/01"

    assert "Please enter your birth date" in shopping_page.get_toast_message()
