from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helpers.cart_utils import open_shop_and_handle_dob
from config import STORE_URL


class RatingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)   # ✅ added for reuse

    def open_product_from_shop(self, product_name):
        self.driver.get(STORE_URL)
        open_shop_and_handle_dob(self.driver)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//img[@alt='{product_name}']"))
        ).click()

    def delete_existing_rating_if_exists(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@class='comment']//div[@class='menu-icon'])[1]"))
            ).click()
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-menu']//button[text()='Delete']"))
            ).click()

            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            print("Alert accepted – review deleted.")
        except:
            print("No review to delete or alert was not displayed.")

    def rate_product(self, stars):
        xpath = f"//div[@class='interactive-rating']//span[contains(@class, 'star')][{stars}]"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()

    def submit_review(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'new-review-btn-send')]"))
        ).click()

    def verify_rating_success_message(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//p[contains(text(), 'You have already reviewed this product')]"
                ))
            )
            print("Rating submitted – already reviewed message is displayed.")
        except:
            raise AssertionError("No message indicating rating was submitted – something is wrong.")

    def verify_error_message(self, expected_text):
        # ✅ fixed: removed missing wait_for_element, replaced with standard wait
        try:
            xpath = f'//*[contains(text(), "{expected_text}")]'
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            assert expected_text in element.text
        except:
            raise AssertionError(f"The expected error message was not found: '{expected_text}'")

    def close_cart_overlay_if_present(self):
        try:
            overlay = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'cart-modal')]"))
            )
            close_btn = overlay.find_element(By.XPATH, ".//button[contains(text(),'Close') or contains(text(),'×')]")
            close_btn.click()
            print("Closed cart overlay before rating.")
        except TimeoutException:
            pass
