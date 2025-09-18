import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.shopping_page import ShopPage
from pages.checkout_page import CheckoutPage
from config import TEST_USER_CREDENTIALS


@pytest.mark.usefixtures("driver", "config")
def test_shipping_cost_threshold(driver, config):
    """
    Verify that free shipping applies above €20,
    and reverts to €5 when cart subtotal drops below €20.
    """

    wait = WebDriverWait(driver, 15)

    # Step 1: Login and go to store
    LoginPage(driver).login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])
    shopping_page = ShopPage(driver)
    shopping_page.open_store()
    shopping_page.handle_age_verification("01-01-2000")

    # Step 2: Add products until subtotal > €20
    unit_price = shopping_page.get_first_product_price()
    qty_needed = (20 // unit_price) + 2  # add buffer above 20€
    shopping_page.add_first_product_to_cart(qty_needed)

    # Step 3: Check free shipping
    checkout = CheckoutPage(driver)
    checkout.open_checkout()
    shipping = checkout.read_shipping_cost()
    assert "0" in shipping or "Free" in shipping, f"❌ Expected free shipping, got: {shipping}"

    # Step 4: Reduce quantity until subtotal < 20
    while checkout.get_subtotal_amount() >= 20:
        checkout.decrease_quantity()

    # Step 5: Verify shipping is €5
    shipping = checkout.read_shipping_cost()
    assert "5" in shipping or "5.00" in shipping, f"❌ Expected €5 shipping, got: {shipping}"

    # Step 6: Cleanup
    checkout.clear_cart()
