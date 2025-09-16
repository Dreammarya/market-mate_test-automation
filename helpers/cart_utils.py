import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.shopping_page import ShopPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage


# ==========================
# CONFIG & TEST DATA
# ==========================

BASE_URL = "https://grocerymate.masterschool.com"
AUTH_URL = f"{BASE_URL}/auth"
STORE_URL = f"{BASE_URL}/store"
CHECKOUT_URL = f"{BASE_URL}/checkout"
CART_URL = f"{BASE_URL}/cart"

# Timeouts (in seconds)
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
LONG_TIMEOUT = 20  

# Test checkout data
TEST_CHECKOUT_DATA = {
    "street": "Test str. 1",
    "city": "Test",
    "postcode": "12323",
    "card_number": "1111111111111111",
    "card_name": "Maria Lazar",
    "card_expiry": "12/2032",
    "card_cvc": "123"
}

# Test user credentials
TEST_USER_CREDENTIALS = {
    "email": "maria3@gmail.com",
    "password": "maria3"
}

# Date of birth values
TEST_DOB = "01-01-2005"     # valid (18+)
INVALID_DOB = "32-12-2005"  # invalid

# Sample products used in tests
TEST_PRODUCTS = {
    "rating_product": "Ginger",
    "shipping_product": "Ginger",
    "cheap_product": "Kale"
}

# Expected shipping costs for different cart totals
SHIPPING_COST_EXPECTED = {
    "below_30": "8.00 €",
    "equal_30": "0.00 €",
    "above_30": "0.00 €"
}


# ==========================
# SHOP HELPERS
# ==========================

def open_shop_and_handle_dob(driver):
    """
    Opens the Store page and handles the Date of Birth modal if it appears.
    """
    shop_page = ShopPage(driver)
    shop_page.open_store_page()

    try:
        shop_page.enter_date_of_birth("10-10-1990")
        shop_page.submit_age_verification()
        time.sleep(3)  # Wait for redirection after DOB check
        driver.get(STORE_URL)  # Ensure we are back on the Store
        time.sleep(3)
    except Exception:
        print("ℹ️ No Date of Birth verification was required.")


def add_items_to_cart(driver, product_name, quantity):
    """
    Adds a specific product to the cart multiple times.
    """
    for _ in range(quantity):
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//img[@alt='{product_name}']/ancestor::div[contains(@class, 'product-card')]"
                f"//button[contains(., 'Add to Cart')]"
            ))
        ).click()
        time.sleep(0.5)  # brief pause to allow UI update


def clear_cart(driver):
    """
    Removes all items from the cart, if any exist.
    """
    driver.get(CHECKOUT_URL)
    try:
        while True:
            remove_btn = WebDriverWait(driver, SHORT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='remove-icon']"))
            )
            remove_btn.click()
            time.sleep(1)
    except Exception:
        print("ℹ️ Cart is already empty or no items remain.")


def buy_product(driver, product_name):
    """
    Logs in, opens the shop, adds a product to the cart,
    fills out checkout details, and completes the purchase.
    """
    # Step 1: Login
    driver.get(AUTH_URL)
    login = LoginPage(driver)
    login.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])

    # Step 2: Enter the store and handle DOB check if required
    open_shop_and_handle_dob(driver)

    # Step 3: Add one product to the cart
    add_items_to_cart(driver, product_name, quantity=1)

    # Step 4: Go to Checkout
    driver.get(CHECKOUT_URL)
    driver.refresh()

    # Step 5: Enter checkout details
    checkout = CheckoutPage(driver)
    checkout.enter_checkout_details(
        street=TEST_CHECKOUT_DATA["street"],
        city=TEST_CHECKOUT_DATA["city"],
        zip_code=TEST_CHECKOUT_DATA["postcode"],
        card_number=TEST_CHECKOUT_DATA["card_number"],
        name_on_card=TEST_CHECKOUT_DATA["card_name"],
        expiry=TEST_CHECKOUT_DATA["card_expiry"],
        cvc=TEST_CHECKOUT_DATA["card_cvc"]
    )
    checkout.click_buy_now()   # NOTE: may be skipped if handled automatically
    print("🛍️ Purchase completed.")


def ensure_product_purchased(driver, product_name):
    """
    Ensures a product has been purchased:
    - If 'Rate this product' option is visible, assume product is already purchased.
    - Otherwise, trigger a purchase process.
    """
    driver.get(STORE_URL)
    open_shop_and_handle_dob(driver)

    try:
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, f"//img[@alt='{product_name}']"))
        ).click()

        WebDriverWait(driver, SHORT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'interactive-rating')]"))
        )
        print("✅ Product already purchased – no new purchase required.")
    except Exception:
        print("ℹ️ Product not yet purchased – starting purchase flow.")
        buy_product(driver, product_name)


def go_to_product_detail(driver, product_name):
    """
    Navigates to the Store, handles DOB modal if present,
    and opens the product detail page for a given product.
    """
    driver.get(STORE_URL)
    open_shop_and_handle_dob(driver)

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@alt='{product_name}']"))
    ).click()
