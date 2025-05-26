from selenium.webdriver.common.by import By
import logging
logger = logging.getLogger(__name__)


class ParabankOverviewPage:
    # locators:
    OVERVIEW_HEADER = (
        By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div[1]/h1')

    USER_WELCOME_TEXT = (By.CSS_SELECTOR, '#leftPanel p.smallText')

    # initializer

    def __init__(self, browser):
        self.browser = browser

    def header_text(self):
        element = self.browser.find_element(*self.OVERVIEW_HEADER)
        return element.text

    def title(self):
        return self.browser.title

    def get_username(self):
        welcome_text = self.browser.find_element(*self.USER_WELCOME_TEXT)
        return welcome_text.text
