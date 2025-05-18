import requests
from utils.response import Response


class APIRequest:
    def get(self, url):
        response = requests.get(url)
        return self.__get_responses(response)

    def post(self, url, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(url, data=payload, headers=headers)

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
