from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DEFAULT_TIMEOUT, TEST_CHECKOUT_DATA

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.street_address = (By.XPATH, "//input[@placeholder='Street Address']")
        self.city = (By.XPATH, "//input[@placeholder='City']")
        self.postal_code = (By.XPATH, "//input[@placeholder='Postal Code']")
        self.card_number = (By.XPATH, "//input[@placeholder='Card number']")
        self.card_name = (By.XPATH, "//input[@placeholder='Name on card']")
        self.card_expiry = (By.XPATH, "//input[@placeholder='Expiration']")
        self.card_cvc = (By.XPATH, "//input[@placeholder='Cvv']")
        self.buy_now_button = (By.XPATH, "//button[text()='Buy now']")

    def _wait_and_send_keys(self, locator, text, timeout=DEFAULT_TIMEOUT):
        """Wait for element to be present and type text into it."""
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator)).send_keys(text)

    def _wait_and_click(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for element to be clickable and click it."""
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    # --- Checkout actions ---
    def enter_checkout_details(self, street, city, zip_code, card_number, name_on_card, expiry, cvc):
        """Fill in the checkout form."""
        self._wait_and_send_keys(self.street_address, street)
        self._wait_and_send_keys(self.city, city)
        self._wait_and_send_keys(self.postal_code, zip_code)
        self._wait_and_send_keys(self.card_number, card_number)
        self._wait_and_send_keys(self.card_name, name_on_card)
        self._wait_and_send_keys(self.card_expiry, expiry)
        self._wait_and_send_keys(self.card_cvc, cvc)

    def click_buy_now(self):
        """Click the 'Buy now' button."""
        self._wait_and_click(self.buy_now_button)

    def complete_checkout_with_test_data(self):
        """Fill checkout form with predefined test data and submit."""
        self.enter_checkout_details(
            street=TEST_CHECKOUT_DATA["street"],
            city=TEST_CHECKOUT_DATA["city"],
            zip_code=TEST_CHECKOUT_DATA["postcode"],
            card_number=TEST_CHECKOUT_DATA["card_number"],
            name_on_card=TEST_CHECKOUT_DATA["card_name"],
            expiry=TEST_CHECKOUT_DATA["card_expiry"],
            cvc=TEST_CHECKOUT_DATA["card_cvc"]
        )
        self.click_buy_now()

    # --- Shipping info ---
    def get_shipping_cost(self):
        """Return the displayed shipping cost."""
        shipping_element = WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='shipment-container']/h5[2]"))
        )
        return shipping_element.text.strip()

    def get_updated_shipping_after_refresh(self):
        """Refresh page and return updated shipping cost."""
        self.driver.refresh()
        shipping_element = WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, "//h5[text()='Shipment:']/following-sibling::h5"))
        )
        return shipping_element.text.strip()

    # --- Cart actions ---
    def click_minus_button_multiple_times(self, times):
        """Click the minus button in the cart multiple times."""
        for _ in range(times):
            self._wait_and_click((By.XPATH, "//button[@class='minus']"))
