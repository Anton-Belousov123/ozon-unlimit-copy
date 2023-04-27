import json
import time

from bs4 import BeautifulSoup
import requests

from app.api import Api
from app.web import Chrome


def prepare_data_to_upload(ch_w: dict, ch_a: dict, at: list[dict], index) -> dict:
    data = {
        'items': [
            {
                'attributes': at,
                'category_id': ch_a['category_id'],
                'depth': ch_w['depth'],  # TODO: Check it
                'dimension_unit': 'mm',  # TODO: Check it
                'height': ch_w['height'],
                'images': ['https://ir.ozone.ru/s3/multimedia-t/6382045493.jpg',
                           'https://ir.ozone.ru/s3/multimedia-l/6332904873.jpg',
                           'https://ir.ozone.ru/s3/multimedia-m/6332904874.jpg',
                           'https://ir.ozone.ru/s3/multimedia-k/6332904872.jpg',
                           'https://ir.ozone.ru/s3/multimedia-p/6332904877.jpg',
                           'https://ir.ozone.ru/s3/multimedia-j/6332904871.jpg'],
                'name': f'Тест название {index}',#ch_w['Название'],
                'offer_id': f'kamrantest{index}',
                'price': "5000",
                'vat': '0',
                'weight': ch_w['weight'],
                'weight_unit': ch_w['weight_unit'],
                'width': ch_w['width']
            }
        ]
    }
    return data

def get_attributes(ch_a, web_data, api_data, api):
    atrs = []
    for i in ch_a:
        try:
            if i['name'] in web_data.keys():
                if i['name'] == 'Бренд':
                    continue
                attributes = api.scrape_attribute_values(i['id'], api_data['category_id'])
                values = []
                for j in attributes:
                    if j['value'] in web_data[i['name']].split(', '):
                        values.append({'dictionary_value_id': int(j['id'])})
                        break
                atrs.append(
                    {
                        "id": int(i['id']),
                        "values": values
                    },
                )
        except Exception as e:
            atrs.append(
                {
                    "complex_id": 0,
                    'id': int(i['id']),
                    "values": [
                        {
                            "dictionary_value_id": int(i['dictionary_id']),
                            "value": web_data[i['name']]
                        }
                    ]
                }
            )
    atrs.append(
        {
            'id': 85,
            "values": [
                {
                    "value": "Нет бренда"
                }
            ]
        }
    )
    return atrs

def start():
    product_id = 483801856  # TODO: Here connect to database
    chrome = Chrome()
    api = Api()

    product_ids = [483800582, 483800559, 483800501, 483800444, 483800397, 483800338, 483800311, 483800285, 483800253, 483800229, 483800226, 483800205, 483799722, 483799717, 483799710, 483799690, 483799672, 483799671, 483799669, 483799609, 483799609, 483799590, 483799566, 483799484, 483799477, 483799474, 483799459, 483799454, 483799441, 483799440, 483799083, 483799081, 483798999, 483798871, 483798829, 483798828, 483798826, 483798818, 483798802, 483798777, 483798750, 483798714, 483798631, 483798516, 483798496, 483798492, 483798426, 483798421, 483798371, 483798336]

    for index, product_id, in enumerate(product_ids):

        characteristics_from_web: dict = chrome.scrape_product(product_id)
        characteristics_from_api: dict = api.scrape_product(product_id)
        attribute_names_from_api: dict = api.scrape_attribute_names(category_id=characteristics_from_api['category_id'])
        attrubute_names = get_attributes(attribute_names_from_api, characteristics_from_web, characteristics_from_api, api)

        prepared_data: dict = prepare_data_to_upload(
            ch_w=characteristics_from_web,
            ch_a=characteristics_from_api,
            at=attrubute_names,
            index=index
        )
        task_id: int = api.upload_item(prepared_data)['task_id']
        upload_status: dict = api.get_upload_status(task_id)
        print(index, upload_status)  # TODO: Here connect to database
