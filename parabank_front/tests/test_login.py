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
from parabank_front.pages.transfer import ParabankTransfer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
# fa for front assertions
import parabank_front.tests.ui_assertions.pb_ui_assertions as fa
from parabank_front.front_utils.open_new_account import open_new_account
from parabank_front.front_utils.fake_data_generator import generate_user

# from assertpy.assertpy import assert_that, soft_assertions

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
    fa.assert_title_page(register_page, register_page.TITLE)

    # WHEN, se registra un customer
    register_page.register_customer(random_user)
    # THEN, obtengo nuevo titulo de pagina, y welcome text
    fa.assert_title_page(register_page, register_page.TITLE_SUCCESS)
    full_text = overview_page.get_username()
    logger.info(f'full welcome text: {full_text}')
    fa.assert_welcome_text_with_name(
        register_page, random_user['first_name'], random_user['last_name'])


def test_register_customer_fail_due_used_username(browser):
    register_page = ParabankRegister(browser)
    john_user = generate_user('john')
    # Given, estoy en la pagiona de register
    register_page.load(register_page.URL)
    logger.info(f'titulo de la pagina: {register_page.title}')
    fa.assert_title_page(register_page, register_page.TITLE)
    # WHEN, registro un customer con username ya usado
    register_page.register_customer(john_user)
    # THEN: Obtengo error porque el username esta en uso
    error_message = register_page.has_error_message()
    logger.info(f'mensaje de error: {error_message}')
    fa.assert_text(error_message, register_page.USERNAME_ALREADY_EXIST_TEXT)


def test_open_account(browser, new_customer):
    register_page = ParabankRegister(browser)
    overview_page = ParabankOverviewPage(browser)
    openaccount_page = ParabankOpenaccountPage(browser)
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
    openaccount_page.click_open_account()
    # THEN
    fa.assert_text(openaccount_page.get_success_text(),
                   openaccount_page.SUCCESS_TEXT)
    new_account_id = openaccount_page.get_new_account_id()
    logger.info(f'Id de la cuenta nueva: {new_account_id}')


def test_transaction_betwen_customer_accounts(browser, new_customer, amount=50):
    overview_page = ParabankOverviewPage(browser)
    openaccount_page = ParabankOpenaccountPage(browser)
    transfer_page = ParabankTransfer(browser)

    # Given
    account_1, account_2 = open_new_account(browser, new_customer)
    logger.info(f'ID cuenta 1 {account_1}, ID cuenta 2 {account_2}')
    openaccount_page.go_to_transfer_funds()
    fa.assert_title_page(transfer_page, transfer_page.TITLE)
    # time.sleep(1)
    # WHEN
    transfer_page.set_amount(amount)
    # time.sleep(1)
    from_account = transfer_page.select_from_account()
    to_account = transfer_page.select_to_account()
    logger.info(f'from account: {from_account}, to account {to_account}')
    # time.sleep(1)
    transfer_page.click_transfer_account()
    # THEN
    result_title = transfer_page.get_result_title()
    logger.info(f'Result title: {result_title}')
    fa.assert_text(result_title, transfer_page.SUCCESS_TITLE)
    fa.assert_text_contain(transfer_page.get_amount_result_text(), str(amount))
    fa.assert_text(transfer_page.get_from_account_id(), from_account)
    fa.assert_text(transfer_page.get_to_account_id(), to_account)
    logger.info(
        f'Result: from account: {transfer_page.get_from_account_id()} to account: {transfer_page.get_to_account_id()}')
    time.sleep(0)


@pytest.mark.parametrize(
    ['username', 'password', 'name', 'last_name'],
    [('john', 'demo', 'John', 'Smith'),]
)
def test_logout(browser, username, password, name, last_name):

    home_page = ParabankHomePage(browser)
    overview_page = ParabankOverviewPage(browser)

    # Given la pagina de parabank esta activa
    home_page.load(home_page.URL)
    logger.info(f'titulo de pagina HOME: {home_page.title}')
    home_page.login(username, password)
    logger.info(f'titulo de pagina OVERVIEW: {overview_page.title}')
    # WHEN presiono boton para desloguear
    overview_page.log_out()
    logger.info(f'Deslogueado. titulo de pagina HOME: {home_page.title}')
    # THEN buscar algo apra hacer el assert"
    # valido el titulo de la pagina
    fa.assert_title_page(home_page, home_page.TITLE)
