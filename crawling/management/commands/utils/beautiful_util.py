import csv
import os
import re
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from django.conf import settings

class BeautifulUtils:
    def __init__(self, site, target, price=False):
        self.path = os.path.join(settings.DATA_ROOT, site, target)
        self.site = site
        self.target = target
        self.keys = []
        self.data = {}
        self.csv_data = []
        self.summary_header = []
        self.price = price

    def soup_util(self, file):

        return BeautifulSoup(open(file, encoding="utf-8"), 'html.parser')

    def do_write_csv(self, header, data):
        _yyyymmdd = datetime.strftime(datetime.now(), '%Y%m%d')
        price = '_price' if self.price else ''
        filename = f'{self.site}_{self.target}{price}_{_yyyymmdd}.csv'
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

    def mynavi_util(self, domain, corp):
        url, corp_start, location, employee, description = [''] * 5
        title_tag = corp.find('div', class_='recruit_head')
        name = re.sub(r'\s|\|.+', '', title_tag.find('p', class_='main_title').get_text())
        url = domain + title_tag.find('a').get('href')
        _description = corp.find('th', text='仕事内容')
        if _description:
            description = re.sub(r'\s|\t|\n', '', _description.parent.find('td').get_text())
        p_text = corp.find('p', class_='company_data').get_text().replace('企業データ', '').split('／')
        if len(p_text) == 2:
            if '設立：' in p_text[0]:
                corp_start = re.sub(r'設立：', '', p_text[0])
                employee = '-'
            else:
                corp_start = '-'
                employee = re.sub(r'従業員数：', '', p_text[0])
            location = re.sub(r'本社所在地：|\s|\t|\n', '', p_text[1])
        elif len(p_text) == 3:
            corp_start = re.sub(r'設立：', '', p_text[0])
            employee = re.sub(r'従業員数：', '', p_text[1])
            location = re.sub(r'本社所在地：|\s|\t|\n', '', p_text[2])
        return name, url, corp_start, location, employee, description

    def green_util(self, domain, corp):
        url, location, talent = [''] * 3
        name = re.sub(r'\s|\t|\n', '',
                      corp.find('div', class_='MuiTypography-root MuiTypography-subtitle2 css-k1ckjv').get_text())
        url = domain + corp.find('a').get('href', 'ERROR')
        location = corp.find('div', attrs={'aria-label': '勤務地'}).get_text()
        talent = corp.find('div', attrs={'aria-label': '募集職種'}).get_text()
        return name, url, location, talent