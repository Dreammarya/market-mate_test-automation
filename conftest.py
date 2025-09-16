import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from config import AUTH_URL, TEST_USER_CREDENTIALS, TEST_CHECKOUT_DATA, TEST_DOB, DEFAULT_TIMEOUT, SHORT_TIMEOUT, STORE_URL

@pytest.fixture(scope="function")
def driver():
    """Create a new Chrome browser for each test"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    yield driver
    
    # Clean up after test
    try:
        driver.delete_all_cookies()
        driver.quit()
    except Exception as e:
        print(f"Error during cleanup: {e}")
        
@pytest.fixture
def config():
    return {"base_url": "http://localhost:5000"}

@pytest.fixture(scope="function")
def purchase_product_once(driver):
    """Login user and purchase a product so they can leave reviews"""
    
    try:
        # Step 1: Go to login page and login
        driver.get(AUTH_URL)
        login_page = LoginPage(driver)
        login_page.login(TEST_USER_CREDENTIALS["email"], TEST_USER_CREDENTIALS["password"])
        print("User logged in successfully")
        
        # Step 2: Navigate to store
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        store_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/store']"))
        )
        store_link.click()
        print("Navigated to store")
        
        # Step 3: Handle age verification if it appears
        try:
            dob_input = WebDriverWait(driver, SHORT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='DD-MM-YYYY']"))
            )
            dob_input.clear()
            dob_input.send_keys(TEST_DOB)
            
            confirm_button = WebDriverWait(driver, SHORT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirm']"))
            )
            confirm_button.click()
            print("Age verification completed")
            
        except TimeoutException:
            print("Date of birth verification was not required")
        
        # Step 4: Add Gala Apples to cart
        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Gala Apples']/ancestor::div[@class='card']//button[contains(text(), 'Add to Cart')]"))
        )
        add_to_cart_button.click()
        print("Added Gala Apples to cart")
        
        # Step 5: Open shopping cart
        cart_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='headerIcon'])[3]"))
        )
        cart_icon.click()
        print("Opened shopping cart")
        
        # Step 6: Complete checkout process
        checkout_page = CheckoutPage(driver)
        checkout_page.enter_checkout_details(
            street=TEST_CHECKOUT_DATA["street"],
            city=TEST_CHECKOUT_DATA["city"],
            zip_code=TEST_CHECKOUT_DATA["postcode"],
            card_number=TEST_CHECKOUT_DATA["card_number"],
            name_on_card=TEST_CHECKOUT_DATA["card_name"],
            expiry=TEST_CHECKOUT_DATA["card_expiry"],
            cvc=TEST_CHECKOUT_DATA["card_cvc"]
        )
        print("Entered checkout details")
        
        checkout_page.click_buy_now()
        print("Purchase completed successfully")
        
        # Step 7: Wait a moment and return to store
        time.sleep(3)
        driver.get(STORE_URL)
        print("Returned to store page - ready for rating tests")
        
        return driver
        
    except TimeoutException as e:
        print(f"Timeout error during purchase setup: {e}")
        raise
    except NoSuchElementException as e:
        print(f"Element not found during purchase setup: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during purchase setup: {e}")
        raise