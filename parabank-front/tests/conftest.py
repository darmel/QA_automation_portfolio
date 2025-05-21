"""
Este modulo contiene los fixtures para inciar y cerrar el driver
es necesario que este en el directorio tests
es necesario que se llame conftest

"""

import webdriver_manager.chrome  # para leer el archivo de config.json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeServide
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
import json

import logging
logger = logging.getLogger(__name__)


def pytest_configure():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")


@pytest.fixture
def config(scope='sesion'):  # scope= sesion, es para que lo  lea una vez y no en cada test
    # lee el json
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    # with open('config.json') as config_file:
    with open(os.path.abspath(config_path)) as config_file:
        config = json.load(config_file)

    # checkeamos los valores de la config
    assert config['browser'] in ['Firefox', 'Chrome', 'Headless Chrome']
    assert isinstance(config['implicit_wait'], int)
    assert config['implicit_wait'] > 0

    # si todo es valido, devolvemos la config
    return config


@pytest.fixture
def browser(config):  # ahora el browser recibe la config que ya fue checkeada
    # incializa una instancia del webdriver segun venga desde el config
    if config['browser'] == 'Firefox':
        # b = selenium.webdriver.Firefox()
        b = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()))
    elif config['browser'] == 'Chrome':
        # b = selenium.webdriver.Chrome()
        b = webdriver.Chrome(service=ChromeServide(
            ChromeDriverManager().install()))
    # elif config['browser'] == 'Headless Chrome':
        # opts = selenium.webdriver.ChromeOptions()
        # opts.add_argument('headless')
        # b = selenium.webdriver.Chrome(options=opts)
    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    # define el tiempo de espera para que aparezcan los eleementos segun la config
    b.implicitly_wait(config['implicit_wait'])

    # devuvle la instancia de webdriver
    yield b

    # cuando regresa, cierra la instancia
    b.quit()
