from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from parabank_front.config import FRONT_URL
import logging
logger = logging.getLogger(__name__)


class BasePage:
    DEFAULT_WAIT = 10
    USER_WELCOME_TEXT = (By.CSS_SELECTOR, '#leftPanel p.smallText')

    # left panel locators
    LINK_OPEN_NEW_ACCOUNT = (By.LINK_TEXT, "Open New Account")
    LINK_ACCOUNTS_OVERVIEW = (By.LINK_TEXT, "Accounts Overview")
    LINK_TRANSFER_FUNDS = (By.LINK_TEXT, "Transfer Funds")
    LINK_BILL_PAY = (By.LINK_TEXT, "Bill Pay")
    LINK_FIND_TRANSACTIONS = (By.LINK_TEXT, "Find Transactions")
    LINK_UPDATE_CONTACT_INFO = (By.LINK_TEXT, "Update Contact Info")
    LINK_REQUEST_LOAN = (By.LINK_TEXT, "Request Loan")
    LINK_LOG_OUT = (By.LINK_TEXT, "Log Out")

    def __init__(self, browser):
        self.browser = browser

    def load(self, URL):
        self.browser.get(URL)

    @property
    def title(self):
        return self.browser.title

    def get_username(self):
        welcome_text = self.browser.find_element(*self.USER_WELCOME_TEXT)
        return welcome_text.text

    # helper común para localizar elementos con espera explícita

    def find(self, locator, wait=DEFAULT_WAIT):
        return WebDriverWait(self.browser, wait).until(
            ec.presence_of_element_located(locator)
        )

    # Left Panel Actions
    def go_to_open_new_account(self):
        self.find(self.LINK_OPEN_NEW_ACCOUNT).click()

    def go_to_accounts_overview(self):
        self.find(self.LINK_ACCOUNTS_OVERVIEW).click()

    def go_to_transfer_funds(self):
        self.find(self.LINK_TRANSFER_FUNDS).click()

    def go_to_bill_pay(self):
        self.find(self.LINK_BILL_PAY).click()

    def go_to_find_transactions(self):
        self.find(self.LINK_FIND_TRANSACTIONS).click()

    def go_to_update_contact_info(self):
        self.find(self.LINK_UPDATE_CONTACT_INFO).click()

    def go_to_request_loan(self):
        self.find(self.LINK_REQUEST_LOAN).click()

    def log_out(self):
        self.find(self.LINK_LOG_OUT).click()
