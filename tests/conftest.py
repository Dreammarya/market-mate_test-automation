import pytest
from selenium import webdriver

print("=== CONFTEST.PY IS LOADING ===")

@pytest.fixture(scope="function")  
def driver():
    """Create a new Chrome browser for each test"""
    print("=== CREATING DRIVER ===")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    print("=== DRIVER CREATED ===")
    
    yield driver
    
    print("=== CLEANING UP DRIVER ===")
    try:
        driver.quit()
    except Exception as e:
        print(f"Error during cleanup: {e}")

print("=== CONFTEST.PY LOADED ===")
