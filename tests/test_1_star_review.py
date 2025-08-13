import time
import pytest
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage


@pytest.mark.usefixtures('driver', 'config')
def test_complete_purchase_and_review_workflow(driver, config):
    """
    End-to-end test: Login, purchase product, and submit review with verification.
    """

    TIMEOUT = 20
    BIRTH_DATE = "01-01-2000"
    REVIEWER_NAME = "AutoTestG"
    STAR_RATING = 4

    # Setup webdriver wait
    wait = WebDriverWait(driver, TIMEOUT)

    # Login sequence
    login_handler = LoginPage(driver)
    login_handler.login(config["email"], config["password"])
    wait.until(EC.url_to_be("https://grocerymate.masterschool.com/"))

    # Store navigation and age verification
    shop_handler = ShopPage(driver)
    shop_handler.open_store()
    shop_handler.handle_age_verification(BIRTH_DATE)

    # Get product information
    product_card = shop_handler.get_first_product_card()
    qty_field = product_card.find_element(By.XPATH, ".//input[contains(@class, 'quantity')]")
    product_id = qty_field.get_attribute("name").split("_", 1)[1]

    # Purchase workflow
    shop_handler.add_first_product_to_cart()
    time.sleep(1.5)

    purchase_handler = CheckoutPage(driver)
    purchase_handler.buy()

    # Navigate back to product page
    shop_handler.open_store()
    review_page = ProductPage(driver)
    review_page.load(product_id)

    # Submit review
    review_page.remove_existing_review()
    unique_comment = f"{REVIEWER_NAME} - {STAR_RATING}-star review - {uuid4().hex[:6]}"
    review_page.select_star_rating(STAR_RATING)
    review_page.enter_review_text(unique_comment)
    review_page.submit_review()

    # Verify review submission
    time.sleep(2)
    has_review = review_page.user_has_comment(REVIEWER_NAME)
    assert has_review, f"Review verification failed for user: {REVIEWER_NAME}"

    # Test cleanup
    purchase_handler.clear_cart()