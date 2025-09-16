from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHECKOUT_URL


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        # locator for shipping cost info
        self.shipping_info = (By.XPATH, "//div[contains(@class, 'shipping-cost')]")
        # locator for remove button in cart
        self.remove_icon = (By.XPATH, "//a[@class='remove-icon']")

    def clear_cart(self):
        # go to checkout page
        self.driver.get(CHECKOUT_URL)
        # keep clicking remove buttons until no more items left
        while True:
            try:
                remove_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.remove_icon)
                )
                remove_btn.click()
            except:
                # if no remove button found, cart is empty
                break

    def get_shipping_text(self):
        # wait until shipping info is visible and return its text
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.shipping_info)
        ).text
