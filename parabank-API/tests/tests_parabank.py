from assertpy.assertpy import assert_that, soft_assertions
import pytest
from pathlib import Path
from jsonpath_ng import parse
# from tests.schema_test import schema

# import tests.assertions.people_assertions as pa
# from utils.helpers import obtain_person_by_lastname


def test_validate_login(client):
    response = client.login
