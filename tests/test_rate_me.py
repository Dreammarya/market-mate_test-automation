import pytest
from helpers.product_fixtures import purchase_product_once
from pages.rateproduct_page import RatingPage

from config import TEST_PRODUCTS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time


# ---------- Helper ----------
def wait_and_click(driver, element):
    """Tries to click, falls back to JS if intercepted"""
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def safe_click_with_js(driver, locator, timeout=10):
    """Enhanced safe click function with better error handling"""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )
    
    # Scroll to element first
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)  # Wait for scroll to complete
    
    try:
        element.click()
    except ElementClickInterceptedException:
        print("Click intercepted, using JavaScript click...")
        driver.execute_script("arguments[0].click();", element)
    
    return element


# ---------- Tests ----------

# 1st, 2nd, 3rd Test Cases - Verify that a user can submit a valid product rating (1 to 5 stars).
@pytest.mark.parametrize("stars", [1, 2, 3, 4, 5])
def test_user_can_rate_and_cleanup(driver, purchase_product_once, stars):
    rating_page = RatingPage(driver)
    
    # Open product page
    rating_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])
    
    # Delete any existing rating
    rating_page.delete_existing_rating_if_exists()
    
    # Close any cart overlay that might be blocking elements
    try:
        rating_page.close_cart_overlay_if_present()
    except:
        pass  # No overlay to close
    
    # Rate the product with enhanced click handling
    star_xpath = f"//div[@class='interactive-rating']//span[contains(@class,'star')][{stars}]"
    safe_click_with_js(driver, (By.XPATH, star_xpath))
    
    # Submit the review
    submit_xpath = "//button[contains(@class, 'new-review-btn-send')]"
    safe_click_with_js(driver, (By.XPATH, submit_xpath))
    
    # Verify success
    rating_page.verify_rating_success_message()
    
    # Clean up
    rating_page.delete_existing_rating_if_exists()
    print(f"A rating of {stars} stars has been submitted.")


# 4th Test Case - Verify system behavior when the user does not select a rating
def test_user_cannot_submit_rating_without_selecting(driver, purchase_product_once):
    rating_page = RatingPage(driver)
    
    # Open product page
    rating_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])
    
    # Delete any existing rating
    rating_page.delete_existing_rating_if_exists()
    
    # Close any cart overlay
    try:
        rating_page.close_cart_overlay_if_present()
    except:
        pass
    
    # Try to submit without selecting rating
    submit_xpath = "//button[contains(@class, 'new-review-btn-send')]"
    safe_click_with_js(driver, (By.XPATH, submit_xpath))
    
    # Verify error message
    rating_page.verify_error_message("Invalid input for the field 'Rating'")
    print("Review cannot be submitted without a star rating – error has been shown.")


# 5th Test Case - Verify system behavior when user submits multiple ratings
def test_user_cannot_rate_same_product_twice(driver, purchase_product_once):
    rating_page = RatingPage(driver)
    
    # Open product page
    rating_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])
    
    # Delete any existing rating
    rating_page.delete_existing_rating_if_exists()
    
    # Close any cart overlay
    try:
        rating_page.close_cart_overlay_if_present()
    except:
        pass
    
    # Submit first rating
    star_xpath = f"//div[@class='interactive-rating']//span[contains(@class,'star')][4]"
    safe_click_with_js(driver, (By.XPATH, star_xpath))
    
    submit_xpath = "//button[contains(@class, 'new-review-btn-send')]"
    safe_click_with_js(driver, (By.XPATH, submit_xpath))
    
    rating_page.verify_rating_success_message()
    print("The first review has been successfully submitted.")
    
    # Refresh page and try to submit again
    driver.refresh()
    time.sleep(2)  # Wait for page to load
    
    # Check for duplicate review message
    rating_page.verify_error_message("You have already reviewed this product")
    print("A message preventing a second rating has been shown.")