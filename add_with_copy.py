import time

import requests
import json


def test_upload():
    test_client_id = '667260'
    test_api_key = 'fd6087c6-de11-43ee-a233-4540cb92998a'
    headers = {
        'Client-Id': test_client_id,
        'Api-Key': test_api_key
    }
    url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    data = {
        "items": [
            {
                "sku": '483800834',
                "name": "Тест от олега от 12 мая",
                "offer_id": "Oleg-5",
                "currency_code": "RUB",
                "old_price": "10000",
                "price": "10000",
                "premium_price": "10000",
                "vat": "0"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()

    url = 'https://api-seller.ozon.ru/v1/product/import/info'
    data = {'task_id': response['result']['task_id']}
    time.sleep(20)
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    print(response)
    if len(response['result']['items'][0]['errors']) > 0:
        print('Есть ошибки')
    else:
        print('Нет ошибок')


def load_ozon(item):
    client_id = '667260'
    api_key = 'fd6087c6-de11-43ee-a233-4540cb92998a'
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key
    }
    url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    data = {
        "items": [
            {
                "sku": str(item.id),
                "name": item.name,
                "offer_id": "РСВ-" + str(item.source_item.id) + "РСВ-" + str(item.source_item.id),
                "currency_code": "RUB",
                "old_price": "10000",
                "price": "10000",
                "premium_price": "10000",
                "vat": "0"
            }
        ]
    }
    requests.post(url, headers=headers, data=json.dumps(data))
