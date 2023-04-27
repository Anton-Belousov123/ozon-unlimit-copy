import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

from app.telegram import Telegram


class Chrome:
    def __init__(self):
        self.driver = self._login()

    def scrape_product(self, product_id: int) -> dict:
        page_source = self._get_source(product_id)
        characteristics: dict = self._scrape_page_source(page_source)
        return characteristics

    def _get_source(self, product_id: int):
        self.driver.get(f'https://seller.ozon.ru/app/products/{product_id}/edit/preview')
        time.sleep(5)
        return self.driver.page_source

    def _login(self):
        telegram = Telegram()
        item_url = 'https://seller.ozon.ru/app/products/483801974/edit/preview'
        url = 'https://seller.ozon.ru/app/products?filter=all'
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(use_subprocess=True, options=options)
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'button-module_text_2lz6v').click()
        time.sleep(3)
        driver.find_element(By.NAME, 'autocomplete').send_keys('9870739395')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)
        telegram.send_message()
        driver.find_element(By.NAME, 'otp').send_keys(telegram.get_code())  # TODO: Telegram Auth
        time.sleep(5)
        return driver

    def _scrape_page_source(self, page_source: str) -> dict:
        soup = BeautifulSoup(page_source, features='html.parser')
        soup = soup.find('div', {'schema': '[object Object]'}).find_all('div')[1::]

        d = {}
        for index, element in enumerate(soup):
            if 'Характеристики' in element.next:
                continue
            if 'index_row' in str(element):
                response = element.find_all('div')
                d[response[0].text.strip()] = response[1].text.strip().replace('\xa0', '').replace('₽', '')

        if 'Вес с упаковкой, г' in d.keys():
            d['weight'] = d['Вес с упаковкой, г']
            d['weight_unit'] = 'g'
        else:
            d['weight'] = d['Вес с упаковкой, кг']
            d['weight_unit'] = 'kg'
        d['Длина × Ширина × Высота'] = d['Длина × Ширина × Высота'].split(' x ')
        d['depth'] = d['Длина × Ширина × Высота'][0]
        d['width'] = d['Длина × Ширина × Высота'][1]
        d['height'] = d['Длина × Ширина × Высота'][2]
        return d
