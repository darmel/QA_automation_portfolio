from assertpy.assertpy import assert_that, soft_assertions
import pytest
# from pathlib import Path
# from jsonpath_ng import parse
# from tests.schema_test import schema
from parabank_database.expected_schema import table_definitions as td
from parabank_front.front_utils.open_new_account import open_new_account

import logging
logger = logging.getLogger(__name__)

# Arrange
# Act
# Assert


@pytest.mark.parametrize(
    "table_name, expected_columns",
    [
        ("CUSTOMER", td.CUSTOMER_COLUMNS),
        ("ACCOUNT", td.ACCOUNT_COLUMNS),
        ("TRANSACTION", td.TRANSACTION_COLUMNS),
        ("STOCK", td.STOCK_COLUMNS),
        ("COMPANY", td.COMPANY_COLUMNS),
        ("POSITIONS", td.POSITIONS_COLUMNS)
    ]
)
def test_table_has_expected_columns(db_cursor, table_name, expected_columns):
    db_cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")
    actual_columns = {desc[0] for desc in db_cursor.description}
    logger.info(f"columnas: {actual_columns}")
    assert_that(actual_columns).contains(*expected_columns)


def test_customer_table_is_not_empty(db_cursor):
    db_cursor.execute("SELECT COUNT(*) FROM CUSTOMER")
    count = db_cursor.fetchone()[0]
    logger.info(f'el numero que obtengo de la query: {count}')
    assert_that(count).is_greater_than(0)


def test_ui_created_accounts_linked_to_same_customer_in_db(db_cursor, browser, new_customer):
    # ARRANGE
    account_1, account_2 = open_new_account(browser, new_customer)
    USERNAME = new_customer['username']
    logger.info(f'username: {USERNAME}')
    logger.info(f'ID cuenta 1 {account_1}, ID cuenta 2 {account_2}')
    db_cursor.execute(f"SELECT ID FROM CUSTOMER WHERE USERNAME = '{USERNAME}'")
    customer_id = db_cursor.fetchone()[0]
    logger.info(f'user id: {customer_id}')
    # ACT
    db_cursor.execute(
        f"SELECT ID FROM ACCOUNT WHERE CUSTOMER_ID = '{customer_id}'")
    db_accounts = db_cursor.fetchall()
    db_account_1 = str(db_accounts[0][0])
    db_account_2 = str(db_accounts[1][0])
    # ASSERT
    logger.info(f"cuenta 1: {db_account_1} y cuenta 2: {db_account_2} en db")
    assert_that(account_1).is_equal_to(db_account_1)
    assert_that(account_2).is_equal_to(db_account_2)
