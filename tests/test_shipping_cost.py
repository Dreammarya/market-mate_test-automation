import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.shopping_page import ShopPage
from pages.checkout_page import CheckoutPage
from helpers.cart_utils import clear_cart, add_items_to_cart, open_shop_and_handle_dob
from config import AUTH_URL, STORE_URL, CHECKOUT_URL, TEST_PRODUCTS, TEST_USER_CREDENTIALS

def test_shipping_cost_threshold(driver):
    """
    Verify that free shipping applies above €20,
    and reverts to €5 when cart subtotal drops below €20.
    """
    
    wait = WebDriverWait(driver, 15)
    
    # Step 1: Login and go to store
    driver.get(AUTH_URL)
    LoginPage(driver).login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])
    
    # Step 2: Open shop and handle age verification
    open_shop_and_handle_dob(driver)
    
    # Step 3: Clear cart to start fresh
    clear_cart(driver)
    driver.get(STORE_URL)
    
    # Step 4: Add enough products to get above €20 (assuming each product costs around €2)
    add_items_to_cart(driver, TEST_PRODUCTS["shipping_product"], 11)  # Should be above €20
    
    # Step 5: Go to checkout and check free shipping
    driver.get(CHECKOUT_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'shipment-container')]"))
    )
    
    checkout = CheckoutPage(driver)
    shipping = checkout.get_shipping_cost()
    assert "0€" in shipping or "free" in shipping.lower(), f"Expected free shipping, got: {shipping}"
    
    # Step 6: Reduce quantity to get below €20
    checkout.click_minus_button_multiple_times(3)  # Remove 3 items
    
    # Step 7: Wait for shipping cost to update and verify it's now paid
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "//div[contains(@class, 'shipment-container')]"), "€"
        )
    )
    
    updated_shipping = checkout.get_updated_shipping_after_refresh()
    assert "5" in updated_shipping or "8" in updated_shipping, f"Expected paid shipping (5€ or 8€), got: {updated_shipping}"
    
    # Step 8: Cleanup
    clear_cart(driver)