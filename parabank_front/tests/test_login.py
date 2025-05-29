"""
esto es el test del login de parabank
"""
import time  # solo para debug

# importo las page object de las paginas que voy a usar
import logging
from pages.home import ParabankHomePage
from parabank_front.pages.overview import ParabankOverviewPage
from parabank_front.pages.register import ParabankRegister
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
# fa for front assertions
import parabank_front.tests.ui_assertions.pb_ui_assertions as fa


from assertpy.assertpy import assert_that, soft_assertions

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ['username', 'password', 'name', 'last_name'],
    [('testuser', 'password', 'juan', 'lopez'),]
)
# el test usa como argumento a la funcion que maneja la instancia del webdriver
# pytest maneja que si hay argumentos, va a fijarse en los fixtures
def test_login_parabank(browser, username, password, name, last_name):

    # creo los dos objetos de las paginas que voy a usar
    home_page = ParabankHomePage(browser)
    overview_page = ParabankOverviewPage(browser)

    # Given la pagina de parabank esta activa
    home_page.load()
    logger.info(f'pagina cargada')

    # WHEN el user ingresa credenciales
    home_page.login(username, password)
    WebDriverWait(browser, 10).until(
        ec.title_is('ParaBank | Accounts Overview'))

    # THEN buscar algo apra hacer el assert"
    # valido el titulo de la pagina
    title = overview_page.title
    logger.info(f'titulo de la pagina: {title}')
    fa.assert_title_page(overview_page, overview_page.TITLE)

    # valido el nombre de usuario
    full_text = overview_page.get_username()
    logger.info(f'full welcome text: {full_text}')
    full_name = f'{name} {last_name}'
    assert_that(full_text).contains(full_name)


def test_login_fail(browser):
    username = "fakeuser"
    password = "fakepass"
    # creo los dos objetos de las paginas que voy a usar
    home_page = ParabankHomePage(browser)

    # Given la pagina de parabank esta activa
    home_page.load()
    logger.info(f'pagina cargada')

    # WHEN el user ingresa credenciales
    home_page.login(username, password)
    WebDriverWait(browser, 10).until(
        ec.title_is('ParaBank | Error'))

    # THEN buscar algo apra hacer el assert"
    # valido el titulo de la pagina
    title = home_page.title
    logger.info(f'titulo de la pagina: {title}')
    fa.assert_title_page(home_page, 'ParaBank | Error')
    # assert 'ParaBank | Error' == home_page.title()
    # valido el nombre de usuario


def test_register_new_customer(browser, random_user):
    # creo los objetos de pagina que voy a usar
    register_page = ParabankRegister(browser)
    overview_page = ParabankOverviewPage(browser)

    # Given, estoy en lapagina register
    register_page.load()
    logger.info(f'titulo de la pagina: {register_page.title}')
    fa.assert_title_page(register_page, register_page.TITLE)

    # WHEN, se registra un customer
    register_page.register_customer(random_user)
    # time.sleep(3)
    WebDriverWait(browser, 10).until(
        ec.title_is('ParaBank | Customer Created'))
    fa.assert_title_page(register_page, 'ParaBank | Customer Created')
    # valido el nombre de usuario
    full_text = overview_page.get_username()
    logger.info(f'full welcome text: {full_text}')
    full_name = f'{random_user["first_name"]} {random_user["last_name"]}'
    assert_that(full_text).contains(full_name)
