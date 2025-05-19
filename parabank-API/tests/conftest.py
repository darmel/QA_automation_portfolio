import pytest
from clients.client import ParaBankClient
# from utils.helpers import db_cleaner
# from utils.helpers import read_file
import random
from utils.helpers import pretty_print

from utils import response


@pytest.fixture
def client():
    return ParaBankClient()


@pytest.fixture
def get_customerId(client):
    response = client.login_testuser('testuser', 'password')
    customerId = response.as_dict.get("id")
    print('\nCustomer Id obtenida: ', customerId)
    return customerId


@pytest.fixture
def get_first_accountId(client, get_customerId):
    response = client.get_customer_accounts(get_customerId)
    # pretty_print(response.as_dict)
    first_account = response.as_dict[0]
    account_id = first_account["id"]
    print('Id de la primera cuenta: ', account_id)
    return account_id
