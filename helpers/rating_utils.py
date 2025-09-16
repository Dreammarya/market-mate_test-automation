from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def delete_existing_review(driver):
    """
    Deletes an existing user review if present.
    Handles:
      - Opening the review menu
      - Clicking the delete option
      - Confirming the deletion via alert
    If no review is found, it simply logs the information.
    """
    try:
        # Step 1: Open the options menu for the review (⋮ / menu icon)
        WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='menu-icon']"))
        ).click()
        time.sleep(1)  # small pause to ensure menu is fully visible

        # Step 2: Click on the "Delete" option in the dropdown
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-menu']/button[text()='Delete']"))
        ).click()

        # Step 3: Confirm deletion in the browser alert dialog
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        # Step 4: Log success and give the UI time to update
        print(" The review has been successfully removed.")
        time.sleep(2)

    except Exception as e:
        # If no review is found or already deleted, log the situation instead of failing the test
        print(f"ℹNo review was deleted (possibly none existed): {str(e)}")
