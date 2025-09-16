import pytest
from pages.rateproduct_page import RatingPage
from pages.login_page import LoginPage
from config import TEST_PRODUCTS
from helpers.rating_utils import delete_existing_review  # <-- new import


# 1st, 2nd, 3rd Test Cases - check that a user can rate a product (1 to 5 stars)
@pytest.mark.parametrize("stars", [1, 2, 3, 4, 5])
def test_user_can_rate_and_cleanup(driver, purchase_product_once, stars):
    rateproduct_page = RatingPage(driver)

    # open product page
    rateproduct_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])

    # cleanup – remove old rating if exists
    delete_existing_review(driver)

    # give stars
    rateproduct_page.rate_product(stars)

    # submit the review
    rateproduct_page.submit_review()

    # check success message
    rateproduct_page.verify_rating_success_message()

    # cleanup again – remove rating
    delete_existing_review(driver)

    print(f"✅ A rating of {stars} stars has been submitted and cleaned up.")


# 4th Test Case - try to submit without selecting stars
def test_user_cannot_submit_rating_without_selecting(driver, purchase_product_once):
    rateproduct_page = RatingPage(driver)

    # open product page
    rateproduct_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])

    # cleanup old rating
    delete_existing_review(driver)

    # directly click submit (without stars)
    rateproduct_page.submit_review()

    # check error message
    rateproduct_page.verify_error_message("Invalid input for the field 'Rating'")

    print("⚠️ Review cannot be submitted without a star rating – correct error shown.")


# 5th Test Case - try to rate same product twice
def test_user_cannot_rate_same_product_twice(driver, purchase_product_once):
    rateproduct_page = RatingPage(driver)

    # open product page
    rateproduct_page.open_product_from_shop(TEST_PRODUCTS["rating_product"])

    # cleanup old rating
    delete_existing_review(driver)

    # submit first review
    rateproduct_page.rate_product(4)
    rateproduct_page.submit_review()
    rateproduct_page.verify_rating_success_message()
    print("✅ The first review has been submitted.")

    # refresh and try again
    driver.refresh()

    # check error message for duplicate review
    rateproduct_page.verify_error_message("You have already reviewed this product")
    print("⚠️ Second review blocked – correct error message displayed.")
