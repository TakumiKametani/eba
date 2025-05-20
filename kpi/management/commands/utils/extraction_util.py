import csv
import os
import pandas as pd
import yaml
from datetime import datetime
from django.conf import settings


class SkillSheetExtractionUtil:
    def __init__(self):
        self.csv_data = []
        self.name_path = self.get_name_path()
        self.sheets = []
        self.results = {}
        self.header = [
            '氏名', 'Java', 'Spring', 'Struts', 'Seasar2', 'JSP', 'Thymeleaf', 'JUnit',
            'PHP', 'Laravel', 'CakePHP', 'Symfony', 'FuelPHP', 'CodeIgniter',
            'Zend', 'Yii', 'Slim', 'Smarty', 'Python', 'Django', 'FastAPI',
            'Flask', 'Phalcon', 'TensorFlow', 'Keras', 'Go言語', 'Rust', 'Ruby',
            'Ruby on Rails', 'C言語', 'C#', 'ASP.NET', '.NETFramework', 'C++',
            'Pro*C', 'Perl', 'R言語', 'Swift', 'Kotlin', 'Objective-C', 'Unity',
            'UnrealEngine', 'Xcode', 'COBOL', 'VBA', 'Gosu', 'GAS', 'BigQuery',
            'ローコード', 'Tableau', 'JavaScript', 'TypeScript', 'Dart', 'Flutter',
            'React', 'Next.js', 'MaterialUI', 'Vue.js', 'Vuex', 'Vuetify',
            'Nuxt.js', 'Angular', 'Node.js', 'Nest.js', 'Express', 'jQuery',
            'ReactNative', 'AngularJS', 'AWS', 'GCP', 'Azure', 'MySQL',
            'PostgreSQL', 'OracleDB', 'SQLite', 'DB2', 'MongoDB', 'ストアドプロシージャ',
            'SQLServer', 'MariaDB', 'DynamoDB', 'Firebase', 'GraphQL', 'PL/SQL',
            'Bash', 'Shell script', 'PowerShell', 'Docker', 'Cisco', 'PM', 'PL',
            'PMO', 'マネジメント', 'ディレクション', 'プロジェクト管理', '顧客折衝', '見積',
            '要件定義', '基本設計', '詳細設計', 'XD', 'Figma', 'Dreamweaver',
            'InDesign', 'UI/UX', 'WordPress', 'Photoshop', 'Illustrator', 'HTML',
            'CSS', 'Sass', '企画', '調査', 'サーバ設計', 'サーバ構築', 'ベンダーコントロール',
            'AzureAD', 'Hyper-V', 'VMWare', 'UNIX', 'RHEL', 'CentOS', 'Ubuntu',
            'WindowsServer', 'SharePoint', 'Zabbix'
        ]

    def read(self, file, index_col=1):
        try:
            self.df = pd.read_excel(file, engine="openpyxl", header=None, index_col=index_col, skiprows=9)
        except:
            self.df = pd.read_excel(file, header=None, index_col=index_col, skiprows=9)

    def get_name_path(self):
        parent = os.path.join(settings.SKILL_SHEET, 'input')
        tops = [os.path.join(parent, x) for x in os.listdir(parent)]
        hira_list = []
        name_path = {}
        for top in tops:
            _hira = os.listdir(top)
            for hira in _hira:
                hira_list += [os.path.join(top, hira)]

        for hira_path in hira_list:
            names = os.listdir(hira_path)
            for name in names:
                name_path[name] = os.path.join(hira_path, name)
        return name_path


class InvoiceExtractionUtil:
    def __init__(self):
        self.in_path = os.path.join(settings.INVOICE_PATH, 'input')
        self.out_path = os.path.join(settings.INVOICE_PATH, 'output')
        self.sheets = []
        self.data = {}
        self.csv_data = []
        self.header = ['no', '氏名', '上位', '参画期間']
        self.open_yaml()
        self.pairs = self.config['pair_name']

    def open_yaml(self):
        with open(os.path.join(settings.BASE_DIR, 'pass.yaml'), 'r', encoding='utf_8') as yml:
            self.config = yaml.safe_load(yml)

    def get_sheet_name(self, file):
        xl = pd.ExcelFile(file)
        self.sheets = xl.sheet_names
    def read(self, file, sheet):
        try:
            self.df = pd.read_excel(file, sheet_name=sheet)
        except:
            self.df = pd.read_excel(file, engine="openpyxl", sheet_name=sheet)

    def get_key_member(self):
        path = os.path.join(self.in_path, '社員マスタ.csv')
        with open(path, 'r', encoding='utf-8-sig') as f:
            self.data = {
                row.replace('\n', '').split(',')[1]: {
                    'company': '',
                    'counter': 0,
                    'no': int(row.replace('\n', '').split(',')[0]),
                    'display': ''
                } for row in f.readlines()
            }

    def change(self, nom):
        year = nom // 12
        month = nom % 12
        display = f'{year}年{month}ヶ月' if year else f'{month}ヶ月'
        return display


def do_write_csv(path, header, data):
    with open(path, 'w', newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)