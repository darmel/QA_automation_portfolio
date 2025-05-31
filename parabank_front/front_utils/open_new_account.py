from parabank_front.pages.register import ParabankRegister
from parabank_front.pages.overview import ParabankOverviewPage
from parabank_front.pages.openaccount import ParabankOpenaccountPage
import parabank_front.tests.ui_assertions.pb_ui_assertions as fa
import logging
logger = logging.getLogger(__name__)


def open_new_account(browser, customer):
    overview_page = ParabankOverviewPage(browser)
    openaccount_page = ParabankOpenaccountPage(browser)

    overview_page.go_to_open_new_account()
    fa.assert_title_page(openaccount_page, openaccount_page.TITLE)
    account_id = openaccount_page.get_first_account_id()
    openaccount_page.click_open_account()
    fa.assert_text(openaccount_page.get_success_text(),
                   openaccount_page.SUCCESS_TEXT)
    new_account_id = openaccount_page.get_new_account_id()

    return account_id, new_account_id
