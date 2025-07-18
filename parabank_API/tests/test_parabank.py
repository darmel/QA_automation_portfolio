from assertpy.assertpy import assert_that, soft_assertions
import pytest
from pathlib import Path
from jsonpath_ng import parse
# from tests.schema_test import schema
import parabank_API.tests.assertions.parabank_assertions as pa
from parabank_API.utils.helpers import pretty_print, count_accounts, accountId_helper
from parabank_API.schemas.schema_customerId import schema_customer
from parabank_API.schemas.schema_accountId import schema_account
import logging
logger = logging.getLogger(__name__)

# Arrange
# Act
# Assert


@pytest.mark.api
def test_validate_login(client):
    response = client.login_testuser('john', 'demo')
    pa.assert_status_code(response, 200)
    pa.assert_firstName_is_present(response, 'John')
    pa.assert_customerId_is_valid(response)

    pretty_print(response.as_dict)


@pytest.mark.api
def test_login_invalid_credentials(client):
    response = client.login_testuser('fakeuser', 'fakepass')
    pa.assert_status_code(response, 400)
    pa.assert_text_response(response, 'Invalid username and/or password')
    pretty_print(response.text)


@pytest.mark.api
def test_customer_has_valid_schema(client, get_customerId):
    customerId = get_customerId
    response = client.customer_by_Id(customerId)
    pretty_print(response.as_dict)
    pa.assert_status_code(response, 200)
    pa.assert_customer_by_Id_has_expected_schema(schema_customer, response)


@pytest.mark.api
def test_customer_has_valid_number_of_accounts(client, get_first_accountId, get_customerId):
    # account_amount = 0
    customerId = get_customerId
    response = client.get_customer_accounts(customerId)
    pa.assert_status_code(response, 200)
    pa.assert_customer_has_valid_amount_of_accounts(response)
    pa.assert_value_is_present_in_array_of_elements(
        response, 'id', get_first_accountId)


@pytest.mark.api
def test_get_account_detail_schema(client, get_first_accountId):
    accountId = get_first_accountId
    response = client.get_account_info(accountId)
    pretty_print(response.as_dict)
    pa.assert_status_code(response, 200)
    account = response.as_dict
    pa.assert_account_by_Id_has_expected_schema(schema_account, response)


@pytest.mark.api
def test_can_create_new_account_for_customer(client, get_first_accountId, get_customerId):
    customerId = get_customerId
    response = client.get_customer_accounts(customerId)
    original_account_amount = count_accounts(response)
    response = client.create_new_account_for_customer(
        customerId, get_first_accountId)
    pa.assert_status_code(response, 200)
    pretty_print(response.as_dict)
    new_account_id = response.as_dict.get('id')
    # new_account_id = 12345
    logger.info(f'new account id: {new_account_id}')
    response = client.get_customer_accounts(customerId)
    new_account_amount = count_accounts(response)
    pa.assert_a_is_greter_than_b(new_account_amount, original_account_amount)
    pa.assert_value_is_present_in_array_of_elements(
        response, 'id', new_account_id)


@pytest.mark.api
def test_validate_transfer(client, get_customerId, ensure_two_accounts):
    # customerId = get_customerId
    amount = 50
    id1, id2 = ensure_two_accounts
    logger.info(f'de veulta en el test id1 {id1} y id2 {id2}')
    response = client.trasnfer(id2, id1, amount)
    pretty_print(response.text)
    pa.assert_status_code(response, 200)
    pa.assert_trasnfer_is_succesful(response, id1, id2, amount)
