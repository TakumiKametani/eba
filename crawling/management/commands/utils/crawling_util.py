import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from django.conf import settings

class CrawlingUtils:
    def __init__(self, site, target):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.path = os.path.join(settings.DATA_ROOT, site, target)
        self.counter = 0
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def access(self, url):
        self.driver.get(url)
        sleep(5)

    def element(self, selector='', _type='', multi=False, target_num=0, style='get', string=''):
        if multi:
            element = self.driver.find_elements(by=_type, value=selector)[target_num]
        else:
            element = self.driver.find_element(by=_type, value=selector)
        if style == 'get':
            return element
        if style == 'click':
            element.click()
            sleep(3)
        if style == 'input':
            element.send_keys(string)

    def get_html(self):
        return self.driver.page_source

    def save_html(self):
        page_source = self.get_html()

        # HTMLをファイルに保存
        save_path = os.path.join(self.path, f'{self.counter}.html')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(page_source)

    def open_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            rows = f.readlines()
        return rows



