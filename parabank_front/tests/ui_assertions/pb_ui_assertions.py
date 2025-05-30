from assertpy.assertpy import assert_that, soft_assertions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
logger = logging.getLogger(__name__)


def assert_title_page(page, expected, wait=10):
    WebDriverWait(page.browser, wait).until(ec.title_is(expected))
    assert_that(page.title).is_equal_to(expected)


def assert_welcome_text_with_name(page, name, last_name):
    full_name = f'{name} {last_name}'
    full_text = page.get_username()
    assert_that(full_text).contains(full_name)


def assert_aaccount_oppend(page, text):
    assert_that(page.get_success_text()).is_equal_to(text)
