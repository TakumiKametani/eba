import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--target",
            help="",
        )

    def handle(self, *args, **options):
        target = options.get('target', '')
        # CSVを格納したディレクトリから、ファイル一覧を取得
        files = os.listdir(settings.WEEKLY)
        for _file in files:
            name = ''
            name_flg = False
            data = []
            data_weekly_flg = False
            data_date_flg = False
            path = os.path.join(settings.WEEKLY, _file)
            with open(path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if ['社員名'] == row:
                        name_flg = True
                        continue
                    if name_flg:
                        name = row[0]
                        name_flg = False
                        continue
                    if '年月週' == row[0]:
                        data_weekly_flg = True
                        data_date_flg = False
                        continue
                    if data_weekly_flg:
                        data += [[row[0], '------------------------------']]
                        data += [['学んだこと', row[1]]]
                        data += [['コメント', row[2]]]
                        data_weekly_flg = False
                        continue
                    if '日付' == row[0]:
                        data_date_flg = True
                        continue
                    if data_date_flg:
                        data += [[row[0], row[1]]]
                        continue

            self.do_write_csv(name + target + '.csv', data)

    def do_write_csv(self, filename, data):
        with open(os.path.join(settings.WEEKLY, filename), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

