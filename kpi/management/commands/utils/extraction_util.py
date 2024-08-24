import os
import pandas as pd
from django.conf import settings


class ExtractionUtil:
    def __init__(self):
        self.csv_data = []
        self.name_path = self.get_name_path()
        self.sheets = []
        self.results = {}
        self.header = ['氏名']

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

