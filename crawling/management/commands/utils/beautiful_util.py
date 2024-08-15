import csv
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from django.conf import settings

class BeautifulUtils:
    def __init__(self, site, target):
        self.path = os.path.join(settings.DATA_ROOT, site, target)
        self.site = site
        self.target = target
        self.csv_data = {}

    def soup_util(self, file):

        return BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')

    def do_write_csv(self, header, data):
        _yyyymmdd = datetime.strftime(datetime.now(), '%Y%m%d')
        filename = f'{self.site}_{self.target}_{_yyyymmdd}.csv'
        with open(os.path.join(settings.DATA_ROOT, self.site, filename), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)