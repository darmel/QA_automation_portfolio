from uuid import uuid4
# from ..utils.request import APIRequest
from ..utils.request import APIRequest
from ..config import BASE_URL
import logging
logger = logging.getLogger(__name__)


class ParaBankClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.request = APIRequest()

    def login_testuser(self, username: str, password: str):
        url = f'{self.base_url}/login/{username}/{password}'
        logger.info(f'url: {url}')
        return self.request.get(url)

    def customer_by_Id(self, customerId):
        url = f'{self.base_url}/customers/{customerId}'
        return self.request.get(url)

    def get_customer_accounts(self, customerId):
        url = f'{self.base_url}/customers/{customerId}/accounts'
        return self.request.get(url)

    def create_new_account_for_customer(self, customerId, accountId):
        url = f'{self.base_url}/createAccount'
        # accounts type
        saving = 0
        checking = 1
        loan = 2
        params = {
            "customerId": customerId,
            "newAccountType": checking,
            "fromAccountId": accountId
        }
        response = self.request.post(url, payload=None, params=params)
        return response

    def get_account_info(self, accountId):
        url = f'{self.base_url}/accounts/{accountId}'
        return self.request.get(url)

    def trasnfer(self, fromAccountId, toAccountId, ammount):
        url = f'{self.base_url}/transfer'
        params = {
            "fromAccountId": fromAccountId,
            "toAccountId": toAccountId,
            "amount": ammount
        }
        response = self.request.post(url, payload=None, params=params)
        return response
