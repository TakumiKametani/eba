import csv
import os
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from django.conf import settings

class BeautifulUtils:
    def __init__(self, site, target):
        self.path = os.path.join(settings.DATA_ROOT, site, target)
        self.site = site
        self.target = target
        self.keys = []
        self.data = {}
        self.csv_data = []
        self.summary_header = []

    def soup_util(self, file):

        return BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')

    def do_write_csv(self, header, data):
        _yyyymmdd = datetime.strftime(datetime.now(), '%Y%m%d')
        filename = f'{self.site}_{self.target}_{_yyyymmdd}.csv'
        path = os.path.join(settings.DATA_ROOT, self.site, filename)
        with open(path, 'w', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            if header:
                writer.writerow(header)
            writer.writerows(data)
        if len(data) >= 5000:
            self._chunks(path)

    def _chunks(self, path):
        chunk_size = 2000
        chunks = pd.read_csv(path, chunksize=chunk_size)
        _yyyymmdd = datetime.strftime(datetime.now(), '%Y%m%d')
        for i, chunk in enumerate(chunks):
            filename = f'{self.site}_{self.target}_{_yyyymmdd}_{i}.csv'
            chunk.to_csv(os.path.join(settings.DATA_ROOT, self.site, filename), index=False)

    def do_write_xlsx(self, header):
        now = datetime.now().date().strftime('%Y%m%d')
        filename = f'{self.site}_{now}.xlsx'
        path = os.path.join(settings.DATA_ROOT, self.site, filename)
        with pd.ExcelWriter(path) as writer:
            df_summary = pd.DataFrame(self.data['summary'], columns=self.summary_header)
            df_summary.to_excel(writer, sheet_name='集計', index=False)
            for key in self.keys:
                df = pd.DataFrame(self.data[key]['data'], columns=header)
                df.to_excel(writer, sheet_name=key, index=False)
