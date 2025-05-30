from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parabank_front.config import FRONT_URL
from parabank_front.pages.base import BasePage
import logging
logger = logging.getLogger(__name__)


class ParabankHomePage(BasePage):
    # url contra el online de parasoft

    URL = f'{FRONT_URL}/index.htm'
    TITLE = 'ParaBank | Welcome | Online Banking'
    TITLE_ERROR = 'ParaBank | Error'

    # locators
    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'input.button')

    # interactions methods
    def login(self, usarname, password):
        username_input = self.browser.find_element(*self.USERNAME_INPUT)
        username_input.send_keys(usarname)
        password_input = self.browser.find_element(*self.PASSWORD_INPUT)
        password_input.send_keys(password + Keys.RETURN)
