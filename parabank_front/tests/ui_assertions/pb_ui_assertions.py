from assertpy.assertpy import assert_that, soft_assertions
import pytest
from cerberus import Validator
from parabank_API.schemas.schema_customerId import schema_customer
import logging
logger = logging.getLogger(__name__)


def assert_title_page(page, expected):
    assert_that(page.title).is_equal_to(expected)
