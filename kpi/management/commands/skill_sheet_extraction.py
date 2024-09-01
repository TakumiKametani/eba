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
                if key in ['人物像', '実績（一部）', '【人物像】', '業務実績']:
                    break
                if isinstance(key, int):
                    print(key)
                    print(file)
                    continue
                if re.search(r'～|保守|運用|≪社内', key) or key in ['対応工程', '言語・フレームワーク', 'OS・NW機器・サーバー等', '言語・フレームワーク・DB・サーバー', '資格', '対応可能工程', '習得資格', 'OS・NW機器・サーバー・ツール等', '【NW機器】', '【ツール】', 'その他']:
                    continue
                key = re.sub(r'\s|\t|\u3000|（.+）|\(.+\)|\(.+）|（.+\)|※.+|独学|経験', '', key)
                key = self.key_change(key)
                if 'Photoshop、Illustrator、XD' == key or 'React.js/Next.js' == key:
                    for _key in key.split('、'):
                        if _key not in util.header:
                            util.header += [_key]
                        util.results[name][_key] = ''
                else:
                    if key not in util.header:
                        util.header += [key]
                    util.results[name][key] = ''
                for value in data[1]:
                    if pd.isna(value):
                        continue
                    if re.match(r'.年.+月$|.+月|.年$', value):
                        if re.match(r'.年$', value):
                            value = value.replace('年', '年0ヶ月')
                        if 'Photoshop、Illustrator、XD' == key or 'React.js/Next.js' == key or 'Vue.js/React' == key:
                            if 'Photoshop、Illustrator、XD' == key:
                                _split = key.split('、')
                            elif 'React.js/Next.js' == key or 'Vue.js/React' == key:
                                _split = key.split('/')
                            for _key in _split:
                                if 'React.js' == _key:
                                    _key = 'React'
                                util.results[name][_key] = re.sub(r'カ|ヵ|か', 'ヶ', re.sub(r'\s|\t', '', value))
                        else:
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
        with open(path, 'w', newline='', encoding='utf_8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

    def key_change(self, key):
        if key == 'C':
            key = 'C言語'
        elif 'Spring' in key:
            key = 'Spring'
        elif 'Postg' in key:
            key = 'PostgreSQL'
        elif key == 'Javascript' or key == 'JS':
            key = 'JavaScript'
        elif 'css' in key.lower():
            key = 'CSS'
        elif 'css' in key.lower():
            key = 'CSS'
        elif 'Angular.js' == key:
            key = 'AngularJS'
        elif 'PosgreSQL' == key:
            key = 'PostgreSQL'
        elif 'RHEL6/CentOS6' == key:
            key = 'RHEL6'
        elif 'Vuejs' == key:
            key = 'Vue.js'
        elif '' == key:
            key = ''
        elif '' == key:
            key = ''
        elif '' == key:
            key = ''
        elif '' == key:
            key = ''
        elif key in ['React.js', 'ReactJS']:
            key = 'React'
        elif key in ['ASP', 'ASP.net.1', 'ASP.NETCoreMVC']:
            key = 'ASP.NET'
        elif key in ['Go.1', 'GoLang', 'golang.1', 'Go言語']:
            key = 'Go'
        elif key in ['illustrator.1', 'Ilustrator']:
            key = 'Illustrator'
        elif key in ['Jquery.1', 'JQuery.2']:
            key = 'jQuery'
        elif key in ['PremierePro', 'PremierPro', 'PremirePro']:
            key = 'Premiere Pro'
        elif key in ['Python3']:
            key = 'Python'
        elif key in ['RubyonRails', 'RubyOnRails.1']:
            key = 'Ruby on Rails'
        elif key in ['']:
            key = ''


        elif 'CakePHP' in key:
            key = 'CakePHP'
        elif 'HTML' in key:
            key = 'HTML'
        elif 'Java' in key:
            key = 'Java'




        return key