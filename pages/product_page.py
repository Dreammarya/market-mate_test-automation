import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from utils.alert_handler import accept_alert


class ProductPage:
    """Page Object Model for the Product Page."""

    # Locators as class constants
    _INTERACTIVE_RATING = (By.CLASS_NAME, "interactive-rating")
    _REVIEW_TEXTAREA = (By.CLASS_NAME, "new-review-form-control")
    _STAR_LIST = (By.CSS_SELECTOR, ".interactive-rating .star")
    _SEND_BUTTON = (By.CLASS_NAME, "new-review-btn-send")
    _REVIEW_RESTRICTION = (By.XPATH, "//p[contains(text(), 'You have already reviewed this product')]")
    _MENU_ICON = (By.CLASS_NAME, "menu-icon")
    _DELETE_BUTTON = (By.XPATH, "//button[contains(text(),'Delete')]")
    _REVIEWS_TEXT = (By.CSS_SELECTOR, "p.reviews")
    _COMMENT_BLOCKS = (By.CSS_SELECTOR, ".comment")
    _REVIEW_CONTAINERS = (By.CSS_SELECTOR, ".review-container")
    _COMMENT_HEADER_STRONG = (By.CSS_SELECTOR, ".comment-header strong")
    _STARS = (By.CSS_SELECTOR, ".star")
    _REVIEW_BLOCKS = (By.CLASS_NAME, "review-block")
    _COMMENT_DIVS = (By.CSS_SELECTOR, "div.comment")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def load(self, product_id: str) -> None:
        self.driver.get(f"https://grocerymate.masterschool.com/product/{product_id}")

    def open_review_form(self) -> None:
        self.wait.until(EC.presence_of_element_located(self._INTERACTIVE_RATING))

    def enter_review_text(self, text: str) -> None:
        textarea = self.wait.until(EC.presence_of_element_located(self._REVIEW_TEXTAREA))
        textarea.clear()
        textarea.send_keys(text)

    def select_star_rating(self, stars: int = 5) -> None:
        try:
            self.wait.until(EC.presence_of_all_elements_located(self._STAR_LIST))
            stars_list = self.driver.find_elements(*self._STAR_LIST)
        except TimeoutException:
            raise Exception("Cannot rate: user has already reviewed or stars not rendered.")

        if stars < 1 or stars > len(stars_list):
            raise ValueError(f"Invalid star count: {stars}")

        self.driver.execute_script("arguments[0].scrollIntoView(true);", stars_list[stars - 1])
        stars_list[stars - 1].click()
        self.wait.until(EC.element_to_be_clickable(self._SEND_BUTTON))

    def submit_review(self) -> None:
        send_btn = self.wait.until(EC.element_to_be_clickable(self._SEND_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", send_btn)
        send_btn.click()

    def verify_review_present(self, text: str) -> None:
        locator = (By.XPATH, f"//div[contains(@class,'review-body') and contains(text(), '{text}')]")
        self.wait.until(EC.presence_of_element_located(locator))

    def remove_existing_review(self) -> None:
        try:
            self.wait.until(EC.presence_of_element_located(self._REVIEW_RESTRICTION))

            menu_icon = self.wait.until(EC.element_to_be_clickable(self._MENU_ICON))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", menu_icon)
            menu_icon.click()

            self.wait.until(EC.element_to_be_clickable(self._DELETE_BUTTON))
            delete_button = self.driver.find_element(*self._DELETE_BUTTON)
            delete_button.click()

            try:
                accept_alert(self.driver)
            except NoAlertPresentException:
                pass

            self.wait.until_not(EC.presence_of_element_located(self._REVIEW_RESTRICTION))

        except TimeoutException:
            pass

    def get_review_comments(self) -> list[tuple[str, str]]:
        self.wait.until(EC.presence_of_all_elements_located(self._COMMENT_BLOCKS))
        comment_blocks = self.driver.find_elements(*self._COMMENT_BLOCKS)

        result = []
        for block in comment_blocks:
            try:
                author = block.find_element(By.CSS_SELECTOR, ".author").text.strip()
                comment = block.find_element(By.CSS_SELECTOR, ".text").text.strip()
                if comment:
                    result.append((author, comment))
            except Exception:
                continue
        return result

    def _parse_average_rating_from_stars(self, stars) -> float:
        full_stars = 0
        partial_fraction = 0.0

        for star in stars:
            class_attr = star.get_attribute("class")

            if "full" in class_attr:
                full_stars += 1
            elif "partial" in class_attr:
                try:
                    filled_span = star.find_element(By.CSS_SELECTOR, ".filled")
                    style_attr = filled_span.get_attribute("style")
                    percent_str = style_attr.split("width:")[1].split("%")[0].strip()
                    percent = float(percent_str)
                    partial_fraction = percent / 100
                except Exception:
                    partial_fraction = 0.0
                break

        return round(full_stars + partial_fraction, 1)

    def get_average_rating(self) -> float:
        stars = self.wait.until(EC.presence_of_all_elements_located(self._STARS))
        return self._parse_average_rating_from_stars(stars)

    def get_review_count(self) -> int:
        elem = self.wait.until(EC.presence_of_element_located(self._REVIEWS_TEXT))
        raw = elem.text.strip()
        if raw.startswith("(") and raw.endswith(")"):
            return int(raw[1:-1])
        # fallback for e.g. "3 Reviews"
        digits = re.findall(r"\d+", raw)
        if digits:
            return int(digits[0])
        raise ValueError(f"Unexpected format for review count: {raw}")

    def get_user_comment_text(self) -> str:
        self.wait.until(EC.presence_of_all_elements_located(self._REVIEW_CONTAINERS))
        author_blocks = self.driver.find_elements(*self._REVIEW_CONTAINERS)

        for block in author_blocks:
            try:
                author = block.find_element(By.CSS_SELECTOR, ".review-username").text
                if "AutoTestG" in author:
                    comment = block.find_element(By.CSS_SELECTOR, ".review-comment").text.strip()
                    return comment
            except Exception:
                continue
        return ""

    def user_has_comment(self, username: str) -> bool:
        self.wait.until(EC.presence_of_all_elements_located(self._COMMENT_HEADER_STRONG))
        author_elements = self.driver.find_elements(*self._COMMENT_HEADER_STRONG)
        return any(el.text.strip() == username for el in author_elements)

    def get_visible_review_star_ratings(self) -> list[int]:
        review_blocks = self.driver.find_elements(*self._REVIEW_BLOCKS)
        ratings = []
        for block in review_blocks:
            filled_stars = block.find_elements(By.CSS_SELECTOR, ".custom-rating span.star-filled")
            ratings.append(len(filled_stars))
        return ratings

    def get_average_from_visible_reviews(self) -> float:
        self.wait.until(EC.presence_of_all_elements_located(self._COMMENT_DIVS))
        reviews = self.driver.find_elements(*self._COMMENT_DIVS)

        total = 0
        count = 0

        for review in reviews:
            try:
                rating_text = review.find_element(By.CSS_SELECTOR, "span.small").text.strip()
                if rating_text.startswith("(") and rating_text.endswith(")"):
                    value = int(rating_text[1:-1])
                    total += value
                    count += 1
            except Exception:
                continue

        if count == 0:
            raise ValueError("No valid review ratings found.")

        return round(total / count, 1)
