import pytest
from clients.client import ParaBankClient
# from utils.helpers import db_cleaner
# from utils.helpers import read_file
import random


@pytest.fixture
def client():
    return ParaBankClient()
