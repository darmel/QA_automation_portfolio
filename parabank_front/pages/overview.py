from selenium.webdriver.common.by import By
from parabank_front.pages.base import BasePage

import logging
logger = logging.getLogger(__name__)


class ParabankOverviewPage(BasePage):
    TITLE = 'ParaBank | Accounts Overview'

    # locators:

    USER_WELCOME_TEXT = (By.CSS_SELECTOR, '#leftPanel p.smallText')

    # initializer

    def __init__(self, browser):
        self.browser = browser

# del BasePage
    # def title(self):
    #    return self.browser.title

    def get_username(self):
        welcome_text = self.browser.find_element(*self.USER_WELCOME_TEXT)
        return welcome_text.text
