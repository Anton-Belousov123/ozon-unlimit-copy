import json

import requests

from secrets import env_info


class Api:
    def __init__(self):
        self.headers = {
            'Client-Id': env_info.client_id,
            'Api-Key': env_info.api_key
        }

    def scrape_product(self, product_id: int) -> dict:
        url = 'https://api-seller.ozon.ru/v2/product/info'
        data = {
            "offer_id": "",
            "product_id": product_id,
            "sku": 0
        }
        result = requests.post(url=url, headers=self.headers, data=json.dumps(data)).json()['result']
        return result

    def scrape_attribute_names(self, category_id: int):
        data = {
            "attribute_type": "ALL",
            "category_id": [category_id],
            "language": "RU"
        }
        url = 'https://api-seller.ozon.ru/v3/category/attribute'
        result = requests.post(url=url, headers=self.headers,
                               data=json.dumps(data)).json()['result'][0]['attributes']
        return result

    def scrape_attribute_values(self, attribute_id: int, category_id: int):
        url = 'https://api-seller.ozon.ru/v2/category/attribute/values'
        data = {
            "attribute_id": attribute_id,
            "category_id": category_id,
            "language": "DEFAULT",
            "last_value_id": 0,
            "limit": 5000
        }
        result = requests.post(url=url, headers=self.headers, data=json.dumps(data)).json()
        return result['result']


    def upload_item(self, data: dict):
        response = requests.post(url='https://api-seller.ozon.ru/v2/product/import',
                                 headers=self.headers,
                                 data=json.dumps(data)).json()['result']
        return response


    def get_upload_status(self, task_id: int) -> dict:
        url = 'https://api-seller.ozon.ru/v1/product/import/info'
        data = {
            'task_id': task_id
        }
        response = requests.post(url=url, headers=self.headers, data=json.dumps(data)).json()
        return response
