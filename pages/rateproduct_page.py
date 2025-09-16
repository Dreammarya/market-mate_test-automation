from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.cart_utils import open_shop_and_handle_dob
from config import STORE_URL


class RatingPage:
    def __init__(self, driver):
        """Initialize the RatingPage with WebDriver instance and default wait time."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Set default wait time to 10 seconds

    def open_product_from_shop(self, product_name):
        """
        Navigate to the store and open a specific product.
        
        Steps:
        1. Navigate to the store URL
        2. Handle the date of birth modal if present
        3. Click on the product by its image alt text
        """
        # Navigate to the main store page
        self.driver.get(STORE_URL)
        
        # Handle any date of birth verification modal that appears
        open_shop_and_handle_dob(self.driver)
        
        # Wait for the product image to be clickable and click it
        product = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//img[@alt='{product_name}']"))
        )
        product.click()

    def delete_existing_rating_if_exists(self):
        """
        Remove any existing review for the current product.
        
        This method handles the case where a user has already reviewed
        the product and needs to delete it before submitting a new one.
        """
        try:
            # Step 1: Click on the menu icon (three dots) of the existing review
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//div[@class='comment']//div[@class='menu-icon'])[1]")
                )
            ).click()
            
            # Step 2: Click the 'Delete' option from the dropdown menu
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='dropdown-menu']//button[text()='Delete']")
                )
            ).click()
            
            # Step 3: Handle the confirmation alert that appears
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()  # Confirm deletion
            
            print("Old review deleted successfully.")
            
        except:
            # If no existing review is found or deletion fails, continue silently
            print("No existing review found to delete.")

    def rate_product(self, stars: int):
        """
        Select a star rating for the product.
        
        Args:
            stars (int): Number of stars to select (1-5)
        
        The method locates the interactive rating component and clicks
        on the specified star number.
        """
        # Build XPath to target the specific star number in the rating component
        xpath = f"//div[@class='interactive-rating']//span[contains(@class, 'star')][{stars}]"
        
        # Wait for the star element to be clickable and click it
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def submit_review(self):
        """
        Submit the review by clicking the send button.
        
        This method locates the review submission button and clicks it
        to send the rating to the server.
        """
        # Wait for the submit button to be clickable and click it
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'new-review-btn-send')]")
            )
        ).click()

    def verify_rating_success_message(self):
        """
        Verify that a success message appears after review submission.
        
        This method checks for a message indicating the review was submitted
        or that the user has already reviewed the product.
        
        Raises:
            AssertionError: If no success message is found
        """
        try:
            # Wait for the success message to appear on the page
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(), 'You have already reviewed this product')]")
                )
            )
            print("Review submitted message is displayed.")
            
        except:
            # If no success message is found, raise an assertion error
            raise AssertionError("No review submitted message found!")

    def verify_error_message(self, expected_text: str):
        """
        Verify that a specific error message appears on the page.
        
        Args:
            expected_text (str): The error message text to look for
            
        This method searches for any element containing the expected error text
        and confirms it matches what we expect to see.
        
        Raises:
            AssertionError: If the expected error message is not found
        """
        try:
            # Build XPath to find any element containing the expected error text
            xpath = f'//*[contains(text(), "{expected_text}")]'
            
            # Wait for the error element to be visible
            error_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            
            # Verify the error text is actually present in the element
            assert expected_text in error_element.text
            
            print(f"Error message shown: {expected_text}")
            
        except:
            # If error message is not found, raise an assertion error
            raise AssertionError(f"Expected error message not found: '{expected_text}'")