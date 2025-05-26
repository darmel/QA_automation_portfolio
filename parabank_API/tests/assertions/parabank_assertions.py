from assertpy.assertpy import assert_that, soft_assertions
import pytest
from cerberus import Validator
from parabank_API.schemas.schema_customerId import schema_customer
from parabank_API.utils.helpers import count_accounts
import logging
logger = logging.getLogger(__name__)


def assert_status_code(response, expected_code):
    assert_that(response.status_code).is_equal_to(expected_code)


def assert_firstName_is_present(response, firstName):
    first_name = response.as_dict.get("firstName")
    assert_that(first_name).is_equal_to(firstName)


def assert_customerId_is_valid(response):
    customerId = response.as_dict.get('id')
    # customerId = -1
    assert_that(customerId).is_positive()


def assert_text_response(response, expected_test):
    text = response.text
    assert_that(text).contains(expected_test)


def assert_customer_by_Id_has_expected_schema(schema, response):
    validator = Validator(schema, require_all=True)  # type: ignore
    is_valid = validator.validate(response.as_dict)  # type: ignore
    assert_that(is_valid, description=validator.errors).is_true()


def assert_customer_has_valid_amount_of_accounts(response):
    account_amount = count_accounts(response)
    # account_amount = -1
    assert_that(account_amount).is_greater_than_or_equal_to(1)


def assert_a_is_greter_than_b(a, b):
    assert_that(a).is_greater_than(b)


def assert_value_is_present_in_array_of_elements(response, key, value):
    ids = [account['id'] for account in response.as_dict]
    logger.info(f'ids: {ids}')
    assert_that(ids).contains(value)


def assert_account_by_Id_has_expected_schema(schema, response):
    validator = Validator(schema, require_all=True)  # type: ignore
    is_valid = validator.validate(response.as_dict)  # type: ignore
    assert_that(is_valid, description=validator.errors).is_true()


def assert_trasnfer_is_succesful(response, id1, id2, amount):
    text = response.text
    assert_that(text).contains(str(id1), str(id2), str(amount))
