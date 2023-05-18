import json
import time

from bs4 import BeautifulSoup
import requests

from app import db
from app.api import Api
from app.web import Chrome


def prepare_data_to_upload(ch_w: dict, ch_a: dict, at: list[dict], name, article) -> dict:
    data = {
        'items': [
            {
                'attributes': at,
                'category_id': ch_a['category_id'],
                'depth': ch_w['depth'],
                'dimension_unit': 'mm',
                'height': ch_w['height'],
                'images': ['https://ir.ozone.ru/s3/multimedia-t/6382045493.jpg',
                           'https://ir.ozone.ru/s3/multimedia-l/6332904873.jpg',
                           'https://ir.ozone.ru/s3/multimedia-m/6332904874.jpg',
                           'https://ir.ozone.ru/s3/multimedia-k/6332904872.jpg',
                           'https://ir.ozone.ru/s3/multimedia-p/6332904877.jpg',
                           'https://ir.ozone.ru/s3/multimedia-j/6332904871.jpg'],
                'name': name,#ch_w['Название'],
                'offer_id': "РСВ-" + str(article) + "РСВ-" + str(article),
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
    chrome = Chrome()
    api = Api()
    while True:
        try:
            product_id, name, sku = db.get_code()
            upload_status, new_product_id = api.test_upload(product_id, name, sku)
            if upload_status is False:
                print('Режим ручной загрузки')
                while True:
                    #try:
                    if True:
                        characteristics_from_web: dict = chrome.scrape_product(new_product_id)
                    #except:
                    #    chrome = Chrome()
                    #    continue
                    break
                print("WEB CHARACTERISTIC PARSED!!!")
                characteristics_from_api: dict = api.scrape_product(new_product_id)
                print("CHARACTERISTIC PARSED!!!")
                attribute_names_from_api: dict = api.scrape_attribute_names(category_id=characteristics_from_api['category_id'])
                print("ATRIBUTES PARSED!!!")
                attrubute_names = get_attributes(attribute_names_from_api, characteristics_from_web, characteristics_from_api, api)
                print("ATRIBUTES GETTED!")
                prepared_data: dict = prepare_data_to_upload(
                    ch_w=characteristics_from_web,
                    ch_a=characteristics_from_api,
                    at=attrubute_names,
                    name=name,
                    article=product_id
                )
                print('DATA PREPARED!!!')
                api.upload_item(prepared_data)
                print('UPLOADED!!!')
            else:
                api.upload_to_main(product_id, name, sku)
        except Exception as e:
            print(e)
            print("EXception add")
        try:
            db.update_status(product_id)
        except:
            print("Exception update db")
            time.sleep(30)
