from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    _EMAIL = (By.XPATH, "//input[@placeholder='Email address']")
    _PASSWORD = (By.XPATH, "//input[@placeholder='Password']")
    _LOGIN_BUTTON = (By.CLASS_NAME, "submit-btn")
    _SHOP_BUTTON = (By.XPATH, "//a[@href='/store']")
    _ERROR_MESSAGE = (By.XPATH, "//*[contains(text(),'Invalid email or password')]")  # ✅ added

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def login(self, email: str, password: str):
        email_field = self.wait.until(EC.presence_of_element_located(self._EMAIL))
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.wait.until(EC.presence_of_element_located(self._PASSWORD))
        password_field.clear()
        password_field.send_keys(password)

        self.wait.until(EC.element_to_be_clickable(self._LOGIN_BUTTON)).click()
        # ✅ no unconditional wait for shop – because wrong password won’t show shop button
