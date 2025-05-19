import requests
from urllib.parse import urlencode

from utils.response import Response


class APIRequest:
    def get(self, url):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'  # sin esto me devulvelve en xml
        }
        response = requests.get(url, headers=headers)
        return self.__get_responses(response)

    def post(self, url, payload, params):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if payload is not None:
            # print('con payload')
            response = requests.post(url, data=payload, headers=headers)
        else:
            # print('sin payload')
            response = requests.post(url, headers=headers, params=params)

        return self.__get_responses(response)

    def __get_responses(self, response):
        try:
            as_dict = response.json()
        except ValueError:
            as_dict = {}
        return Response(
            status_code=response.status_code,
            text=response.text,
            as_dict=as_dict,
            headers=response.headers
        )
