from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parabank_front.config import FRONT_URL
from parabank_front.pages.base import BasePage
import logging
logger = logging.getLogger(__name__)


class ParabankRegister(BasePage):

    URL = f'{FRONT_URL}/register.htm'
    TITLE1 = 'ParaBank | Register for Free Online Account Access'
    TITLE2 = 'ParaBank | Customer Created'  # after register title change

    # locators
    FIRST_NAME_INPUT = (By.ID, 'customer.firstName')
    LAST_NAME_INPUT = (By.ID, 'customer.lastName')
    ADDRESS_INPUT = (By.ID, 'customer.address.street')
    CITY_INPUT = (By.ID, 'customer.address.city')
    STATE_INPUT = (By.ID, 'customer.address.state')
    ZIP_CODE_INPUT = (By.ID, 'customer.address.zipCode')
    SSN_INPUT = (By.ID, 'customer.ssn')

    USERNAME_INPUT = (By.ID, 'customer.username')
    PASSWORD_INPUT = (By.ID, 'customer.password')
    PASSWORD_CONFIRM_INPUT = (By.ID, 'repeatedPassword')
    REGISTER_BUTTON = (
        By.CSS_SELECTOR, 'input[type="submit"][value="Register"]')

    # interactions methods

    def register_customer(self, customer):
        firstaname_input = self.find(self.FIRST_NAME_INPUT)
        firstaname_input.send_keys(customer["first_name"])
        lastname_input = self.find(self.LAST_NAME_INPUT)
        lastname_input.send_keys(customer["last_name"])
        address_input = self.find(self.ADDRESS_INPUT)
        address_input.send_keys(customer["address"])
        city_input = self.find(self.CITY_INPUT)
        city_input.send_keys(customer["city"])
        state_input = self.find(self.STATE_INPUT)
        state_input.send_keys(customer["state"])
        zipcode_input = self.find(self.ZIP_CODE_INPUT)
        zipcode_input.send_keys(customer["zip_code"])
        ssn_input = self.find(self.SSN_INPUT)
        ssn_input.send_keys(customer["ssn"])
        username_input = self.find(self.USERNAME_INPUT)
        username_input.send_keys(customer["username"])

        password_input = self.find(self.PASSWORD_INPUT)
        password_input.send_keys(customer["password"])
        password_confirm_input = self.find(self.PASSWORD_CONFIRM_INPUT)
        password_confirm_input.send_keys(customer["password"] + Keys.RETURN)
