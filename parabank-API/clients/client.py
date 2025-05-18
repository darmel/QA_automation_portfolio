import json
from uuid import uuid4
from utils.request import APIRequest
from config import BASE_URL


class ParaBankClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.request = APIRequest()

    def login_testuser(self, username: str, password: str):
        username = "usertest"
        password = "password"
        url = f'{self.base_url}/{username}/{password}'
        return self.request.get(url)
