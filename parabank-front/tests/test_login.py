"""
esto es el test del login de parabank
"""

# importo las page object de las paginas que voy a usar
import logging
from pages.home import ParabankHomePage
from pages.overview import ParabankOverviewPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
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
    title = overview_page.title()
    logger.info(f'titulo de la pagina: {title}')
    assert 'ParaBank | Accounts Overview' == overview_page.title()
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
    title = home_page.title()
    logger.info(f'titulo de la pagina: {title}')
    assert 'ParaBank | Error' == home_page.title()
    # valido el nombre de usuario
