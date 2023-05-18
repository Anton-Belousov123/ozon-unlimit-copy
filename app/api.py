import json
import time

import requests

from secrets import env_info


class Api:
    def __init__(self):
        headers = {
            'Client-Id': env_info.client_id,
            'Api-Key': env_info.api_key
        }

    def test_upload(self, article, name, sku):
        print(article, name, sku)
        headers = {
            'Client-Id': '855070',
            'Api-Key': '4afd7b0a-561f-4494-86b0-d83d56565b78'
        }
        url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
        data = {
            "items": [
                {
                    "sku": sku,
                    "name": name,
                    "offer_id": "РСВ-" + str(article) + "РСВ-" + str(article),
                    "currency_code": "RUB",
                    "old_price": "10000",
                    "price": "10000",
                    "premium_price": "10000",
                    "vat": "0"
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data)).json()
        time.sleep(60)
        status = self.get_upload_status(response['result']['task_id'])
        print(status)
        if 'errors' in status['result']['items'][0].keys():
            print(status['result']['items'][0]['errors'])
            return False, status['result']['items'][0]['product_id']
        return True, 0

    def upload_to_main(self, article, name, sku):
        headers = {
            'Client-Id': '667260',
            'Api-Key': '835f30d9-7159-4956-97f0-5f6353f93aab'
        }
        url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
        data = {
            "items": [
                {
                    "sku": sku,
                    "name": name,
                    "offer_id": "РСВ-" + str(article) + "РСВ-" + str(article),
                    "currency_code": "RUB",
                    "old_price": "10000",
                    "price": "10000",
                    "premium_price": "10000",
                    "vat": "0"
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data)).json()


    def scrape_product(self, product_id: int) -> dict:
        headers = {
            'Client-Id': '855070',
            'Api-Key': '4afd7b0a-561f-4494-86b0-d83d56565b78'
        }
        url = 'https://api-seller.ozon.ru/v2/product/info'
        data = {
            "offer_id": "",
            "product_id": product_id,
            "sku": 0
        }
        result = requests.post(url=url, headers=headers, data=json.dumps(data)).json()['result']
        return result

    def scrape_attribute_names(self, category_id: int):
        headers = {
            'Client-Id': '855070',
            'Api-Key': '4afd7b0a-561f-4494-86b0-d83d56565b78'
        }
        data = {
            "attribute_type": "ALL",
            "category_id": [category_id],
            "language": "RU"
        }
        url = 'https://api-seller.ozon.ru/v3/category/attribute'
        result = requests.post(url=url, headers=headers,
                               data=json.dumps(data)).json()['result'][0]['attributes']
        return result

    def scrape_attribute_values(self, attribute_id: int, category_id: int):
        headers = {
            'Client-Id': '855070',
            'Api-Key': '4afd7b0a-561f-4494-86b0-d83d56565b78'
        }
        url = 'https://api-seller.ozon.ru/v2/category/attribute/values'
        data = {
            "attribute_id": attribute_id,
            "category_id": category_id,
            "language": "DEFAULT",
            "last_value_id": 0,
            "limit": 5000
        }
        result = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
        return result['result']

    def upload_item(self, data: dict):
        headers = {
            'Client-Id': '667260',
            'Api-Key': '835f30d9-7159-4956-97f0-5f6353f93aab'
        }
        response = requests.post(url='https://api-seller.ozon.ru/v2/product/import',
                                 headers=headers,
                                 data=json.dumps(data)).json()['result']
        return response

    def get_upload_status(self, task_id: int) -> dict:
        headers = {
            'Client-Id': '855070',
            'Api-Key': '4afd7b0a-561f-4494-86b0-d83d56565b78'
        }
        url = 'https://api-seller.ozon.ru/v1/product/import/info'
        data = {
            'task_id': task_id
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
        return response
