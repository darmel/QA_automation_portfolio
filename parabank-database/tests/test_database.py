from assertpy.assertpy import assert_that, soft_assertions
import pytest
from pathlib import Path
from jsonpath_ng import parse
# from tests.schema_test import schema
import logging
logger = logging.getLogger(__name__)

# Arrange
# Act
# Assert


def test_customer_table_is_not_empty(db_cursor):
    db_cursor.execute("SELECT COUNT(*) FROM CUSTOMER")
    count = db_cursor.fetchone()[0]
    logger.info(f'el numero que obtengo de la query: {count}')
    assert_that(count).is_greater_than(0)
