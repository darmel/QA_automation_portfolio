import json
from pprint import pprint
import json
from pathlib import Path
import requests


def pretty_print(msg, indent=4):
    print()
    pprint(msg, indent=indent)


def count_accounts(response):
    pretty_print(response.as_dict)
    account_amount = 0
    for item in response.as_dict:
        account_amount = account_amount + 1
    print('cantidad de cuentas: ', account_amount)
    return account_amount
