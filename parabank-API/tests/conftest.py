import pytest
from clients.client import ParaBankClient
import random
from utils.helpers import pretty_print, accountId_helper, count_accounts

from utils import response
import logging
logger = logging.getLogger(__name__)


def pytest_configure():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")


@pytest.fixture
def client():
    return ParaBankClient()


@pytest.fixture
def get_customerId(client):
    response = client.login_testuser('testuser', 'password')
    customerId = response.as_dict.get("id")
    logger.info(f'customer Id obtenida {customerId}')
    return customerId


@pytest.fixture
def get_first_accountId(client, get_customerId):
    response = client.get_customer_accounts(get_customerId)
    account_id = accountId_helper(response, 0)
    return account_id


@pytest.fixture
def ensure_two_accounts(client, get_customerId, get_first_accountId):
    accounts = client.get_customer_accounts(get_customerId)
    account_amount = count_accounts(accounts)
    # account_amount = 1
    logger.info(f'cantidad de cuentas para transfer: {account_amount}')

    if account_amount >= 2:
        logger.info(f'Tengo cuentas suficientes para transfer')
        id1 = accounts.as_dict[0]['id']
        id2 = accounts.as_dict[1]['id']
        logger.info(f'id1 {id1} y id2 {id2}')

        return id1, id2
    else:
        logger.info(f'hay que crear cuenta')
        response_creation = client.create_new_account_for_customer(
            get_customerId, accounts.as_dict[0]['id'])
        if response_creation.status_code == 200:
            accounts = client.get_customer_accounts(get_customerId)
            id1 = accounts.as_dict[0]['id']
            id2 = accounts.as_dict[1]['id']
            logger.info(f'id1 {id1} y id2 {id2}')
            return id1, id2
        else:
            pytest.fail("No se puede crear cuentas para el test")
