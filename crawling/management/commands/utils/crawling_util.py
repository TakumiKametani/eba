import base64
import os
import shutil
import yaml
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from django.conf import settings

class CrawlingUtils:
    def __init__(self, site, target, price=False):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.path = os.path.join(settings.DATA_ROOT, site, target)
        self.counter = 0
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def remove_files(self):
        shutil.rmtree(self.path)
        os.makedirs(self.path)

    def get_auth_header(self, user, password):
        b64 = "Basic " + base64.b64encode('{}:{}'.format(user, password).encode('utf-8')).decode('utf-8')
        return {"Authorization": b64}

    def open_yaml(self):
        with open(os.path.join(settings.BASE_DIR, 'pass.yaml'), 'r', encoding='utf_8') as yml:
            self.config = yaml.safe_load(yml)

    def weekly_login(self):
        self.open_yaml()
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders",
                                         {"headers": self.get_auth_header(self.config['oauth']['name'], self.config['oauth']['pass'])})
        self.access('https://eba-report.xyz/index')
        self.element(selector='//input[@name="login_id"]', _type=By.XPATH, style='input', text=self.config['login']['name'])
        self.element(selector='//input[@name="login_pass"]', _type=By.XPATH, style='input', text=self.config['login']['pass'])
        self.element(selector='//button[@name="accept"]', _type=By.XPATH, style='click')

    def access(self, url):
        self.driver.get(url)
        sleep(5)

    def element(self, selector='', _type='xpath', multi=False, target_num=0, style='get', text='', non_sleep=False):
        if multi:
            element = self.driver.find_elements(by=_type, value=selector)[target_num]
        else:
            element = self.driver.find_element(by=_type, value=selector)
        if style == 'get':
            return element
        if style == 'click':
            element.click()
            if not non_sleep:
                sleep(4)
        if style == 'input':
            element.send_keys(text)

    def execute_script(self, target):
        self.driver.execute_script(target)
        sleep(3)

    def get_html(self):
        return self.driver.page_source

    def save_html(self):
        page_source = self.get_html()

        # HTMLをファイルに保存
        save_path = os.path.join(self.path, f'{self.counter}.html')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(page_source)

    def save_html_plus_word_path(self, key):
        page_source = self.get_html()
        key_path = os.path.join(self.path, key)
        if not os.path.exists(key_path):
            os.makedirs(key_path)
        # HTMLをファイルに保存
        save_path = os.path.join(key_path, f'{self.counter}.html')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(page_source)

    def open_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            rows = f.readlines()
        return rows



