import pytest
from parabank_database.db_clients.parabank_db_client import open_parabank_conn
from common.fixtures.common_fixtures import browser, new_customer_generation, random_user, new_customer, config
import logging
logger = logging.getLogger(__name__)


def pytest_configure():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")


@pytest.fixture(scope="session")
def db_conn():
    conn = open_parabank_conn()
    logger.info(f'nueva conexion con base de datos')
    yield conn
    conn.close()


@pytest.fixture  # uno por tests
def db_cursor(db_conn):
    cur = db_conn.cursor()
    logger.info(f'Nuevo cursor')
    yield cur
    cur.close()
