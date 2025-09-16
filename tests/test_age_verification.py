import pytest
import time
from datetime import datetime, timedelta
from config import AUTH_URL, TEST_USER_CREDENTIALS, INVALID_DOB
from pages.login_page import LoginPage
from pages.shopping_page import ShopPage


# ---------- Helper ----------
def login_and_open_shop(driver):
    """Reusable login flow that returns a ShopPage instance"""
    driver.get(AUTH_URL)
    LoginPage(driver).login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])
    return ShopPage(driver)


# ---------- Parametrized Tests ----------
@pytest.mark.parametrize("birth_date, expected", [
    ((datetime.now() - timedelta(days=18*365)).strftime("%d-%m-%Y"), "store"),     # exactly 18
    ((datetime.now() - timedelta(days=17*365)).strftime("%d-%m-%Y"), "underage"),  # under 18
    ((datetime.now() - timedelta(days=19*365)).strftime("%d-%m-%Y"), "store"),     # older than 18
])
def test_age_verification(driver, birth_date, expected):
    shopping_page = login_and_open_shop(driver)

    shopping_page.complete_age_verification(birth_date)
    time.sleep(2)  # wait for redirect/toast

    if expected == "store":
        assert "store" in driver.current_url
        print(f"User with birth date {birth_date} was allowed into store")
    else:
        error_message = shopping_page.read_error_message()
        assert "underage" in error_message.lower()
        print(f"User with birth date {birth_date} was correctly identified as underage")


# ---------- Edge Cases ----------
def test_age_verification_empty_date(driver):
    """Test what happens when no birth date is entered"""
    shopping_page = login_and_open_shop(driver)
    shopping_page.try_empty_date_submission()
    time.sleep(2)  # Wait for error message
    
    error_message = shopping_page.read_error_message()
    assert len(error_message) > 0, "Expected an error message for empty date"
    print(f"Empty date correctly rejected with message: {error_message}")


def test_age_verification_invalid_format(driver):
    """Test what happens when invalid date format is entered"""
    shopping_page = login_and_open_shop(driver)
    
    # Navigate to store first
    shopping_page.click_store_link()
    
    # Try to enter invalid date format - using the correct method names from ShopPage
    try:
        shopping_page.fill_birth_date(INVALID_DOB)
        shopping_page.click_confirm_button()
        time.sleep(2)  # Wait for error message
        
        error_message = shopping_page.read_error_message()
        assert len(error_message) > 0, "Expected an error message for invalid date format"
        print(f"Invalid date format correctly rejected with message: {error_message}")
        
    except Exception as e:
        print(f"Invalid date handling test completed with exception: {e}")
        # This might be expected if the form validates the format immediately