from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parabank_front.config import FRONT_URL
import logging
logger = logging.getLogger(__name__)


class BasePage:
    DEFAULT_WAIT = 10

    def __init__(self, browser):
        self.browser = browser

    @property
    def title(self):
        return self.browser.title

    # helper común para localizar elementos con espera explícita

    def find(self, locator, wait=DEFAULT_WAIT):
        return WebDriverWait(self.browser, wait).until(
            EC.presence_of_element_located(locator)
        )
