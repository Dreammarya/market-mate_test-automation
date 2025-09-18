import pytest
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.product_fixtures import purchase_product_once
from pages.login_page import LoginPage
from pages.shopping_page import ShopPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from config import AUTH_URL, TEST_USER_CREDENTIALS


@pytest.mark.usefixtures("driver", "config")
def test_review_no_star_submission(driver, config):
    """
    Verify that submitting a review without selecting stars
    does not create a review entry.
    """

    wait = WebDriverWait(driver, 15)

    # Step 1: Login and handle age gate
    LoginPage(driver).login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])
    shopping_page = ShopPage(driver)
    shopping_page.open_store()
    shopping_page.handle_age_verification("01-01-2005")

    # Step 2: Select first product & get product_id
    product_element = shopping_page.get_first_product_card()
    product_id = product_element.find_element(By.XPATH, ".//input[contains(@class,'quantity')]")\
                                .get_attribute("name").split("_", 1)[1]

    # Step 3: Add product and purchase
    shopping_page.add_first_product_to_cart()
    checkout = CheckoutPage(driver)
    checkout.buy()

    # Step 4: Open product details
    product_page = ProductPage(driver)
    product_page.load(product_id)

    # Step 5: Ensure no leftover review & attempt no-star review
    product_page.remove_existing_review()
    comment = f"autotest_no_star_{uuid4().hex[:6]}"
    product_page.enter_review_text(comment)
    product_page.submit_review()

    # Step 6: Assert no review is saved
    wait.until_not(EC.presence_of_all_elements_located(
        (By.XPATH, f"//div[contains(@class,'review') and contains(., '{comment}')]")
    ))
    assert not product_page.user_has_comment(TEST_USER_CREDENTIALS["email"].split("@")[0]), \
        "❌ Review unexpectedly saved without star rating."

    # Step 7: Cleanup
    checkout.clear_cart()
