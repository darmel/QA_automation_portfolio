import json
from uuid import uuid4
from utils.request import APIRequest
from config import BASE_URL


class ParaBankClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.request = APIRequest()

    def login_testuser(self, username: str, password: str):
        username = username
        password = password
        url = f'{self.base_url}/login/{username}/{password}'
        # print(url)
        return self.request.get(url)

    def customer_by_Id(self, customerId):
        url = f'{self.base_url}/customers/{customerId}'
        return self.request.get(url)

    def get_customer_accounts(self, customerId):
        url = f'{self.base_url}/customers/{customerId}/accounts'
        return self.request.get(url)

    def create_new_account_for_customer(self, customerId, accountId):
        url = f'{self.base_url}/createAccount'
        params = {
            "customerId": customerId,
            "newAccountType": 1,
            "fromAccountId": accountId
        }
        response = self.request.post(url, payload=None, params=params)
        return response
