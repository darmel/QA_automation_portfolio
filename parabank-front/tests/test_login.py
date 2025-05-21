"""
esto es el test del login de parabank
"""

# importo las page object de las paginas que voy a usar
from pages.home import ParabankHomePage
from pages.overview import ParabankOverviewPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
import logging
logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ['username', 'password'],
    [('testuser', 'password')]
)
# el test usa como argumento a la funcion que maneja la instancia del webdriver
# pytest maneja que si hay argumentos, va a fijarse en los fixtures
def test_login_parabank(browser, username, password):

    # creo los dos objetos de las paginas que voy a usar
    home_page = ParabankHomePage(browser)
    overview_page = ParabankOverviewPage(browser)
    # result_page = DuckDuckGoResultPage(browser)

    # Given la pagina de parabank esta activa
    home_page.load()
    logger.info(f'pagina cargada')

    # WHEN el user ingresa credenciales
    home_page.login(username, password)
    WebDriverWait(browser, 10).until(
        ec.title_is('ParaBank | Accounts Overview'))

    # THEN buscar algo apra hacer el assert"
    title = overview_page.title()
    logger.info(f'titulo de la pagina: {title}')
    assert 'ParaBank | Accounts Overview' == overview_page.title()
    assert True
