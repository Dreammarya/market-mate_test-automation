from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class ShopPage:
    # Page element locators
    STORE_XPATH = (By.XPATH, "//a[@href='/store']")
    DOB_XPATH = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    CONFIRM_BUTTON_XPATH = (By.XPATH, "//div[@class='modal-content']//button[text() = 'Confirm']")
    
    AGE_VERIFICATION_ERROR_XPATH = (By.XPATH, "//div[contains(text(),'underage')]")
    TOAST_MESSAGE = (By.CLASS_NAME, "toast-message")
    ALERT_MESSAGE = (By.CLASS_NAME, "alert")

    # Known overlay selector (update if needed)
    OVERLAY = (By.CSS_SELECTOR, "div.go2072408551")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.short_wait = WebDriverWait(driver, 5)

    # ---------- Generic safe click ----------
    def safe_click(self, locator):
        """Scrolls into view, waits for clickability, retries if an overlay intercepts."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            print("⚠️ Click intercepted — waiting for overlay to disappear...")
            try:
                WebDriverWait(self.driver, 5).until_not(
                    EC.presence_of_element_located(self.OVERLAY)
                )
            except TimeoutException:
                print("Overlay did not disappear, using JS click instead.")
            self.driver.execute_script("arguments[0].click();", element)

    # ---------- Page actions ----------
    def open_store_page(self):
        """Alias for compatibility with tests"""
        self.safe_click(self.STORE_XPATH)

    def click_store_link(self):
        """Original method kept for compatibility"""
        self.open_store_page()
    
    def try_empty_date_submission(self):
        """Try to submit DOB modal without filling the date (for negative test)."""
        try:
            self.safe_click(self.CONFIRM_BUTTON_XPATH)
            print("✅ Tried submitting DOB form with empty date.")
        except TimeoutException:
            print("ℹ️ DOB confirm button not found — modal may not be displayed.")
    

    def fill_birth_date(self, birth_date):
        date_input = self.wait.until(EC.presence_of_element_located(self.DOB_XPATH))
        date_input.clear()
        date_input.send_keys(birth_date)
        print(f"Entered birth date: {birth_date}")

    def click_confirm_button(self):
        self.safe_click(self.CONFIRM_BUTTON_XPATH)

    def read_error_message(self):
        for locator in [self.AGE_VERIFICATION_ERROR_XPATH, self.TOAST_MESSAGE, self.ALERT_MESSAGE]:
            try:
                error_msg = self.short_wait.until(EC.visibility_of_element_located(locator))
                if error_msg.text.strip():
                    return error_msg.text
            except TimeoutException:
                continue
        return ""

    def complete_age_verification(self, birth_date):
        print("Starting age verification...")
        self.open_store_page()
        try:
            self.fill_birth_date(birth_date)
            self.click_confirm_button()
        except TimeoutException:
            print("No DOB modal appeared — skipping.")
