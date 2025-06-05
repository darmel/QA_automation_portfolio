from faker import Faker
import uuid
import unicodedata
import re
import logging
logger = logging.getLogger(__name__)

# faake = Faker("en_US")
fake = Faker("es_AR")


def generate_user():
    first = fake.first_name()
    first_cleaned = clean(first)
    last = fake.last_name()
    last_cleaned = clean(last)
    username = re.sub(r"\s+", ".", f"{first_cleaned}.{last_cleaned}")
    username = f"{username[:12]}{uuid.uuid4().hex[:6]}"
    username = re.sub(r"\s+", ".", username.lower())[:19]
    logger.info(f'customer generado: {first} {last}. Username: {username}')
    customer = {  # devuelve un diccionario
        "first_name": first_cleaned,
        "last_name": last_cleaned,
        "address": clean(fake.street_address()[:40]),
        "city": clean(fake.city()[:20]),  # para limintar  a 20 caracteres
        # "state": fake.state(),
        "state": clean(fake.province()[:20]),
        "zip_code": fake.postcode(),
        "phone": fake.phone_number(),
        "ssn": fake.ssn(),
        "username": username,
        "password": "password"
    }
    logger.info(f'complete customer generado: {customer}')
    return customer


def clean(text: str) -> str:
    # clean ñ and ´s
    text = unicodedata.normalize("NFKD", text).encode(
        "ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", " ", text).strip()  # delete multiple spaces
    return text
