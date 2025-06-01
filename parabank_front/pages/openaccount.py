from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from parabank_front.pages.base import BasePage
from parabank_front.config import FRONT_URL


import logging
logger = logging.getLogger(__name__)


class ParabankOpenaccountPage(BasePage):

    URL = f'{FRONT_URL}/openaccount.htm'
    TITLE = 'ParaBank | Open Account'
    SUCCESS_TEXT = "Your new account number:"

    # locators:

    USER_WELCOME_TEXT = (By.CSS_SELECTOR, '#leftPanel p.smallText')
    FROM_ACCOUNT_SELECT = (By.ID, "fromAccountId")
    OPEN_ACCOUNT_BUTTON = (
        By.CSS_SELECTOR, '#openAccountForm form div input[type="button"]')

#    OPEN_ACCOUNT_RESULT = (By.ID, "openAccountResult")
    SUCCESS_TITLE = (By.CSS_SELECTOR, "#openAccountResult h1")
    # SUCCESS_TEXT_RESULT = (By.CSS_SELECTOR, "#openAccountResult p")
    SUCCESS_TEXT_RESULT = (By.CSS_SELECTOR, "#openAccountResult p b")
    NEW_ACCOUNT_ID = (By.ID, "newAccountId")

    # initializer

    def __init__(self, browser):
        self.browser = browser

    def get_username(self):
        welcome_text = self.browser.find_element(*self.USER_WELCOME_TEXT)
        return welcome_text.text

    def get_first_account_id(self):
        select = Select(self.find(self.FROM_ACCOUNT_SELECT))
        first_option = select.options[0]
        return first_option.get_attribute("value")

    def click_open_account(self):
        self.find(self.OPEN_ACCOUNT_BUTTON).click()

#    def get_success_text(self):
#        return self.find(self.SUCCESS_TEXT_RESULT).text.strip()

    def get_success_text(self, wait=10):
        WebDriverWait(self.browser, wait).until(ec.text_to_be_present_in_element(
            self.SUCCESS_TEXT_RESULT, "Your new account number:"))
        return self.find(self.SUCCESS_TEXT_RESULT).text.strip()

    def get_new_account_id(self):
        return self.find(self.NEW_ACCOUNT_ID).text.strip()
