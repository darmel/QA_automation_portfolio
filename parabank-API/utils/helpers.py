import json
from pprint import pprint
import json
from pathlib import Path
import requests
import logging
logger = logging.getLogger(__name__)


def pretty_print(msg, indent=4):
    print()
    pprint(msg, indent=indent)


def count_accounts(response):
    pretty_print(response.as_dict)
    account_amount = 0
    account_amount = len(response.as_dict)
    logger.info(f'cantidad de cuentas: {account_amount}')
    return account_amount


def accountId_helper(response, position):
    account = response.as_dict[position]
    account_id = account["id"]
    return account_id
