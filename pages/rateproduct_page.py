from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.cart_utils import open_shop_and_handle_dob
from config import STORE_URL


class RatingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_product_from_shop(self, product_name):
        """Open the shop and navigate to a specific product by its image alt attribute."""
        self.driver.get(STORE_URL)
        open_shop_and_handle_dob(self.driver)

        # wait until overlay disappears (if present)
        self._wait_for_overlay_to_disappear()

        # click on product image (by alt text)
        product = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//img[@alt='{product_name}']"))
        )
        product.click()

    def delete_existing_rating_if_exists(self):
        """Delete an existing rating if one is already present."""
        try:
            menu_icon = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@class='comment']//div[@class='menu-icon'])[1]"))
            )
            menu_icon.click()

            delete_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-menu']//button[text()='Delete']"))
            )
            delete_button.click()

            # handle confirmation alert
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Existing review deleted.")
        except Exception:
            print("No existing review found.")

    def rate_product(self, stars: int):
        """Click on a star rating (1–5)."""
        self._wait_for_overlay_to_disappear()
        xpath = f"//div[@class='interactive-rating']//span[contains(@class, 'star')][{stars}]"
        star = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        star.click()

    def submit_review(self):
        """Click the submit button for a review."""
        self._wait_for_overlay_to_disappear()
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'new-review-btn-send')]"))
        )
        submit_button.click()

    def verify_rating_success_message(self):
        """Verify that a success message is shown after submitting a review."""
        try:
            self.wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//p[contains(text(), 'You have already reviewed this product')]"
                ))
            )
            print("Rating submitted – success message displayed.")
        except Exception:
            raise AssertionError("No success message found after submitting rating.")

    def verify_error_message(self, expected_text: str):
        """Verify that the expected error message is displayed."""
        try:
            xpath = f'//*[contains(text(), "{expected_text}")]'
            error_element = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            assert expected_text in error_element.text
        except Exception:
            raise AssertionError(f"Expected error message not found: '{expected_text}'")

    def _wait_for_overlay_to_disappear(self):
        """Utility method: wait until modal overlay disappears before clicking."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "modal-overlay"))
            )
        except Exception:
            # overlay not found or already gone → continue
            pass
