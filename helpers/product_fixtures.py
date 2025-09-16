import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from config import (
    AUTH_URL,
    STORE_URL,
    TEST_USER_CREDENTIALS,
    SHORT_TIMEOUT,
    DEFAULT_TIMEOUT,
    TEST_DOB,
    TEST_CHECKOUT_DATA,
)


@pytest.fixture(scope="function")
def purchase_product_once(driver):
    # Navigate to login page
    driver.get(AUTH_URL)

    # Log in with test credentials
    LoginPage(driver).login(TEST_USER_CREDENTIALS)

    # Open the store
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/store']"))
    ).click()

    # Enter DOB confirmation if prompted
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='DD-MM-YYYY']"))
        ).send_keys(TEST_DOB)

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirm']"))
        ).click()
    except Exception:
        print("Datum rođenja nije tražen.")

    # Add Gala Apples to cart
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//img[@alt='Gala Apples']/ancestor::div[@class='card']//button[contains(text(), 'Add to Cart')]")
        )
    ).click()

    # Open the cart
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@class='headerIcon'])[3]"))
    ).click()

    # Fill in checkout form
    checkout = CheckoutPage(driver)
    checkout.enter_checkout_details(
        street=TEST_CHECKOUT_DATA["street"],
        city=TEST_CHECKOUT_DATA["city"],
        zip_code=TEST_CHECKOUT_DATA["postcode"],
        card_number=TEST_CHECKOUT_DATA["card_number"],
        name_on_card=TEST_CHECKOUT_DATA["card_name"],
        expiry=TEST_CHECKOUT_DATA["card_expiry"],
        cvc=TEST_CHECKOUT_DATA["card_cvc"],
    )
    checkout.click_buy_now()

    print("✅ Product was purchased once for all dependent tests.")

    # Wait briefly to ensure purchase is processed
    time.sleep(3)

    # Ensure the driver returns to the store (manual navigation required)
    driver.get(STORE_URL)
