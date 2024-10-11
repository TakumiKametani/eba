import csv
import os
import re
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from .utils.extraction_util import InvoiceExtractionUtil, do_write_csv


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
        util = InvoiceExtractionUtil()
        util.get_key_member()
        excel_path = os.path.join(util.in_path, 'invoice.xlsx')
        util.get_sheet_name(excel_path)
        for sheet in util.sheets:
            util.read(excel_path, sheet)
            print(sheet)
            for index, row in util.df.iterrows():
                try:
                    name = re.sub(r'\s', '', row['氏名'])
                except:
                    continue
                try:
                    dominate = row['上位']
                except:
                    dominate = row['上位(請求先)']
                if not pd.isna(name):
                    if name in util.pairs:
                        name = util.pairs[name]
                    if name in util.data:
                        if util.data[name]['company'] != dominate:
                            util.data[name]['company'] = dominate
                            util.data[name]['counter'] = 1
                        else:
                            util.data[name]['counter'] += 1

        for name in util.data.keys():
            util.data[name]['display'] = util.change(util.data[name]['counter'])
        util.csv_data = [[data['no'], name, data['company'], data['display']] for name, data in util.data.items()]
        now = datetime.now().strftime('%Y%m%d')
        path = os.path.join(util.out_path, f'out_{now}.csv')
        do_write_csv(path, util.header, util.csv_data)

