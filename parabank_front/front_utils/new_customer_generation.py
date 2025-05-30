from parabank_front.pages.register import ParabankRegister
from parabank_front.pages.overview import ParabankOverviewPage
import parabank_front.tests.ui_assertions.pb_ui_assertions as fa
import logging
logger = logging.getLogger(__name__)


def new_customer_generation(browser, random_user):
    register_page = ParabankRegister(browser)
    overview_page = ParabankOverviewPage(browser)

    register_page.load(register_page.URL)
    register_page.register_customer(random_user)
    logger.info(f'full welcome text: {overview_page.title}')
    fa.assert_title_page(overview_page, register_page.TITLE2)

    return random_user
