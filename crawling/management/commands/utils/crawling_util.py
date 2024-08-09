from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class CrawlingUtils:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def access(self, url):
        self.driver.get(url)
        sleep(3)