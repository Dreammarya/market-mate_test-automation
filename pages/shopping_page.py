from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ShopPage:
    # Page element locators
    STORE_XPATH = (By.XPATH, "//a[@href='/store']")
    DOB_XPATH = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    CONFIRM_BUTTON_XPATH = (By.XPATH, "//div[@class='modal-content']//button[text() = 'Confirm']")
    AGE_VERIFICATION_ERROR_XPATH = (By.XPATH, "//div[contains(text(),'underage')]")
 

    def __init__(self, driver):
        """Initialize the ShopPage with a WebDriver instance"""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Default wait time
        self.short_wait = WebDriverWait(driver, 5)  # For quick elements
    
    def click_store_link(self):
        """Click on the store link to navigate to the shop"""
        try:
            store_link = self.wait.until(
                EC.element_to_be_clickable(self.STORE_XPATH)
            )
            store_link.click()
            print("Successfully clicked store link")
        except TimeoutException:
            print("Could not find or click the store link")
            raise
    
    def fill_birth_date(self, birth_date):
        """Enter the date of birth in the age verification form"""
        try:
            date_input = self.wait.until(
                EC.presence_of_element_located(self.DOB_XPATH)  # FIXED: was DATE_OF_BIRTH_INPUT
            )
            date_input.clear()  # Clear any existing text
            date_input.send_keys(birth_date)
            print(f"Entered birth date: {birth_date}")
        except TimeoutException:
            print("Date of birth input field not found")
            raise
    
    def click_confirm_button(self):
        """Click the confirm button to submit age verification"""
        try:
            confirm_btn = self.short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_BUTTON_XPATH)
            )
            confirm_btn.click()
            print("Clicked confirm button for age verification")
        except TimeoutException:
            print("Confirm button not found or not clickable")
            raise
    
    def read_error_message(self):
        """Get the text from any error message that appears"""
        try:
            error_msg = self.short_wait.until(
                EC.visibility_of_element_located(self.AGE_VERIFICATION_ERROR_XPATH)  # FIXED: was UNDERAGE_MESSAGE
            )
            message_text = error_msg.text
            print(f"Found error message: {message_text}")
            return message_text
        except TimeoutException:
            print("No error message found")
            return ""
    
    def complete_age_verification(self, birth_date):
        """Complete the full age verification process"""
        print("Starting age verification process...")
        self.click_store_link()
        
        try:
            self.fill_birth_date(birth_date)
            self.click_confirm_button()
            print("Age verification completed successfully")
        except TimeoutException:
            print("Age verification modal may not have appeared")
            # This is okay - sometimes the modal doesn't show
    
    def try_empty_date_submission(self):
        """Test submitting age verification with no date entered"""
        print("Testing empty date submission...")
        self.click_store_link()
        
        try:
            # Try to click confirm without entering a date
            self.click_confirm_button()
            print("Submitted empty date form")
        except TimeoutException:
            print("Could not submit empty date - confirm button not available")
    
    def check_if_age_modal_appears(self):
        """Check if the age verification modal shows up"""
        try:
            self.short_wait.until(
                EC.presence_of_element_located(self.DOB_XPATH)  # FIXED: was DATE_OF_BIRTH_INPUT
            )
            print("Age verification modal appeared")
            return True
        except TimeoutException:
            print("No age verification modal found")
            return False