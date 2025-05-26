from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parabank_front.config import FRONT_URL
import logging
logger = logging.getLogger(__name__)


class ParabankHomePage:
    # url contra el online de parasoft
    # URL = 'https://parabank.parasoft.com/parabank/index.htm'

    URL = FRONT_URL

    # locators
    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'input.button')

    # initializer
    def __init__(self, browser):
        self.browser = browser

    def load(self):
        self.browser.get(self.URL)

    # interactions methods
    def login(self, usarname, password):
        username_input = self.browser.find_element(*self.USERNAME_INPUT)
        username_input.send_keys(usarname)
        password_input = self.browser.find_element(*self.PASSWORD_INPUT)
        password_input.send_keys(password + Keys.RETURN)

    def title(self):
        return self.browser.title
