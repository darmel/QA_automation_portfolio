from faker import Faker
import uuid
import logging
logger = logging.getLogger(__name__)

fake = Faker("en_US")
fake = Faker("es_AR")


def generate_user():
    first = fake.first_name()
    last = fake.last_name()
    username = f'{first.lower()}.{last.lower()}{uuid.uuid4().hex[:6]}'
    username = f'{first.lower()}.{uuid.uuid4().hex[:10]}'[:20]
    logger.info(f'customer generado: {first} {last}. Username: {username}')
    return {  # devuelve un diccionario
        "first_name": first,
        "last_name": last,
        "address": fake.street_address(),
        "city": fake.city(),
        # "state": fake.state(),
        "state": fake.province(),
        "zip_code": fake.postcode(),
        "phone": fake.phone_number(),
        "ssn": fake.ssn(),
        "username": username,
        "password": "password"

    }
