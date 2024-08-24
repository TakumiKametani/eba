import os
import re
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from .utils.crawling_util import CrawlingUtils
from .utils.beautiful_util import BeautifulUtils
from selenium.webdriver.common.by import By

from django.conf import settings

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--crawling",
            action="store_true",
            default=False,
            help="",
        )
        parser.add_argument(
            "-s",
            "--site",
            default='',
            help="",
        )
        parser.add_argument(
            "-t",
            "--target",
            default='',
            help="",
        )

    def handle(self, *args, **options):
        self.crawling = options.get('crawling', False)
        self.site = options.get('site', False)
        self.target = options.get('target', False)
        util = CrawlingUtils if self.crawling else BeautifulUtils
        self.util = util(self.site, self.target)
        if 'startup' == self.site:
            if not self.crawling:
                if 'index' == self.target:
                    self.header = ['企業名','設立日','従業員数','上場区分','URL','事業内容']
                    self.order = ['company_start', 'employee', 'part', 'url', 'business_detail']
                elif 'detail' == self.target:
                    self.header = ['社名', '設立日', '従業員数', '上場区分', 'URL', '平均年齢', '親会社', '子会社', '大学発', '住所', 'タグ', '事業内容']
                    self.order = None
            self.startup()
        if 'weekly_check' == self.site:
            if not self.crawling:
                if 'index' == self.target:
                    self.header = ['氏名']
            self.weekly_check()

    def startup(self):
        if self.crawling:
            # アカウントは5日間のみの体験で、ログインはできないのと、インデックスも見れないので、コメントアウト
            # self.util.access('https://startup-db.com/login')
            # self.util.element(selector="//input[@type='email']", _type=By.XPATH, style='input', string='t.kametani@ebacorp.jp')
            # self.util.element(selector="//input[@type='password']", _type=By.XPATH, style='input', string='egAU1pm9hMW20mhv')
            # self.util.element(selector="//button[@data-v-20a634db]", _type=By.XPATH, style='click')
            # if 'index' == self.target:
            #     for i in range(1, 1032):
            #     # for i in [108,280,290,297,381,385,415,424,43,451,455,538,56]:
            #         self.util.counter += 1
            #         # self.util.counter = i
            #         try:
            #             self.util.access(f'https://startup-db.com/companies?page={i}')
            #             self.util.save_html()
            #         except:
            #             break
            if 'detail' == self.target:
                path = os.path.join(settings.DATA_ROOT, self.site, 'satrt_up_detail_urls')
                # self.util.counter = 3673
                for row in self.util.open_file(path):
                    self.util.counter += 1
                    print(self.util.counter)
                    url = row.replace('\n', '')
                    try:
                        self.util.access(url)
                        self.util.save_html()
                    except:
                        print(url)
                        break
        else:
            if 'index' == self.target:
                '''
                ['企業名','設立日','従業員数','上場区分','URL','事業内容']
                '''
                domain = 'https://startup-db.com'
                files = os.listdir(self.util.path)
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(self.util.path, filename))
                    corps = soup.find_all('tr', class_='data-row')
                    for corp in corps:
                        tds = corp.find_all('td')
                        a_tag = corp.find('a', class_='company-name')
                        corp_name = re.sub(r'\n|\t|\s', '', a_tag.get_text())
                        url = domain + a_tag.get('href')
                        company_start = re.sub(r'\n|\t|\s', '', tds[5].get_text())
                        business_detail = re.sub(r'\n|\t|\s', '', tds[4].get_text())
                        part = re.sub(r'\n|\t|\s', '', tds[3].get_text())
                        employee = re.sub(r'\n|\t|\s', '', tds[7].get_text())
                        if corp_name not in self.util.csv_data:
                            self.util.csv_data[corp_name] = {
                                'url': url,
                                'company_start': company_start,
                                'business_detail': business_detail,
                                'part': part,
                                'employee': employee
                            }
                csv_data = [[key, v[self.order[0]], v[self.order[1]], v[self.order[2]], v[self.order[3]], v[self.order[4]]] for key, v in self.util.csv_data.items()]
                self.util.do_write_csv(self.header, csv_data)
            elif 'detail' == self.target:
                '''
                ['社名', '設立日', '従業員数', '上場区分', 'URL', '平均年齢', '親会社', '子会社', '大学発', '住所', 'タグ', '事業内容']
                '''
                self.util.csv_data = []
                files = os.listdir(self.util.path)
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(self.util.path, filename))
                    container = soup.find('div', class_='container', attrs={'data-v-204f294a': ''})
                    if not container:
                        continue
                    dls = container.find_all('dl')
                    dl_1, dl_2 = dls[0], dls[1]
                    dl_1_dds = dl_1.find_all('dd')
                    corp_name = re.sub(r'\n|\t|\s', '', dl_1_dds[0].get_text())
                    start = re.sub(r'\n|\t|\s', '', dl_1_dds[1].get_text())
                    university = re.sub(r'\n|\t|\s', '', dl_1_dds[2].get_text())
                    address = dl_1_dds[3].get_text()
                    dl_2_dds = dl_2.find_all('dd')
                    url = re.sub(r'\n|\t|\s', '', dl_2_dds[0].get_text())
                    employee = re.sub(r'\n|\t|\s', '', dl_2_dds[1].get_text())
                    ave = re.sub(r'\n|\t|\s', '', dl_2_dds[2].get_text())
                    parent = re.sub(r'\n|\t|\s', '', dl_2_dds[3].get_text())
                    child = re.sub(r'\n|\t|\s', '', dl_2_dds[4].get_text())
                    description = re.sub(r'\n', '', soup.find('div', class_='col col-description').get_text())
                    part = re.sub(r'\n|\t|\s', '', soup.find('div', class_='CompanyLabel company-labels').get_text())
                    tag = re.sub(r'\n', ' ', soup.find_all('div', class_='row row-wrap')[0].get_text().replace(' ', ''))
                    self.util.csv_data += [[corp_name, start, employee, part, url, ave, parent, child, university, address, tag, description]]
                self.util.do_write_csv(self.header, self.util.csv_data)


    def weekly_check(self):
        if self.crawling:
            self.util.access('https://eba-report.xyz/subordinate_leader_list')
            # OAuth認証があるから、一度止めてログインしてから、続きを流す。
            a = 1
            for i in [
                # 幹部
                20, 75, 126, 81, 99, 66, 84, 113, 207, 335, 244, 278, 262, 374, 261,
                # リーダー
                107, 115, 118, 268, 85, 103, 165, 209, 242, 311, 356, 366, 480,
                220, 228, 184, 282, 290, 406, 500, 450, 454, 351, 410, 481, 534, 91,
                43, 61, 65, 90, 123, 127, 130, 140, 173, 187, 189,
                218, 236, 249, 251, 253, 260,
                264, 285, 319, 409, 499,
                # 研修担当
                316, 653
            ]:
                self.util.counter += 1
                url = f'https://eba-report.xyz/subordinate_leader_detail?leader_member_no={i}'
                sleep(1)
                try:
                    self.util.access(url)
                    self.util.save_html()
                except:
                    print(url)
                    continue
            pass
        else:
            csv_data = []
            for i in range(1, 100):
                path = os.path.join(self.util.path, f'{i}.html')
                if not os.path.exists(path):
                    break
                soup = self.util.soup_util(path)
                if i == 1:
                    headers = soup.find_all('table')[3].find_all('th')
                    for h in headers:
                        if h.get_text() not in ['ID', 'メンバー名']:
                            self.header += [re.sub(r'提出不要|保存のみ|\s|\t|\n', '', h.get_text()) + '未提出', 'OK', 'NG']
                _bodys = soup.find_all('tbody')
                name = re.sub(r'（自分）|\s|\t|\n', '', _bodys[0].find('td').get_text())
                data = []
                rows = []
                for tr in _bodys[1].find_all('tr'):
                    a_text = re.sub(r'\s|\t|\n', '', tr.find('a').get_text())
                    if name == '亀谷匠' and a_text in ['鈴木雄紀', '栗原なみ', '船木裕矢', '三橋優也', '栗山堅太郎', '品田彩光', '山崎省吾']:
                        continue
                    rows += [[re.sub(r'\s|\t|\n|（.+）', '', td.get_text()) for td in tr.find_all('td') if 'OK' in td.get_text() or 'NG' in td.get_text() or '未提出' in td.get_text()]]
                for i in range(0, len(rows[0])):
                    data += [[row[i] for row in rows]]
                result = [name]
                for d in data:
                    result += [d.count('未提出'), d.count('OK'), d.count('NG')]
                csv_data += [result]

            self.util.do_write_csv(self.header, csv_data)


