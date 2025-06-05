from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from parabank_front.pages.base import BasePage
from parabank_front.config import FRONT_URL


import logging
logger = logging.getLogger(__name__)


class ParabankTransfer(BasePage):

    URL = f'{FRONT_URL}/transfer.htm'
    TITLE = 'ParaBank | Transfer Funds'
    SUCCESS_TITLE = 'Transfer Complete!'

    # locators:

    USER_WELCOME_TEXT = (By.CSS_SELECTOR, '#leftPanel p.smallText')

    AMOUNT = (By.ID, "amount")
    FROM_ACCOUNT_SELECT = (By.ID, "fromAccountId")
    TO_ACCOUNT_SELECT = (By.ID, "toAccountId")

    TRRANSFER_BUTTON = (
        By.CSS_SELECTOR, 'input[type="submit"][value="Transfer"]')

    SHOW_RESULT_TITLE = (By.CSS_SELECTOR, "#showResult h1.title")

    AMOUNT_RESULT = (By.CSS_SELECTOR, "span#amountResult")
    FROM_ACCOUNT_ID_RESULT = (By.ID, "fromAccountIdResult")
    TO_ACCOUNT_ID_RESULT = (By.ID, "toAccountIdResult")

    # initializer

    def __init__(self, browser):
        self.browser = browser

    def set_amount(self, amount):
        amount_input = self.find(self.AMOUNT)
        amount_input.send_keys(amount)
        pass

    def select_from_account(self):
        select = Select(self.find(self.FROM_ACCOUNT_SELECT))
        first_option = select.options[0]
        select.select_by_index(0)
        return first_option.get_attribute("value")

    def select_to_account(self):
        select = Select(self.find(self.TO_ACCOUNT_SELECT))
        second_option = select.options[1]
        select.select_by_index(1)
        return second_option.get_attribute("value")

    def click_transfer_account(self):
        self.find(self.TRRANSFER_BUTTON).click()

#    def get_result_title(self):
#        result_title = self.find(self.SHOW_RESULT_TITLE)
#        return result_title.text.strip()cambio 31/mayo

    def get_result_title(self, wait=10):
        WebDriverWait(self.browser, wait).until(
            ec.text_to_be_present_in_element(self.SHOW_RESULT_TITLE, "Transfer Complete!"))
        return self.find(self.SHOW_RESULT_TITLE).text.strip()

    def get_amount_result_text(self):
        amount_result = self.find(self.AMOUNT_RESULT)
        return amount_result.text.strip()

    def get_from_account_id(self):
        from_account_result = self.find(self.FROM_ACCOUNT_ID_RESULT)
        from_account_result.text.strip()
        return from_account_result.text.strip()

    def get_to_account_id(self):
        to_account_result = self.find(self.TO_ACCOUNT_ID_RESULT)
        return to_account_result.text.strip()
