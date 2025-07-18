from assertpy.assertpy import assert_that, soft_assertions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
import logging
logger = logging.getLogger(__name__)


def assert_title_page(page, expected, wait=10):
    try:
        WebDriverWait(page.browser, wait).until(ec.title_is(expected))
    except TimeoutException:
        logger.info(
            f'[Debug] assert title page fail waiting for {expected}, actual title: {page.title}')
        raise
    assert_that(page.title).is_equal_to(expected)


def assert_welcome_text_with_name(page, name, last_name):
    full_name = f'{name} {last_name}'
    full_text = page.get_username()
    assert_that(full_text).contains(full_name)


# def assert_account_oppend(page, text):
#    assert_that(page.get_success_text()).is_equal_to(text)


def assert_text(text1, text2):
    assert_that(text1).is_equal_to(text2)


def assert_text_contain(text1, text2):
    assert_that(text1).contains(text2)


def assert_amount(amount1, amount2):
    pass
