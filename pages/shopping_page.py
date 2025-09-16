import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ShopPage:
    """Page object for the Store page and Age Verification modal."""

    _STORE_URL = "https://grocerymate.masterschool.com/store"

    # locators
    _SHOP_BUTTON = (By.XPATH, '//a[@href="/store"]')  # shop link
    _DOB_INPUT = (By.XPATH, "//div[contains(@class, 'modal-content')]//input[@placeholder='DD-MM-YYYY']")  # DOB input
    _CONFIRM_BUTTON = (By.XPATH, '//button[contains(text(), "Confirm")]')  # confirm DOB
    _TOAST = (By.XPATH,
        "//div[contains(text(), 'You are of age')"
        " or contains(text(), 'You are underage')"
        " or contains(text(), 'Please enter your birth date')]"
    )  # toast messages

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.toast_wait = WebDriverWait(driver, 15, poll_frequency=0.5)

    def load(self):
        """just open store page"""
        self.driver.get(self._STORE_URL)

    def open_store(self):
        """go to store, wait for either products or DOB popup"""
        self.driver.get(self._STORE_URL)
        self.wait.until(EC.any_of(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card")),
            EC.presence_of_element_located(self._DOB_INPUT),
        ))

    def open_shop_modal(self):
        """click SHOP and wait for DOB field"""
        self.wait.until(EC.element_to_be_clickable(self._SHOP_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self._DOB_INPUT))

    def handle_age_verification(self, dob: str):
        """type DOB and confirm"""
        field = self.wait.until(EC.visibility_of_element_located(self._DOB_INPUT))
        field.clear()
        field.send_keys(dob)
        self.wait.until(EC.element_to_be_clickable(self._CONFIRM_BUTTON)).click()
        time.sleep(1)  # let UI update

    def get_toast_message(self) -> str:
        """get text of toast"""
        return self.toast_wait.until(EC.presence_of_element_located(self._TOAST)).text

    def toast_message_displayed(self, expected_text: str) -> bool:
        """check if toast has my expected text"""
        try:
            toast = self.toast_wait.until(EC.visibility_of_element_located(self._TOAST))
            return expected_text.lower() in toast.text.lower()
        except Exception:
            return False

    def get_first_product_card(self):
        """find first product card"""
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card")))
        card = self.driver.find_elements(By.CLASS_NAME, "product-card")[0]
        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
        time.sleep(0.3)
        return card

    def get_first_product_price(self) -> float:
        """get price from first product (discount or normal)"""
        card = self.get_first_product_card()
        if card.find_elements(By.CLASS_NAME, "discount-price"):
            price_text = card.find_element(By.CLASS_NAME, "discount-price").text
        else:
            price_text = card.find_element(By.CLASS_NAME, "price").text
        return float(price_text.replace("€", "").strip().replace(",", "."))

    def add_first_product_to_cart(self, quantity: int = 1):
        """add first product with chosen quantity"""
        card = self.get_first_product_card()
        qty_input = card.find_element(By.XPATH, ".//input[contains(@class, 'quantity')]")
        add_btn = card.find_element(By.CSS_SELECTOR, "button.btn-cart")

        qty_input.clear()
        qty_input.send_keys(str(quantity))
        time.sleep(0.5)

        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        add_btn.click()
