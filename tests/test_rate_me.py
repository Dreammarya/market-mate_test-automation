import pytest
from helpers.product_fixtures import purchase_product_once
from pages.rateproduct_page import RatingPage
from config import TEST_PRODUCTS


# ---------- Helper ----------
def wait_and_click(driver, element):
    """Tries to click, falls back to JS if intercepted"""
    from selenium.common.exceptions import ElementClickInterceptedException
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


# ---------- Tests ----------

# 1st, 2nd, 3rd Test Cases - Verify that a user can submit a valid product rating (1 to 5 stars).
@pytest.mark.parametrize("stars", [1, 2, 3, 4, 5])
def test_user_can_rate_and_cleanup(driver, purchase_product_once, stars):
    rating_page = RatingPage(driver)
    rating_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])
    rating_page.delete_existing_rating_if_exists()
    rating_page.rate_product(stars)
    rating_page.submit_review()
    rating_page.verify_rating_success_message()
    rating_page.delete_existing_rating_if_exists()
    print(f"✅ A rating of {stars} stars has been submitted.")

def rate_product(self, stars):
    self.close_cart_overlay_if_present()
    xpath = f"//div[@class='interactive-rating']//span[contains(@class,'star')][{stars}]"
    locator = (By.XPATH, xpath)
    self.safe_click(locator)



# 4th Test Case - Verify system behavior when the user does not select a rating
def test_user_cannot_submit_rating_without_selecting(driver, purchase_product_once):
    rating_page = RatingPage(driver)
    rating_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])
    rating_page.delete_existing_rating_if_exists()
    rating_page.submit_review()
    rating_page.verify_error_message("Invalid input for the field 'Rating'")
    print("❌ Review cannot be submitted without a star rating – error has been shown.")


# 5th Test Case - Verify system behavior when user submits multiple ratings
def test_user_cannot_rate_same_product_twice(driver, purchase_product_once):
    rating_page = RatingPage(driver)
    rating_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])
    rating_page.delete_existing_rating_if_exists()
    rating_page.rate_product(4)
    rating_page.submit_review()
    rating_page.verify_rating_success_message()
    print("✅ The first review has been successfully submitted.")

    driver.refresh()

    rating_page.verify_error_message("You have already reviewed this product")
    print("✅ A message preventing a second rating has been shown.")
