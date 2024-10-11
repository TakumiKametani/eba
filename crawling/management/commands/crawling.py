import os
import re
from numpy import mean
from time import sleep
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from .utils.crawling_util import CrawlingUtils
from .utils.beautiful_util import BeautifulUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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
        parser.add_argument(
            "-p",
            "--price",
            action="store_true",
            default=False,
            help="",
        )


    def handle(self, *args, **options):
        self.crawling = options.get('crawling', False)
        self.site = options.get('site', '')
        self.target = options.get('target', '')
        self.price = options.get('price', False)
        self.create_header_target()
        util = CrawlingUtils if self.crawling else BeautifulUtils
        self.util = util(self.site, self.target, self.price)
        if self.crawling:
            self.util.remove_files()
        if 'startup' == self.site:
            self.startup()
        elif 'mynavi' == self.site:
            self.mynavi()
        elif 'tensyoku_ex' == self.site:
            self.tensyoku_ex()
        elif 'rikunabi' == self.site:
            self.rikunabi()
        elif 'en_japan' == self.site:
            self.en_japan()
        elif 'green' == self.site:
            self.green()
        elif 'indeed' == self.site:
            self.indeed()
        elif 'levtech_career' == self.site:
            self.levtech_career()
        elif 'levtech_freelance_analysis' == self.site:
            self.levtech_freelance_analysis()
        elif 'pe_bank_analysis' == self.site:
            self.pe_bank_analysis()
        elif 'geechs_analysis' == self.site:
            self.geechs_analysis()
        elif 'it_pro_partner_analysis' == self.site:
            self.it_pro_partner_analysis()

        elif 'open_work' == self.site:
            self.open_work()
        elif 'wantedly' == self.site:
            self.wantedly()
        elif 'willoftech' == self.site:
            self.willoftech()
        elif 'weekly_check_submission' == self.site:
            self.weekly_check_submission()
        elif 'weekly_download' == self.site:
            self.weekly_download()

        elif 'weekly_check' == self.site:
            if not self.crawling:
                if 'index' == self.target:
                    self.header = ['氏名']
            self.weekly_check()
        if not self.crawling:
            if self.site in ['levtech_freelance_analysis', 'pe_bank_analysis', 'geechs_analysis', 'it_pro_partner_analysis']:
                self.util.do_write_xlsx(self.header)
            else:
                self.util.do_write_csv(self.header, self.util.csv_data)

    def create_header_target(self):
        self.header_order = {
            'startup': {
                'index': {
                    'header': ['企業名', '設立日', '従業員数', '上場区分', 'URL', '事業内容'],
                    'order': ['company_start', 'employee', 'part', 'url', 'business_detail']
                },
                'detail': {
                    'header': ['社名', '設立日', '従業員数', '上場区分', 'URL', '平均年齢', '親会社', '子会社',
                           '大学発', '住所', 'タグ', '事業内容'],
                    'order': None
                },
            },
            'mynavi': {
                'index': {
                    'header': ['会社名','詳細ページURL', '設立日', '所在地','従業員数','仕事内容'],
                    'order': ['url', 'corp_start', 'location', 'employee', 'description'],
                    'price_header': ['会社名', '最低給与', '最大給与','詳細ページURL', '設立日', '所在地','従業員数','仕事内容'],
                },
            },
            'tensyoku_ex': {
                'index': {
                    'header': ['会社名','詳細ページURL', '勤務地', '仕事内容', '応募資格'],
                    'order': ['url', 'location', 'detail', 'requirements']
                },
            },
            'rikunabi': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '業態or業種', '所在地', '求める人材'],
                    'order': ['url', 'industry', 'location', 'talent']
                },
            },
            'en_japan': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '所在地', '求める人材'],
                    'order': ['url', 'location', 'talent']
                },
            },
            'green': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '所在地', '求める人材'],
                    'order': ['url', 'location', 'talent'],
                    'price_header': ['会社名', '最低給与', '最大給与', '詳細ページURL', '所在地', '求める人材'],
                },
            },
            'indeed': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '所在地', '求める人材'],
                    'order': ['url', 'location', 'talent']
                },
            },
            'levtech_career': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '所在地', '事業内容'],
                    'order': ['url', 'location', 'detail']
                },
            },
            'levtech_freelance_analysis': {
                'index': {
                    'header': ['案件名', '単価', '所在地', '開発環境', '求めるスキル', '募集職種', 'URL'],
                    'order': ['name', 'price', 'location', 'environ', 'skill', 'jobs', 'url']
                },
            },
            'pe_bank_analysis': {
                'index': {
                    'header': ['案件名', '最低単価', '最高単価', '所在地', '内容', 'スキル', 'URL'],
                    'order': ['name', 'min_price', 'max_price', 'location', 'jobs', 'skill', 'url']
                },
            },
            'geechs_analysis': {
                'index': {
                    'header': ['案件名', '最低単価', '最高単価', '所在地', '内容', 'スキル', 'URL'],
                    'order': ['name', 'min_price', 'max_price', 'location', 'jobs', 'skill', 'url']
                },
            },
            'it_pro_partner_analysis': {
                'index': {
                    'header': ['案件名', '単価', '開発環境', '内容', 'スキル', 'URL'],
                    'order': ['name', 'price', 'env', 'jobs', 'skill', 'url']
                },
            },



            'open_work': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '所在地', '求める人材'],
                    'order': ['url', 'location', 'talent']
                },
            },
            'wantedly': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '求める人材'],
                    'order': ['url', 'talent']
                },
            },
            'willoftech': {
                'index': {
                    'header': ['会社名', '詳細ページURL', '業態or業種', '所在地', '求める人材'],
                    'order': ['url', 'industry', 'location', 'talent']
                },
            },

            'weekly_check_submission': {
                'index': {
                    'header': [],
                    'order': []
                },
            },
            'weekly_download': {
                'index': {
                    'header': [],
                    'order': []
                },
            },

            'sample': {
                'index': {
                    'header': [],
                    'order': []
                },
            },


        }
        try:
            self.header = self.header_order[self.site].get(self.target, {}).get('header' if not self.price else 'price_header', [])
            self.order = self.header_order[self.site].get(self.target, {}).get('order', [])
        except Exception as e:
            print(e)
            pass

    def startup(self):
        # if not self.crawling:
        #     if 'index' == self.target:
        #         self.header = ['企業名', '設立日', '従業員数', '上場区分', 'URL', '事業内容']
        #         self.order = ['company_start', 'employee', 'part', 'url', 'business_detail']
        #     elif 'detail' == self.target:
        #         self.header = ['社名', '設立日', '従業員数', '上場区分', 'URL', '平均年齢', '親会社', '子会社',
        #                        '大学発', '住所', 'タグ', '事業内容']
        #         self.order = None
        if self.crawling:
            # アカウントは5日間のみの体験で、ログインはできないのと、インデックスも見れないので、コメントアウト
            # self.util.access('https://startup-db.com/login')
            # self.util.element(selector="//input[@type='email']", _type=By.XPATH, style='input', text='t.kametani@ebacorp.jp')
            # self.util.element(selector="//input[@type='password']", _type=By.XPATH, style='input', text='egAU1pm9hMW20mhv')
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
                        if corp_name not in self.util.data:
                            self.util.data[corp_name] = {
                                'url': url,
                                'company_start': company_start,
                                'business_detail': business_detail,
                                'part': part,
                                'employee': employee
                            }
                self.util.csv_data = [[key, v[self.order[0]], v[self.order[1]], v[self.order[2]], v[self.order[3]], v[self.order[4]]] for key, v in self.util.data.items()]
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

    def mynavi(self):
        if self.crawling:
            self.util.access('https://tenshoku.mynavi.jp/shutoken/list/p11+p12+p13+p14/o16+o1G1+o1G225/?ags=0')
            self.util.counter = 1
            self.util.save_html()
            for i in range(1, 10000):
                self.util.counter += 1
                try:
                    self.util.element(selector='//li[@class="pager_item pager_next"]/a', _type=By.XPATH, style='click')
                    self.util.save_html()
                except:
                    print(self.util.counter)
                    break
            pass
        else:
            domain = 'https://tenshoku.mynavi.jp'
            files = os.listdir(self.util.path)
            if not self.price:
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(self.util.path, filename))
                    corps = soup.find_all('section', class_='recruit')
                    for corp in corps:
                        name, url, corp_start, location, employee, description = self.util.mynavi_util(domain, corp)
                        if name not in self.util.data:
                            self.util.data[name] = {
                                'url': url,
                                'corp_start': corp_start,
                                'location': location,
                                'employee': employee,
                                'description': description,
                            }
                        else:
                            self.util.data[name]['description'] += ' ' + description
                self.util.csv_data = [[key, v[self.order[0]], v[self.order[1]], v[self.order[2]], v[self.order[3]], v[self.order[4]]] for key, v in self.util.data.items()]
            else:
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(self.util.path, filename))
                    corps = soup.find_all('section', class_='recruit')
                    for corp in corps:
                        name, url, corp_start, location, employee, description = self.util.mynavi_util(domain, corp)
                        min_price, max_price = [''] * 2
                        _price = corp.find('p', class_='fwb')
                        if _price:
                            try:
                                _price = re.sub(r',|万円', '', _price.find('span').get_text()).split('～')
                                min_price = int(_price[0] + '0000')
                                max_price = int(_price[1] + '0000')
                            except:
                                pass

                        self.util.csv_data += [[name, min_price, max_price, url, corp_start, location, employee, description]]


    def rikunabi(self):
        if self.crawling:
            self.util.access('https://next.rikunabi.com/search/')
            self.util.execute_script('document.getElementsByClassName("rn3-selectBody__button js-searchModalOpen")[0].click()')
            self.util.execute_script('document.querySelector("body > div:nth-child(12) > div.modal > div.modalWrapper > div > div.searchModal > div:nth-child(2) > ul > li:nth-child(4) > label").click()')
            self.util.execute_script('document.querySelector("body > div:nth-child(12) > div.modal > div.modalWrapper > div > div.searchModal > div:nth-child(2) > ul > li:nth-child(3) > label").click()')
            self.util.execute_script('document.querySelector("body > div:nth-child(12) > div.modal > div.modalWrapper > div > div.searchModal > div.searchModalFooter > div.searchModalFooter__right > div.searchModalFooter__btn.searchModalFooter__btn--primary").click()')
            self.util.execute_script('document.querySelector("#js-searchPanel > div.rn3-floatingBottom.js-floatingBottom > div > div.rn3-floatingBottom__button > button").click()')

            self.util.counter = 1
            self.util.save_html()
            for i in range(1, 10000):
                self.util.counter += 1
                try:
                    self.util.execute_script('document.querySelector("body > div.rnn-wrapper.js-rnnWrapper > div.rnn-mainContentsBack.rnn-resultSearch > div > div.rnn-row.rnn-row--gutter-xm > div.rnn-col-9.rnn-group.rnn-group--xm.js-resultSearch.rnn-col-offset-3 > div.rnn-group.rnn-group--xm > div.rnn-group.rnn-group--xs > div > ul > li.rnn-pagination__next > a").click()')
                    self.util.save_html()
                except:
                    break
        else:
            url, industry, location, talent = [''] * 4
            domain = 'https://next.rikunabi.com'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find('ul', class_='rnn-group rnn-group--xm rnn-jobOfferList').find_all('li', class_='rnn-jobOfferList__item rnn-jobOfferList__item--adnet rnn-group rnn-group--s js-kininaruItem js-uilTargetCassette')
                for corp in corps:
                    name = corp.find('p', class_='rnn-jobOfferList__item__company__text').get_text()
                    a_tag = corp.find('h2', class_='rnn-textLl js-abScreen__title').find('a')
                    url = domain + a_tag.get('href', 'ERROR')
                    industry = re.sub(r'\s|\t|\n', '', a_tag.get_text())
                    location = re.sub(r'\s|\t|\n', '', corp.find('tr', class_='rnn-tableGrid rnn-offerDetail js-abScreen__place').get_text())
                    talent = corp.find('tr', class_='rnn-tableGrid rnn-offerDetail js-abScreen__prefer')
                    if talent:
                        talent = re.sub(r'\s|\t|\n', '', talent.get_text())
                    else:
                        talent = ''
                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'industry': industry,
                            'location': location,
                            'talent': talent,
                        }
                    else:
                        self.util.data[name]['talent'] += ' ' + talent
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]], v[self.order[3]]] for
                key, v in self.util.data.items()
            ]

    def en_japan(self):
        if self.crawling:
            self.util.access('https://employment.en-japan.com/search/search_list/?occupation=351000_351500_400000')
            self.util.counter = 1
            self.util.save_html()
            for i in range(1, 10000):
                self.util.counter += 1
                try:
                    self.util.execute_script('document.getElementsByClassName("next page next")[0].click()')
                    self.util.save_html()
                except:
                    break
        else:
            url, location, talent = [''] * 3
            domain = 'https://employment.en-japan.com'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find('div', class_='jobSearchListLeftArea').find_all('div', class_='list')
                for corp in corps:
                    name = re.sub(r'\s|\t|\n', '', corp.find('span', class_='company').get_text())
                    url = domain + corp.find('a').get('href', 'ERROR')
                    data_list = corp.find('ul', class_='dataList').find_all('li', class_='data')
                    location = re.sub(r'\s|\t|\n', '', data_list[-1].find('span', class_='text').get_text())
                    try:
                        talent = re.sub(r'\s|\t|\n', '', data_list[1].find('span', class_='text').get_text())\
                            if data_list[1].find('span', class_='icon icon_condition').get_text() == '応募資格' else ''
                    except:
                        talent = ''

                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'location': location,
                            'talent': talent,
                        }
                    else:
                        self.util.data[name]['talent'] += ' ' + talent
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]]] for
                key, v in self.util.data.items()
            ]

    def green(self):
        if self.crawling:
            self.util.access('https://www.green-japan.com/search')
            self.util.element(selector='//input[@data-testid="SearchFormInput"]', _type=By.XPATH, style='input', text='エンジニア')
            self.util.element(selector='//*[@id="__next"]/header/div[3]/div[2]/div[2]/form/div/button', _type=By.XPATH, style='click')
            self.util.counter = 1
            self.util.save_html()
            for i in range(1, 10000):
                self.util.counter += 1
                try:
                    self.util.element(selector='//*[local-name()="svg" and @data-testid="NavigateNextIcon"]', _type=By.XPATH, style='click')
                    self.util.save_html()
                except:
                    break
            self.util.access('https://www.green-japan.com/search')
            self.util.element(selector='//input[@data-testid="SearchFormInput"]', _type=By.XPATH, style='input',
                              text='デザイン')
            self.util.element(selector='//*[@id="__next"]/header/div[3]/div[2]/div[2]/form/div/button', _type=By.XPATH,
                              style='click')
            self.util.save_html()
            for i in range(1, 10000):
                self.util.counter += 1
                try:
                    self.util.element(selector='//*[local-name()="svg" and @data-testid="NavigateNextIcon"]', _type=By.XPATH, style='click')
                    self.util.save_html()
                except:
                    break
        else:
            domain = 'https://www.green-japan.com'
            files = os.listdir(self.util.path)
            if not self.price:
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(self.util.path, filename))
                    corps = soup.find('div', class_='css-1y5htl1').find_all('div', class_='MuiBox-root css-vfzywm')
                    for corp in corps:
                        name, url, location, talent = self.util.green_util(domain, corp)
                        if name not in self.util.data:
                            self.util.data[name] = {
                                'url': url,
                                'location': location,
                                'talent': talent,
                            }
                        else:
                            self.util.data[name]['talent'] += ' ' + talent
                self.util.csv_data = [
                    [key, v[self.order[0]], v[self.order[1]], v[self.order[2]]] for
                    key, v in self.util.data.items()
                ]
            else:
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(self.util.path, filename))
                    corps = soup.find('div', class_='css-1y5htl1').find_all('div', class_='MuiBox-root css-vfzywm')
                    for corp in corps:
                        name, url, location, talent = self.util.green_util(domain, corp)
                        _price = corp.find('div', attrs={'aria-label': '想定年収'})
                        min_price, max_price = [''] * 2
                        if _price:
                            try:
                                price = _price.get_text().split('〜')
                                min_price = int(price[0].replace('万円', '') + '0000')
                                max_price = int(price[1].replace('万円', '') + '0000')
                            except:
                                pass
                        self.util.csv_data += [[name, min_price, max_price, url, location, talent]]


    def indeed(self):
        if self.crawling:
            urls = [
                'https://jp.indeed.com/jobs?q=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2&l=&from=searchOnDesktopSerp&vjk=34b75978abbec08a',
                'https://jp.indeed.com/jobs?q=WEB%E3%83%87%E3%82%B6%E3%82%A4%E3%83%8A%E3%83%BC&l=&from=searchOnDesktopSerp&vjk=c1aad356beaf5edd',
                'https://jp.indeed.com/jobs?q=PL%E3%80%80PM&l=&from=searchOnDesktopSerp&vjk=b308924613445270'
            ]
            for url in urls:
                self.util.access(url)
                self.util.counter = 1
                self.util.save_html()
                for i in range(1, 10000):
                    self.util.counter += 1
                    try:
                        self.util.element(selector='//button[@aria-label="閉じる"]', _type=By.XPATH, style='click')
                    except:
                        pass
                    try:
                        self.util.element(selector='//button[@class="gnav-CookiePrivacyNoticeButton"]', _type=By.XPATH, style='click')
                    except:
                        pass
                    try:
                        self.util.element(selector='//a[@data-testid="pagination-page-next"]', _type=By.XPATH, style='click')
                        self.util.save_html()
                    except:
                        break
        else:
            url, location, talent = [''] * 3
            domain = 'https://jp.indeed.com'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find('div', class_='mosaic mosaic-provider-jobcards mosaic-provider-hydrated').find('ul').find_all('li')
                for corp in corps:
                    name = corp.find('span', attrs={'data-testid': 'company-name'})
                    if not name:
                        continue
                    name = re.sub(r'\s|\t|\n', '', name.get_text())
                    url = domain + corp.find('a').get('href', 'ERROR')
                    try:
                        location = re.sub(r'\s|\t|\n', '', corp.find('div', attrs={'data-testid': 'text-location'}).get_text())
                    except:
                        location = re.sub(r'\s|\t|\n', '', corp.find('div', attrs={'data-testid': 'icon-location'}).get_text())
                    try:
                        talent = re.sub(r'\s|\t|\n', '', corp.find('div', class_='underShelfFooter').get_text())
                    except:
                        talent = ''

                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'location': location,
                            'talent': talent,
                        }
                    else:
                        if talent:
                            self.util.data[name]['talent'] += ' ' + talent
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]]] for
                key, v in self.util.data.items()
            ]

    def levtech_career(self):
        if self.crawling:
            self.util.access('https://career.levtech.jp/company/search/')
            self.util.counter = 1
            self.util.save_html()
            for i in range(1, 10000):
                self.util.counter += 1
                try:
                    self.util.execute_script('document.getElementsByClassName("next")[0].children[0].click()')
                    self.util.save_html()
                except:
                    break
        else:
            url, location, detail = [''] * 3
            domain = 'https://career.levtech.jp'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find_all('li', class_='project__list')
                for corp in corps:
                    h2 = corp.find('h2', class_='projectTtl__txt__ttlCompany')
                    name = re.sub(r'\s|\t|\n', '', h2.get_text())
                    url = domain + h2.find('a').get('href', 'ERROR')
                    _location = corp.find('p', class_='projectTtl__txt__place')
                    location = re.sub(r'\s|\t|\n', '', _location.get_text()) if _location else '-'
                    try:
                        detail = re.sub(r'\s|\t|\n', '', corp.find('td', class_='projectTable__layout__detail').get_text())
                    except:
                        detail = '-'

                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'location': location,
                            'detail': detail,
                        }
                    else:
                        self.util.data[name]['detail'] += ' ' + detail
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]]] for
                key, v in self.util.data.items()
            ]

    def open_work(self):
        if self.crawling:
            self.util.access('https://www.openwork.jp/job_search_result?o=1&z=601.603.607&p=&remoteWork=&k=&kt=&mids=&y=&totalS=&x=&w=&i=&f=&u=std&jt=')
            self.util.counter = 1
            self.util.save_html()
            for i in range(1, 100000):
                self.util.counter += 1
                try:
                    self.util.element(selector='//a[text()="次へ"]', style='click')
                    self.util.save_html()
                except:
                    break
        else:
            url, location, talent = [''] * 3
            domain = 'https://www.openwork.jp'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                try:
                    corps = soup.find('div', id='contents').find_all('article')
                except:
                    continue
                for corp in corps:
                    a_tag = corp.find('div', class_='jobListHeader').find('h4').find('a')
                    name = re.sub(r'\s|\t|\n', '', a_tag.get_text())
                    url = domain + a_tag.get('href', 'ERROR')
                    trs = corp.find('table', class_='table-job').find_all('tr')
                    location = ''
                    for tr in trs:
                        th = re.sub(r'\s|\t|\n', '', tr.find('th').get_text())
                        if th == '勤務地':
                            location = re.sub(r'\s|\t|\n', '', tr.find('td').get_text())
                            break
                    try:
                        talent = re.sub(r'\s|\t|\n', '', corp.find('p', class_='jobListJobDescription').get_text())
                    except:
                        talent = '-'

                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'location': location,
                            'talent': talent,
                        }
                    else:
                        self.util.data[name]['talent'] += ' ' + talent
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]]] for
                key, v in self.util.data.items()
            ]

    def wantedly(self):
        if self.crawling:
            urls = [
                'https://www.wantedly.com/projects?new=true&page=1&occupationTypes=jp__engineering&hiringTypes=newgrad&hiringTypes=mid_career&hiringTypes=freelance&hiringTypes=side_job&order=mixed',
                'https://www.wantedly.com/projects?new=true&page=1&occupationTypes=jp__design_and_art&hiringTypes=newgrad&hiringTypes=mid_career&hiringTypes=freelance&hiringTypes=side_job&order=mixed',
                'https://www.wantedly.com/projects?new=true&page=1&occupationTypes=jp__pm_and_web_direction&hiringTypes=newgrad&hiringTypes=mid_career&hiringTypes=freelance&hiringTypes=side_job&order=mixed',
                'https://www.wantedly.com/projects?new=true&page=1&occupationTypes=jp__consulting&hiringTypes=newgrad&hiringTypes=mid_career&hiringTypes=freelance&hiringTypes=side_job&order=mixed',
            ]
            self.util.counter = 0
            for url in urls:
                self.util.access(url)
                self.util.counter += 1
                self.util.save_html()
                for i in range(1, 100):
                    self.util.counter += 1
                    try:
                        self.util.element(selector='//button[@aria-label="Go to next page"]', style='click')
                        self.util.save_html()
                    except:
                        break
        else:
            url, talent = [''] * 2
            domain = 'https://www.wantedly.com'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find('ul', class_='ProjectListJobPostsLaptop__ProjectList-sc-79m74y-11').find_all('li')
                for corp in corps:
                    name = corp.find('p', id='company-name')
                    if not name:
                        continue
                    name = re.sub(r'\s|\t|\n', '', name.get_text())
                    url = domain + corp.find('a').get('href', 'ERROR')
                    try:
                        talent = re.sub(r'\s|\t|\n', '', corp.find('h2').get_text())
                    except:
                        talent = '-'

                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'talent': talent,
                        }
                    else:
                        self.util.data[name]['talent'] += ' ' + talent
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]]] for
                key, v in self.util.data.items()
            ]

    def willoftech(self):
        if self.crawling:
            self.util.access('https://willof.jp/techcareer/engineer/search?page=1')
            max_page = 500
            try:
                last = self.util.element(selector='//span[@class="volume"]', style='get')
                last = int(last.text.replace(',', ''))
                max_page = last // 10 + 1 if last % 10 else last // 10
            except:
                pass
            self.util.counter = 1
            self.util.save_html()
            for i in range(1, max_page):
                self.util.counter += 1
                try:
                    self.util.element(selector='//ul[contains(@class, "c-list-paging")]/li[last()]/a', style='click')
                    self.util.save_html()
                except:
                    break
        else:
            url, industry, location, talent = [''] * 4
            domain = 'https://www.wantedly.com'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find('ul', class_='c-list-article').find_all('li', class_='inner-list')
                for corp in corps:
                    name = corp.find('div', class_='company-name')
                    if not name:
                        continue
                    name = re.sub(r'\s|\t|\n', '', name.get_text())
                    try:
                        a_tag = corp.find('div', class_='article-name').find('a')
                    except:
                        continue
                    url = a_tag.get('href', 'ERROR')
                    industry = ','.join([re.sub(r'\s|\t|\n', '', c.get_text()) for c in corp.find_all('div', class_='work-info-data')]).replace(',', '|')
                    location = corp.find('div', class_='prefecture-name')
                    location = re.sub(r'\s|\t|\n', '', location.get_text()) if location else ''
                    station = corp.find('div', class_='station-name')
                    if station:
                        location = location + '|' + re.sub(r'\s|\t|\n', '', station.get_text())
                    talent = re.sub(r'\s|\t|\n', '', a_tag.get_text())
                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'industry': industry,
                            'location': location,
                            'talent': talent,
                        }
                    else:
                        self.util.data[name]['talent'] += ' ' + talent
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]], v[self.order[3]]] for
                key, v in self.util.data.items()
            ]

    def tensyoku_ex(self):
        if self.crawling:
            urls = {
                'メーカー系(電気・電子・機械系)': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0200&salary_type=&company_name_search=&keyword=',
                'メーカー系(素材・医薬品他)': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0300&salary_type=&company_name_search=&keyword=',
                '商社系(電気・電子・機械系)': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0400&salary_type=&company_name_search=&keyword=',
                '商社系(総合商社・素材・医薬品他)': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0500&salary_type=&company_name_search=&keyword=',
                '流通・小売系': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0600&salary_type=&company_name_search=&keyword=',
                'サービス系': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0700&salary_type=&company_name_search=&keyword=',
                'コンサルティング・専門サービス系': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0800&salary_type=&company_name_search=&keyword=',
                'メディア・マスコミ系': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=0900&salary_type=&company_name_search=&keyword=',
                '金融・保険系': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=1000&salary_type=&company_name_search=&keyword=',
                '不動産・建設系': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=1100&salary_type=&company_name_search=&keyword=',
                'その他': 'https://tenshoku-ex.jp/search/detail?area=&large_occupation=060000&middle_occupation=&large_industry=1200&salary_type=&company_name_search=&keyword='
            }
            self.util.counter = 1
            for key, url in urls.items():
                self.util.access(url)
                self.util.save_html()
                for i in range(1, 100000):
                    self.util.counter += 1
                    try:
                        self.util.element(selector='//span[@class="next"]/a', _type=By.XPATH, style='click')
                        self.util.save_html()
                    except:
                        print(self.util.counter)
                        break
                pass
        else:
            # 'url', 'location', 'detail', 'requirements'
            domain = 'https://tenshoku-ex.jp'
            files = os.listdir(self.util.path)
            for filename in files:
                print(filename)
                soup = self.util.soup_util(os.path.join(self.util.path, filename))
                corps = soup.find_all('div', class_='box_job box_job_result')
                for corp in corps:
                    name = re.sub(r'\s|\t|\n', '', corp.find('span', class_='box_job_company').get_text())
                    url = domain + corp.find('a').get('href', 'ERROR')
                    table = corp.find('table', class_='table_job_data')
                    tds = table.find_all('td')
                    detail = re.sub(r'\s|\t|\n', '', tds[0].get_text())
                    requirements = re.sub(r'\s|\t|\n', '', tds[1].get_text())
                    location = re.sub(r'\s|\t|\n|＜.+＞', '', tds[3].get_text())
                    if name not in self.util.data:
                        self.util.data[name] = {
                            'url': url,
                            'location': location,
                            'detail': detail,
                            'requirements': requirements,
                        }
                    else:
                        self.util.data[name]['location'] += '｜' + re.sub(r'\s|\t|\n|＜.+＞', '', location)
                        self.util.data[name]['detail'] += ' ' + detail
                        self.util.data[name]['requirements'] += ' ' + requirements
            self.util.csv_data = [
                [key, v[self.order[0]], v[self.order[1]], v[self.order[2]], v[self.order[3]]] for
                key, v in self.util.data.items()]


    def levtech_freelance_analysis(self):

        if self.crawling:
            urls = {
                'JavaScript': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=4',
                'Java': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=3',
                'PHP': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=5',
                'SQL': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=9',
                'C#': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=11',
                'Python': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=7',
                'Ruby': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=8',
                'Swift': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=49',
                'C++': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=1',
                'Go': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=10',
                'C言語': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=6',
                'TypeScript': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=58',
                'Kotlin': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=57',
                'VBA': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=37',
                'COBOL': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=22',
                'Perl': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&skill[]=12',
                'AWS': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&cld[]=1',
                'GCP': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&cld[]=30',
                'Azure': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&cld[]=4',
                'Vue&Nuxt': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=57&fw[]=52',
                'React&Next': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=49&fw[]=58',
                'Spring': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=5&fw[]=50',
                'Struts': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=8',
                'CakePHP': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=3',
                'CodeIgniter': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=13',
                'Laravel': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&fw[]=44',
                'DynamoDB': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=17',
                'MongoDB': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=16',
                'MySQL': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=3',
                'Oracle': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=2',
                'PostgreSQL': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=4',
                'SQLserver': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=6',
                'MS Access': 'https://freelance.levtech.jp/project/search/?show_public_only=1&sala=7&db[]=1',
            }
            for key, url in urls.items():
                self.util.access(url)
                self.util.counter = 1
                self.util.save_html_plus_word_path(key)
                for i in range(1, 10000):
                    self.util.counter += 1
                    try:
                        self.util.element(selector='//a[contains(@class, "operateButton")]', _type=By.XPATH, style='click', multi=True, target_num=1)
                        self.util.save_html_plus_word_path(key)
                    except:
                        break
        else:
            name, price, location, environ, skill, jobs, url = [''] * 7
            self.util.summary_header =['言語', '案件数', '最大', '平均', '開発', 'PL', 'PMO', 'PM']
            domain = 'https://freelance.levtech.jp'
            self.util.keys = [
                'JavaScript', 'Java', 'PHP', 'SQL', 'C#', 'Python',
                'Ruby', 'Swift', 'C++', 'Go', 'C言語', 'TypeScript',
                'Kotlin', 'VBA', 'COBOL', 'Perl',
                'AWS', 'GCP', 'Azure',
                'Vue&Nuxt', 'React&Next', 'Spring', 'Struts',
                'CakePHP', 'CodeIgniter', 'Laravel',
                'DynamoDB', 'MongoDB', 'MySQL', 'Oracle', 'PostgreSQL', 'SQLserver', 'MS Access'
            ]
            for key in self.util.keys:
                path = os.path.join(self.util.path, key)
                files = os.listdir(path)
                self.util.data[key] = {'data': [], 'summary': {'jobs': [], 'programmer': [], 'pl': [], 'pm': [], 'pmo': []}, 'counter': 0}
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(path, filename))
                    corps = soup.find_all('li', class_='projectCard')
                    for corp in corps:
                        self.util.data[key]['counter'] += 1
                        name = re.sub(r'\s|\t|\n', '', corp.find('h3', class_='nameGroup').get_text())
                        price = re.sub(r'\s|\t|\n|円|,', '', corp.find('span', class_='price').get_text())
                        try:
                            price = int(price)
                        except:
                            pass

                        location = re.sub(r'\s|\t|\n', '', corp.find('ul', class_='summaryList').find_all('p', class_='summaryText')[1].get_text())
                        items = corp.find('div', class_='tableGroup')
                        environ, skill, jobs = [''] * 3
                        for dt, dd in zip(items.find_all('dt'), items.find_all('dd')):
                            if dt.get_text() == '開発環境':
                                environ = re.sub(r'\s|\t|\n', '', dd.get_text())
                            elif dt.get_text() == '求めるスキル':
                                skill = re.sub(r'\s|\t|\n', '', dd.get_text())
                            elif dt.get_text() == '募集職種':
                                jobs = re.sub(r'\s|\t|\n', '', dd.get_text())
                        if isinstance(price, int) and price >= 100000:
                            self.util.data[key]['summary']['jobs'] += [price]
                            if re.search(r'PMO|pmo', jobs):
                                self.util.data[key]['summary']['pmo'] += [price]
                            if re.search(r'PM[^O]|pm[^o]', jobs):
                                self.util.data[key]['summary']['pm'] += [price]
                            if re.search(r'PL|pl', jobs):
                                self.util.data[key]['summary']['pl'] += [price]
                            else:
                                self.util.data[key]['summary']['programmer'] += [price]

                        url = domain + corp.find('a', class_='linkButton -primary').get('href', 'ERROR')

                        self.util.data[key]['data'] += [[name, price, location, environ, skill, jobs, url]]

            self.util.data['summary'] = [
                [
                    key,
                    self.util.data[key]['counter'],
                    max(self.util.data[key]['summary']['jobs']),
                    round(mean(self.util.data[key]['summary']['jobs']), 0),
                    round(mean(self.util.data[key]['summary']['programmer']), 0) if self.util.data[key]['summary']['programmer'] else '-',
                    round(mean(self.util.data[key]['summary']['pl']), 0) if self.util.data[key]['summary']['pl'] else '-',
                    round(mean(self.util.data[key]['summary']['pmo']), 0) if self.util.data[key]['summary']['pmo'] else '-',
                    round(mean(self.util.data[key]['summary']['pm']), 0) if self.util.data[key]['summary']['pm'] else '-',
                ] for key in self.util.keys
            ]

    def pe_bank_analysis(self):

        if self.crawling:
            urls = {
                'Java': 'https://pe-bank.jp/project/java/',
                'PHP': 'https://pe-bank.jp/project/php/',
                'Ruby': 'https://pe-bank.jp/project/ruby/',
                'Python': 'https://pe-bank.jp/project/python/',
                'JavaScript': 'https://pe-bank.jp/project/javascript/',
                'Angular.js・Node.js': 'https://pe-bank.jp/project/angular_node/',
                'Typescript・Vue.js': 'https://pe-bank.jp/project/typescript_vue/',
                'React': 'https://pe-bank.jp/project/react/',
                'iOS': 'https://pe-bank.jp/project/ios/',
                'Objective-C': 'https://pe-bank.jp/project/objectivec/',
                'Swift': 'https://pe-bank.jp/project/swift/',
                'Android': 'https://pe-bank.jp/project/android/',
                'Kotlin': 'https://pe-bank.jp/project/kotlin/',
                'インフラ(サーバー)': 'https://pe-bank.jp/project/server/',
                'インフラ(ネットワーク)': 'https://pe-bank.jp/project/network/',
                'パブリッククラウド': 'https://pe-bank.jp/project/cloud/',
                'AWS': 'https://pe-bank.jp/project/aws/',
                'Azure': 'https://pe-bank.jp/project/azure/',
                'GCP': 'https://pe-bank.jp/project/gcp/',
                'PM': 'https://pe-bank.jp/project/pm/',
                'PMO': 'https://pe-bank.jp/project/pmo/',
                'コンサルティング': 'https://pe-bank.jp/project/consul/',
                'Webディレクター': 'https://pe-bank.jp/project/director/',
                'ITアーキテクト': 'https://pe-bank.jp/project/architect/',
                'DX': 'https://pe-bank.jp/project/dx/',
                'データベース': 'https://pe-bank.jp/project/db/',
                'SQL': 'https://pe-bank.jp/project/sql/',
                'HTML5': 'https://pe-bank.jp/project/html5/',
                'テスト・検証': 'https://pe-bank.jp/project/verification/',
                'AI・機械学習': 'https://pe-bank.jp/project/ai/',
                'Shell(C・B・K)': 'https://pe-bank.jp/project/shell/',
                'Unity・Unreal Engine': 'https://pe-bank.jp/project/unity/',
                'ゲーム': 'https://pe-bank.jp/project/game/',
                'ERP': 'https://pe-bank.jp/project/erp/',
                'IoT': 'https://pe-bank.jp/project/iot/',
                'アセンブラ': 'https://pe-bank.jp/project/assembler/',
                'RPA': 'https://pe-bank.jp/project/rpa/',
                'Scala': 'https://pe-bank.jp/project/scala/',
                'Go': 'https://pe-bank.jp/project/golang/',
                'COBOL': 'https://pe-bank.jp/project/cobol/',
                '.NET(VB・C#)': 'https://pe-bank.jp/project/dotnet/',
                'C言語': 'https://pe-bank.jp/project/clang/',
                'C++': 'https://pe-bank.jp/project/cplus/',
                'VC++': 'https://pe-bank.jp/project/vcplus/',
                'Perl': 'https://pe-bank.jp/project/perl/',
                'VB・VBA': 'https://pe-bank.jp/project/vb_vba/',
                'Chef': 'https://pe-bank.jp/project/chef/',
                'Puppet': 'https://pe-bank.jp/project/puppet/',
                'Ansible': 'https://pe-bank.jp/project/ansible/',
                'SAP・Salesforce': 'https://pe-bank.jp/project/sap_sf/',
                'その他言語': 'https://pe-bank.jp/project/other/',
                'インフラ(その他)': 'https://pe-bank.jp/project/infra/'
            }
            for key, url in urls.items():
                self.util.access(url)
                self.util.counter = 1
                self.util.save_html_plus_word_path(key)
                for i in range(1, 10000):
                    self.util.counter += 1
                    try:
                        element = self.util.element(selector='//li[@class="next"]/a', _type=By.XPATH, style='get')
                        if element.get_attribute('href'):
                            element.click()
                            sleep(3)
                        else:
                            break
                        self.util.save_html_plus_word_path(key)
                    except:
                        break
        else:
            name, min_price, max_price, location, skill, jobs, url = [''] * 7
            self.util.summary_header = ['言語', '案件数', '最大', '最大平均', '開発', 'PMO', 'PM']
            domain = 'https://pe-bank.jp'
            self.util.keys = [
                'Java', 'PHP', 'Ruby', 'Python',
                'JavaScript', 'Angular.js・Node.js', 'Typescript・Vue.js', 'React',
                'iOS', 'Objective-C', 'Swift', 'Android', 'Kotlin',
                'インフラ(サーバー)', 'インフラ(ネットワーク)', 'パブリッククラウド', 'AWS', 'Azure', 'GCP',
                'PM', 'PMO', 'コンサルティング', 'Webディレクター', 'ITアーキテクト', 'DX',
                'データベース', 'SQL', 'HTML5', 'テスト・検証', 'AI・機械学習', 'Shell(C・B・K)',
                'Unity・Unreal Engine', 'ゲーム', 'ERP', 'IoT', 'アセンブラ',
                'RPA', 'Scala', 'Go', 'COBOL', '.NET(VB・C#)', 'C言語', 'C++', 'VC++', 'Perl',
                'VB・VBA', 'Chef', 'Puppet', 'Ansible', 'SAP・Salesforce', 'その他言語', 'インフラ(その他)'
            ]
            for key in self.util.keys:
                path = os.path.join(self.util.path, key)
                files = os.listdir(path)
                self.util.data[key] = {'data': [],
                                       'summary': {'jobs': [], 'programmer': [], 'pm': [], 'pmo': []},
                                       'counter': 0}
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(path, filename))
                    corps = soup.find('ul', class_='projectList').find_all('div', class_='box')
                    for corp in corps:
                        self.util.data[key]['counter'] += 1
                        dl = corp.find('dl', class_='projectListCts')
                        a_tag = dl.find('dt').find('a')
                        name =re.sub(r'\s|\t|\n', '', a_tag.get_text())
                        url = a_tag.get('href', '')
                        min_price, max_price, location, skill, jobs = [''] * 5
                        for dd in dl.find_all('dd'):
                            text = re.sub(r'\s|\t|\n', '', dd.get_text())
                            if '単価：' in text:
                                _price = re.sub(r'単価：|万円', '', text).split('～')
                                min_price = int(_price[0] + '0000')
                                max_price = int(_price[1] + '0000')
                            elif '勤務地：' in text:
                                location = re.sub(r'勤務地：', '', text)
                            elif '内容：' in text:
                                jobs = re.sub(r'内容：', '', text)
                            elif 'スキル：' in text:
                                skill = re.sub(r'スキル：', '', text)
                        if isinstance(min_price, int) and min_price >= 100000:
                            self.util.data[key]['summary']['jobs'] += [round(mean([min_price, max_price]), 0)]
                            if re.search(r'PMO|pmo', skill):
                                self.util.data[key]['summary']['pmo'] += [round(mean([min_price, max_price]), 0)]
                            if re.search(r'PM$|PM,|PM[^O]|pm[^o]', skill):
                                self.util.data[key]['summary']['pm'] += [round(mean([min_price, max_price]), 0)]
                            else:
                                self.util.data[key]['summary']['programmer'] += [round(mean([min_price, max_price]), 0)]

                        self.util.data[key]['data'] += [[name, min_price, max_price, location, skill, jobs, url]]

            self.util.data['summary'] = [
                [
                    key,
                    self.util.data[key]['counter'],
                    max(self.util.data[key]['summary']['jobs']),
                    round(mean(self.util.data[key]['summary']['jobs']), 0),
                    round(mean(self.util.data[key]['summary']['programmer']), 0) if self.util.data[key]['summary'][
                        'programmer'] else '-',
                    round(mean(self.util.data[key]['summary']['pmo']), 0) if self.util.data[key]['summary'][
                        'pmo'] else '-',
                    round(mean(self.util.data[key]['summary']['pm']), 0) if self.util.data[key]['summary'][
                        'pm'] else '-',
                ] for key in self.util.keys
            ]

    def geechs_analysis(self):

        if self.crawling:
            urls = {
                'ios': 'https://geechs-job.com/project/ios',
                'android': 'https://geechs-job.com/project/android',
                'Go': 'https://geechs-job.com/project/go',
                'Java': 'https://geechs-job.com/project/java',
                'Python': 'https://geechs-job.com/project/python',
                'Scala': 'https://geechs-job.com/project/scala',
                'PHP': 'https://geechs-job.com/project/php',
                'Ruby': 'https://geechs-job.com/project/ruby',
                'Perl': 'https://geechs-job.com/project/perl',
                'Unity': 'https://geechs-job.com/project/unity',
                'Cocos2d-x': 'https://geechs-job.com/project/cocos2d-x',
                'C#.NET': 'https://geechs-job.com/project/csharp-dotnet',
                'VB.NET': 'https://geechs-job.com/project/vb-dotnet',
                'VB・VBA': 'https://geechs-job.com/project/vb-vba',
                'C・C++': 'https://geechs-job.com/project/c-cpp',
                'HTML・CSS': 'https://geechs-job.com/project/html5-css3',
                'JavaScript': 'https://geechs-job.com/project/javascript',
                'Photoshop・Illustrator': 'https://geechs-job.com/project/photoshop-illustrator',
                'SQL': 'https://geechs-job.com/project/sql',
                'DB(インフラ)': 'https://geechs-job.com/project/db',
                'NW(インフラ)': 'https://geechs-job.com/project/nw',
                'サーバ(インフラ)': 'https://geechs-job.com/project/server',
                'AWS': 'https://geechs-job.com/project/aws',
                'TypeScript': 'https://geechs-job.com/project/typescript',
                'Flutter': 'https://geechs-job.com/project/flutter',
                'Node.js': 'https://geechs-job.com/project/nodejs',
                'ReactNative': 'https://geechs-job.com/project/reactnative',
                'Salesforce': 'https://geechs-job.com/project/salesforce',
                'UnrealEngine': 'https://geechs-job.com/project/unrealengine',
                'ディレクター': 'https://geechs-job.com/project/roles/director',
                'PM・PMO': 'https://geechs-job.com/project/roles/pm',
                'PL': 'https://geechs-job.com/project/roles/pl',
                'SE': 'https://geechs-job.com/project/roles/se',
                'PG': 'https://geechs-job.com/project/roles/pg',
                'テスター': 'https://geechs-job.com/project/roles/tester',
                '保守・運用': 'https://geechs-job.com/project/roles/maintenance',
                'プランナー': 'https://geechs-job.com/project/roles/planner',
                'UI・UX': 'https://geechs-job.com/project/roles/ui-ux',
            }
            for key, url in urls.items():
                self.util.access(url)
                self.util.counter = 1
                self.util.save_html_plus_word_path(key)
                for i in range(1, 10000):
                    self.util.counter += 1
                    try:
                        self.util.element(selector='//i[@class="p-paginationNav_icon fas fa-angle-right"]/..', _type=By.XPATH, style='click')
                        sleep(2)
                        self.util.save_html_plus_word_path(key)
                    except:
                        break
        else:
            name, min_price, max_price, location, skill, jobs, url = [''] * 7
            self.util.summary_header = ['言語', '案件数', '最大', '最大平均', '開発', 'PL', 'PMO/PM']
            domain = 'https://geechs-job.com'
            self.util.keys = [
                'Java', 'PHP', 'Python', 'JavaScript', 'TypeScript', 'ReactNative', 'Node.js', 'Flutter',
                'Go', 'Ruby', 'Scala', 'Perl', 'Cocos2d-x', 'C#.NET', 'VB.NET', 'VB・VBA', 'C・C++',
                'SQL', 'DB(インフラ)', 'NW(インフラ)', 'サーバ(インフラ)',
                'AWS', 'Salesforce', 'ios', 'android', 'Unity', 'UnrealEngine',
                'PG', 'SE', 'PL', 'PM・PMO', 'ディレクター', 'テスター', '保守・運用',
                'プランナー', 'HTML・CSS', 'Photoshop・Illustrator', 'UI・UX'
            ]
            for key in self.util.keys:
                path = os.path.join(self.util.path, key)
                files = os.listdir(path)
                self.util.data[key] = {'data': [],
                                       'summary': {'jobs': [], 'programmer': [], 'pl': [], 'pm_pmo': []},
                                       'counter': 0}
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(path, filename))
                    corps = soup.find('ul', class_='p-article-project').find_all('li', class_='c-card p-card-project p-card-project-new')
                    for corp in corps:
                        self.util.data[key]['counter'] += 1
                        a_tag = corp.find('a', class_='c-card_title_link')
                        name = re.sub(r'\s|\t|\n', '', a_tag.get_text())
                        url = a_tag.get('href', 'ERROR')
                        infos = corp.find('ul', class_='c-card-info01').find_all('li')
                        for info in infos:
                            text = re.sub(r'\s|\t|\n', '', info.get_text())
                            if '単価' in text:
                                _price = re.sub(r'単価.+\)|万円.+|\s|\t|\n', '', text).split('〜')
                                min_price = int(_price[0] + '0000')
                                max_price = int(_price[1] + '0000')
                            elif 'fa-map-marker-alt' in info.find('i').get('class',''):
                                location = re.sub(r'\s|\t|\n', '', info.get_text())

                        skill, jobs = [''] * 2
                        dls = corp.find_all('dl', class_='project-detail-table')
                        for dl in dls:
                            dt = dl.find('dt')
                            dd = dl.find('dd')
                            if '募集スキル' in dt.get_text():
                                for c in dd.find_all('li', class_='c-category_tab'):
                                    if not skill:
                                        skill = re.sub(r'\s|\t|\n', '', c.get_text())
                                    else:
                                        skill += '|' + re.sub(r'\s|\t|\n', '', c.get_text())
                            elif 'ポジション' in dt.get_text():
                                for c in dd.find_all('li', class_='c-category_tab'):
                                    if not jobs:
                                        jobs = re.sub(r'\s|\t|\n', '', c.get_text())
                                    else:
                                        jobs += '|' + re.sub(r'\s|\t|\n', '', c.get_text())
                        if isinstance(min_price, int) and min_price >= 100000:
                            self.util.data[key]['summary']['jobs'] += [round(mean([min_price, max_price]), 0)]
                            if 'PL' in jobs:
                                self.util.data[key]['summary']['pl'] += [round(mean([min_price, max_price]), 0)]
                            elif 'PM' in jobs:
                                self.util.data[key]['summary']['pm_pmo'] += [round(mean([min_price, max_price]), 0)]
                            else:
                                self.util.data[key]['summary']['programmer'] += [round(mean([min_price, max_price]), 0)]

                        self.util.data[key]['data'] += [
                            [name, min_price, max_price, location, skill, jobs, url]
                        ]

            self.util.data['summary'] = [
                [
                    key,
                    self.util.data[key]['counter'],
                    max(self.util.data[key]['summary']['jobs']),
                    round(mean(self.util.data[key]['summary']['jobs']), 0),
                    round(mean(self.util.data[key]['summary']['programmer']), 0) if
                    self.util.data[key]['summary'][
                        'programmer'] else '-',
                    round(mean(self.util.data[key]['summary']['pl']), 0) if self.util.data[key]['summary'][
                        'pl'] else '-',
                    round(mean(self.util.data[key]['summary']['pm_pmo']), 0) if self.util.data[key]['summary'][
                        'pm_pmo'] else '-',
                ] for key in self.util.keys
            ]

    def it_pro_partner_analysis(self):

        if self.crawling:
            urls = {
                'Java': 'https://itpropartners.com/job/engineer/java',
                'JavaScript': 'https://itpropartners.com/job/engineer/javascript',
                'PHP': 'https://itpropartners.com/job/engineer/php',
                'Python': 'https://itpropartners.com/job/engineer/python',
                'Ruby': 'https://itpropartners.com/job/engineer/ruby',
                'Swift': 'https://itpropartners.com/job/engineer/swift',
                'Kotlin': 'https://itpropartners.com/job/engineer/kotlin',
                'C言語': 'https://itpropartners.com/job/engineer/c_lang',
                'AWS': 'https://itpropartners.com/job/engineer/aws',
                'TypeScript': 'https://itpropartners.com/job/engineer/typescript',
                'React.js': 'https://itpropartners.com/job/engineer/reactjs',
                'Vue.js': 'https://itpropartners.com/job/engineer/vuejs',
                'Go': 'https://itpropartners.com/job/engineer/go',
                'フロントエンド': 'https://itpropartners.com/job/engineer/frontend-engineer',
                'バックエンド': 'https://itpropartners.com/job/engineer/backend-engineer',
                'インフラ': 'https://itpropartners.com/job/engineer/infrastructure-engineer',
                '機械学習': 'https://itpropartners.com/job/engineer/machine-learning-engineer',
                'iOS': 'https://itpropartners.com/job/engineer/ios-engineer',
                'Android': 'https://itpropartners.com/job/engineer/android-engineer',
                'データサイエンティスト': 'https://itpropartners.com/job/engineer/data-scientist',
                'PM': 'https://itpropartners.com/job/engineer/project-manager',
                'PdM': 'https://itpropartners.com/job/engineer/product-manager',
                'SRE': 'https://itpropartners.com/job/engineer/sre',
                'マーケター': 'https://itpropartners.com/job/marketer',
                'デザイナー': 'https://itpropartners.com/job/designer',
            }
            for key, url in urls.items():
                self.util.access(url)
                self.util.counter = 1
                self.util.save_html_plus_word_path(key)
                for i in range(1, 10000):
                    self.util.counter += 1
                    try:
                        self.util.element(selector='//a[text()="next"]', _type=By.XPATH, style='click')
                        self.util.save_html_plus_word_path(key)
                    except:
                        break
        else:
            name, price, env, jobs, skill, url = [''] * 6
            self.util.summary_header = ['言語', '案件数', '最大', '平均', '開発', 'PM']
            domain = 'https://itpropartners.com'
            self.util.keys = [
                'Java', 'JavaScript', 'PHP', 'Python', 'Ruby',
                'TypeScript', 'React.js', 'Vue.js', 'Go', 'Swift', 'Kotlin', 'C言語', 'AWS',
                'フロントエンド', 'バックエンド', 'インフラ',
                '機械学習', 'iOS', 'Android', 'データサイエンティスト',
                'PM', 'PdM', 'SRE', 'マーケター', 'デザイナー',
            ]
            for key in self.util.keys:
                path = os.path.join(self.util.path, key)
                files = os.listdir(path)
                self.util.data[key] = {'data': [],
                                       'summary': {'jobs': [], 'programmer': [], 'pm': []},
                                       'counter': 0}
                for filename in files:
                    print(filename)
                    soup = self.util.soup_util(os.path.join(path, filename))
                    corps = soup.find_all('div', class_='c-job-card pc-show')
                    for corp in corps:
                        self.util.data[key]['counter'] += 1
                        a_tag = corp.find('a')
                        name = re.sub(r'\s|\t|\n|', '', a_tag.find('h3', class_='c-job-card__title').get_text())
                        url = a_tag.get('href', '')
                        price = int(re.sub(r'\s|\t|\n|,', '', corp.find('div', class_='c-job-price').find('span').get_text()))
                        flag = '5日' in corp.find('div', class_='c-job-price').get_text()
                        env, jobs, skill = [''] * 3
                        trs = corp.find('tbody').find_all('tr')
                        for tr in trs:
                            text = re.sub(r'\s|\t|\n|', '', tr.get_text())
                            if '開発環境' in text:
                                env = re.sub(r'\s|\t|\n|開発環境', '', text).replace(',', '|')
                            elif '求めるスキル' in text:
                                skill = re.sub(r'\s|\t|\n|求めるスキル|もっと見る', '', text)
                            elif '募集職種' in text:
                                jobs = re.sub(r'\s|\t|\n|募集職種', '', text).replace(',', '|')
                        if flag and isinstance(price, int) and price >= 100000:
                            self.util.data[key]['summary']['jobs'] += [price]
                            if 'PM' in jobs:
                                self.util.data[key]['summary']['pm'] += [price]
                            else:
                                self.util.data[key]['summary']['programmer'] += [price]

                        self.util.data[key]['data'] += [
                            [name, price, env, jobs, skill, url]
                        ]
            self.util.data['summary'] = [
                [
                    key,
                    self.util.data[key]['counter'],
                    max(self.util.data[key]['summary']['jobs']),
                    round(mean(self.util.data[key]['summary']['jobs']), 0),
                    round(mean(self.util.data[key]['summary']['programmer']), 0) if
                    self.util.data[key]['summary'][
                        'programmer'] else '-',
                    round(mean(self.util.data[key]['summary']['pm']), 0) if self.util.data[key]['summary'][
                        'pm'] else '-',
                ] for key in self.util.keys
            ]

    def weekly_download(self):
        if self.crawling:
            self.util.weekly_login()
            now = datetime.now()
            year = now.year
            month = '{:02d}'.format(now.month)
            year_month = f'{year}-{month}'
            week = 1
            from_year_month = '2024-04'
            to_year_month = '2024-09'
            noms = self.util.config['weekly_target']
            for nom in noms:
                self.util.counter += 1
                url = f'https://eba-report.xyz/weekly_report?member_no={nom}&weekly_report_year_month={year_month}&weekly_report_week_num={week}&edit=&team_flg='
                try:
                    self.util.access(url)
                    self.util.element(selector='//label[@for="terms_output"]', _type=By.XPATH, style='click', non_sleep=True)
                    self.util.execute_script(f'document.getElementsByName("csv_ym_from")[0].value = "{from_year_month}"')
                    self.util.execute_script(f'document.getElementsByName("csv_ym_to")[0].value = "{to_year_month}"')
                    element = self.util.element(selector='//select[@name="csv_week_to"]', _type=By.XPATH, style='get')
                    select = Select(element)
                    select.select_by_value('6')
                    self.util.element(selector='//input[@name="weekly_report_download"]', _type=By.XPATH, style='click', non_sleep=True)

                except:
                    print(url)
                    continue
        else:
            for i in range(1, 100):
                path = os.path.join(self.util.path, f'{i}.html')
                if not os.path.exists(path):
                    break
                soup = self.util.soup_util(path)
                name = re.sub(r'提出統計：|\s|\n', '', soup.find('section', class_='content-header').find('h1').get_text())
                target = soup.find('ul', class_='nav nav-pills nav-stacked')
                self.util.csv_data += [[name]]
                self.util.csv_data += [[text] for text in re.sub(r'(\n)(\d)(\n)', r'\2\3', target.get_text().replace('\n', '', 1).replace('\n\n', '\n')).split('\n')]

    def weekly_check_submission(self):
        if self.crawling:
            self.util.weekly_login()

            start_year = 2024
            end_year = 2024
            start_month = 4
            end_month = 9
            noms = self.util.config['weekly_target']
            for nom in noms:
                self.util.counter += 1
                url = f'https://eba-report.xyz/total_submission?start_year={start_year}&start_month={start_month}&start_week=1&end_year={end_year}&end_month={end_month}&end_week=6&member_no={nom}&search=%E6%A4%9C%E7%B4%A2'
                try:
                    self.util.access(url)
                    self.util.save_html()
                except:
                    print(url)
                    continue
        else:
            for i in range(1, 100):
                path = os.path.join(self.util.path, f'{i}.html')
                if not os.path.exists(path):
                    break
                soup = self.util.soup_util(path)
                name = re.sub(r'提出統計：|\s|\n', '', soup.find('section', class_='content-header').find('h1').get_text())
                target = soup.find('ul', class_='nav nav-pills nav-stacked')
                self.util.csv_data += [[name]]
                self.util.csv_data += [[text] for text in re.sub(r'(\n)(\d)(\n)', r'\2\3', target.get_text().replace('\n', '', 1).replace('\n\n', '\n')).split('\n')]

    def weekly_check(self):
        if self.crawling:
            self.util.weekly_login()

            for i in [
                # 幹部
                20, 75, 126, 81, 99, 66, 84, 207, 335, 244, 278, 262, 374, 261, 220,
                # リーダー
                107, 115, 118, 268, 85, 103, 165, 209, 242, 311, 356, 366, 480,
                228, 184, 282, 290, 406, 500, 450, 454, 351, 410, 481, 534, 479,
                # この上の行に昇格したリーダーを追加していく運用
                # 亀谷担当が下記になる
                91, 43, 61, 65, 90, 123, 127, 130, 140, 173, 187, 189,
                218, 236, 249, 251, 253, 260,
                264, 285, 319, 409, 499, 113,
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
                if len(_bodys) <= 1:
                    continue
                name = re.sub(r'（自分）|\s|\t|\n', '', _bodys[0].find('td').get_text())
                data = []
                rows = []
                print(path)
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
                self.util.csv_data += [result]
