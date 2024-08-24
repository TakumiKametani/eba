import csv
import os
import re
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from .utils.extraction_util import ExtractionUtil


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        # parser.add_argument(
        #     "-t",
        #     "--target",
        #     help="",
        # )
        pass

    def handle(self, *args, **options):


        util = ExtractionUtil()
        for name, path in util.name_path.items():
            util.results[name] = {}
            try:
                _file = os.path.join(path, os.listdir(path)[0])
                if os.path.isfile(_file):
                    file = _file
                else:
                    print(_file)
                    continue
            except:
                continue
            util.read(file)
            for data in util.df.iterrows():
                if pd.isna(data[0]):
                    continue
                key = data[0]
                if key in ['人物像', '実績（一部）']:
                    break
                if re.search(r'～|保守|運用', key) or key in ['対応工程', '言語・フレームワーク', 'OS・NW機器・サーバー等', '言語・フレームワーク・DB・サーバー', '資格', '対応可能工程', '習得資格']:
                    continue
                key = re.sub(r'\s|\t|\u3000|（.+）|\(.+\)|\(.+）|（.+\)|※.+|', '', key)
                if key == 'C':
                    key = 'C言語'
                if 'Spring' in key:
                    key = 'Spring'
                if 'Postg' in key:
                    key = 'PostgreSQL'
                if key == 'Javascript':
                    key = 'JavaScript'
                if key not in util.header:
                    util.header += [key]
                util.results[name][key] = ''
                for value in data[1]:
                    if pd.isna(value):
                        continue
                    if re.match(r'.年.+月$|.+月|.年$', value):
                        util.results[name][key] = re.sub(r'カ|ヵ|か', 'ヶ', re.sub(r'\s|\t', '', value))
                        break

        for name, skills in util.results.items():
            data = [re.sub(r'K|JAVA|JS|PHP|N|F|inf|さん$', '', name)]
            for target in util.header[1::]:
                if target == '':
                    continue
                data += [skills.get(target, '')]
            util.csv_data += [data]
        _now = datetime.strftime(datetime.now().date(), '%Y%m%d')
        path = os.path.join(settings.SKILL_SHEET, 'output', f'result_{_now}.csv')
        self.do_write_csv(path, util.header, util.csv_data)



        a = 1

    def do_write_csv(self, path, header, data):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

