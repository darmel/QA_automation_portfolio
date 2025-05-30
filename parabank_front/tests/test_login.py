"""
esto es el test del login de parabank
"""
import time  # solo para debug

# importo las page object de las paginas que voy a usar
import logging
from pages.home import ParabankHomePage
from parabank_front.pages.overview import ParabankOverviewPage
from parabank_front.pages.register import ParabankRegister
from parabank_front.pages.openaccount import ParabankOpenaccountPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
# fa for front assertions
import parabank_front.tests.ui_assertions.pb_ui_assertions as fa


from assertpy.assertpy import assert_that, soft_assertions

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ['username', 'password', 'name', 'last_name'],
    [('john', 'demo', 'John', 'Smith'),]
)
# el test usa como argumento a la funcion que maneja la instancia del webdriver
# pytest maneja que si hay argumentos, va a fijarse en los fixtures
def test_login_parabank(browser, username, password, name, last_name):

    # creo los dos objetos de las paginas que voy a usar
    home_page = ParabankHomePage(browser)
    overview_page = ParabankOverviewPage(browser)

    # Given la pagina de parabank esta activa
    home_page.load(home_page.URL)
    logger.info(f'pagina cargada')

    # WHEN el user ingresa credenciales
    home_page.login(username, password)
#    WebDriverWait(browser, 10).until(
 #       ec.title_is('ParaBank | Accounts Overview'))

    # THEN buscar algo apra hacer el assert"
    # valido el titulo de la pagina
    title = overview_page.title
    logger.info(f'titulo de la pagina: {title}')
    fa.assert_title_page(overview_page, overview_page.TITLE)

    # valido el nombre de usuario en el welcome text
    full_text = overview_page.get_username()
    logger.info(f'full welcome text: {full_text}')
    fa.assert_welcome_text_with_name(overview_page, name, last_name)


def test_login_fail(browser):
    username = "fakeuser"
    password = "fakepass"
    # creo los dos objetos de las paginas que voy a usar
    home_page = ParabankHomePage(browser)

    # Given la pagina de parabank esta activa
    home_page.load(home_page.URL)
    logger.info(f'pagina cargada')
    fa.assert_title_page(home_page, home_page.title)

    # WHEN el user ingresa credenciales falsas
    home_page.login(username, password)

    # THEN
    # valido el titulo de la pagina que cambia a error por credenciales falsas
    title = home_page.title
    logger.info(f'titulo de la pagina: {title}')
    fa.assert_title_page(home_page, home_page.TITLE_ERROR)


def test_register_new_customer(browser, random_user):
    # creo los objetos de pagina que voy a usar
    register_page = ParabankRegister(browser)
    overview_page = ParabankOverviewPage(browser)

    # Given, estoy en lapagina register
    register_page.load(register_page.URL)
    logger.info(f'titulo de la pagina: {register_page.title}')
    fa.assert_title_page(register_page, register_page.TITLE1)

    # WHEN, se registra un customer
    register_page.register_customer(random_user)
    fa.assert_title_page(register_page, register_page.TITLE2)
    full_text = overview_page.get_username()
    logger.info(f'full welcome text: {full_text}')
    fa.assert_welcome_text_with_name(
        register_page, random_user['first_name'], random_user['last_name'])


def test_transaction_betwen_same_customer_accounts(browser, new_customer):
    register_page = ParabankRegister(browser)
    overview_page = ParabankOverviewPage(browser)
    openaccount_page = ParabankOpenaccountPage(browser)
    time.sleep(2)
    # given
    # you are in registar page after a customer registration
    fa.assert_welcome_text_with_name(
        register_page, new_customer['first_name'], new_customer['last_name'])
    # When
    # go to open new account
    register_page.go_to_open_new_account()
    logger.info(f'titulo de la pagina: {register_page.title}')
    fa.assert_title_page(openaccount_page, openaccount_page.TITLE)
    account_id = openaccount_page.get_first_account_id()
    logger.info(f'Id de la 1era ceunta: {account_id}')
    time.sleep(1)
    openaccount_page.click_open_account()
    time.sleep(2)
    fa.assert_aaccount_oppend(openaccount_page, openaccount_page.SUCCESS_TEXT)
    new_account_id = openaccount_page.get_new_account_id()
    logger.info(f'Id de la cuenta nueva: {new_account_id}')
    time.sleep(2)

    assert_that(1).is_equal_to(1)

    # given
