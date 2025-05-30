from selenium.webdriver.common.by import By
from parabank_front.pages.base import BasePage

import logging
logger = logging.getLogger(__name__)


class ParabankOverviewPage(BasePage):
    TITLE = 'ParaBank | Accounts Overview'

    # locators:

    # initializer

    def __init__(self, browser):
        self.browser = browser
