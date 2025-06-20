"""
Este modulo contiene los fixtures para inciar y cerrar el driver
es necesario que este en el directorio tests
es necesario que se llame conftest

"""

import webdriver_manager.chrome  # para leer el archivo de config.json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from parabank_front.front_utils.fake_data_generator import generate_user
from parabank_front.front_utils.new_customer_generation import new_customer_generation
from common.fixtures.common_fixtures import browser, random_user, new_customer, config


import os
import json

import logging
logger = logging.getLogger(__name__)


def pytest_configure():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")


# ALL FIXTURES MOVED TO common/fixtures/common_fixtures.py pecause they are used for database tests too
# imported using: from common.fixtures.common_fixtures import browser, random_user, new_customer, config

#
# @pytest.fixture
# def config(scope='sesion'):

# @pytest.fixture
# def browser(config):

# @pytest.fixture
# def random_user():

# @pytest.fixture
# def new_customer(browser, random_user):
