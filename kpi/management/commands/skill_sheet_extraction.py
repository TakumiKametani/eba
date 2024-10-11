import csv
import os
import re
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from .utils.extraction_util import SkillSheetExtractionUtil, do_write_csv


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
        util = SkillSheetExtractionUtil()
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
                print(path)
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
                if isinstance(key, datetime) or re.search(r'～|保守|運用|≪社内|実績', key) or key in self.exclution():
                    continue
                key = re.sub(r'\s|\t|\u3000|（.+）|\(.+\)|\(.+）|（.+\)|※.+|独学|経験', '', key)
                key = self.key_change(key)
                # if 'Photoshop、Illustrator、XD' == key or 'React.js/Next.js' == key:
                #     for _key in key.split('、'):
                #         if _key not in util.header:
                #             util.header += [_key]
                #         util.results[name][_key] = ''
                # else:
                #     if key not in util.header:
                #         util.header += [key]
                #     util.results[name][key] = ''
                for value in data[1]:
                    if pd.isna(value):
                        continue
                    if re.match(r'.年.+月$|.+月|.年$', value):
                        if re.match(r'.年$', value):
                            value = value.replace('年', '年0ヶ月')
                        if key in ['C、C#、C++', 'C、C++', 'Photoshop、Illustrator、XD', 'React.js/Next.js', 'Vue.js/React', 'React/Redux', 'C/C++', 'サーバ設計/構築', '基本設計/詳細設計', 'PL/PMO', '要件定義・設計書作成']:
                            if '、' in key:
                                _split = key.split('、')
                            elif '/' in key:
                                _split = key.split('/')
                            elif '・' in key:
                                _split = key.split('・')

                            for _key in _split:
                                if 'React.js' == _key:
                                    _key = 'React'
                                elif 'C' == _key:
                                    _key = 'C言語'
                                elif '構築' == _key:
                                    _key = 'サーバ構築'
                                elif '設計書作成' == _key:
                                    _key = '基本設計書'



                                util.results[name][_key] = re.sub(r'カ|ヵ|か', 'ヶ', re.sub(r'\s|\t', '', value))
                        else:
                            util.results[name][key] = re.sub(r'カ|ヵ|か', 'ヶ', re.sub(r'\s|\t', '', value))
                        break

        for name, skills in util.results.items():
            data = [re.sub(r'K|JAVA|JS|PHP|N|F|inf|さん|Ｃ#|WEB|インフラ|Python|lutter', '', name)]
            for target in util.header[1::]:
                if target == '':
                    continue
                data += [skills.get(target, '')]
            util.csv_data += [data]
        _now = datetime.strftime(datetime.now().date(), '%Y%m%d')
        path = os.path.join(settings.SKILL_SHEET, 'output', f'result_{_now}.csv')
        do_write_csv(path, util.header, util.csv_data)

    def key_change(self, key):
        if key == 'C':
            key = 'C言語'
        elif 'Spring' in key:
            key = 'Spring'
        elif key == 'Javascript' or key == 'JS':
            key = 'JavaScript'
        elif 'css' in key.lower():
            key = 'CSS'
        elif 'css' in key.lower():
            key = 'CSS'
        elif 'Angular.js' == key:
            key = 'AngularJS'
        elif 'Vuejs' == key:
            key = 'Vue.js'
        elif 'Vuex4' == key:
            key = 'Vuex'
        elif 'R' == key:
            key = 'R言語'
        elif 'Typescript' == key:
            key = 'TypeScript'
        elif 'illustrator' == key:
            key = 'Illustrator'
        elif 'PL等のリーダー' == key:
            key = 'PL'
        elif 'ベンダー調整/管理' == key:
            key = 'ベンダーコントロール'
        elif '要件定義書作成' == key:
            key = '要件定義'
        elif '設計書作成' == key:
            key = '詳細設計書'
        elif 'jsp' == key:
            key = 'JSP'
        elif 'Junit' == key:
            key = 'JUnit'
        elif 'Wordpress' == key:
            key = 'WordPress'
        elif '要求分析・要件定義' == key:
            key = '要件定義'
        elif 'Slimv3' == key:
            key = 'Slim'
        elif 'Kotolin' == key:
            key = 'Kotlin'
        elif '設計' == key:
            key = 'サーバ設計'
        elif '構築' == key:
            key = 'サーバ構築'

        elif key in ['C♯', 'C＃', 'C#9.0']:
            key = 'C#'
        elif key in ['React.js', 'ReactJS']:
            key = 'React'
        elif key in ['ASP', 'ASP.net.1', 'ASP.NETCoreMVC', 'ASP.net']:
            key = 'ASP.NET'
        elif key in ['Go.1', 'GoLang', 'golang.1', 'Go', 'GO', 'golang', ]:
            key = 'Go言語'
        elif key in ['illustrator.1', 'Ilustrator']:
            key = 'Illustrator'
        elif key in ['Jquery.1', 'JQuery.2', 'jquery', 'Jquery', 'jQueryUI', 'JQuery']:
            key = 'jQuery'
        elif key in ['PremierePro', 'PremierPro', 'PremirePro']:
            key = 'Premiere Pro'
        elif key in ['Python3']:
            key = 'Python'
        elif key in ['RubyonRails', 'RubyOnRails.1']:
            key = 'Ruby on Rails'
        elif key in ['UI提案', 'UIデザイン']:
            key = 'UI/UX'
        elif key in ['shell', 'shellscript', 'Shellscript', 'sh', 'Shell', 'ShellScript', 'シェル', 'シェルスクリプト', 'shellScript']:
            key = 'Shell script'
        elif key in ['Oracle', 'Oracle8i', 'OracleSQL', 'OracleDatabase', 'ORACLE', 'Oracle10g', 'OracleDatabaseSQL', 'Oracle11.c']:
            key = 'OracleDB'
        elif key in ['AmazonEC2', 'Cloud9', 'AmazonDynamoDB', 'AWSCLI', 'EC2', 'VPC・セキュリティグループ', 'RDS', 'AWSCloudWatch', 'AWSSessionManager']:
            key = 'AWS'
        elif key in ['ZendFramework2', 'ZendFramework', 'ZendFrameWork']:
            key = 'Zend'
        elif key in ['WindowsServer2012', 'WindowsServer2016', 'WindowsServer2019', 'Windowsサーバー', 'WindowsServer2012R2', 'WindowsServerR22008', 'WindowsServer2010', 'WindowsServer2022', 'WindowsServer2008']:
            key = 'WindowsServer'
        elif key in ['RHEL8', 'RHEL9', 'RedHatEnterpriseLinux', 'RedHat', 'RHEL7,8', 'RHEL7', 'RHEL6/CentOS6', 'RHEL5.5', 'RHEL6.8', 'RHEL7.6', 'RHEL5', 'RHEL6']:
            key = 'RHEL'
        elif key in ['CentOS7', 'CentOS6']:
            key = 'CentOS'
        elif key in ['DockerCompose']:
            key = 'Docker'
        elif key in ['VB.net', 'VB', 'VB.Net']:
            key = 'VB.NET'
        elif key in ['MicrosoftSQLServer', 'SQL', 'MicrosoftSQL', 'SQLserver', 'SQL/Server', 'MSSQLServer']:
            key = 'SQLServer'
        elif key in ['プロジェクトマネジメント', 'マネジメント対応(サブリーダー以上']:
            key = 'マネジメント'
        elif key in ['.NET_x000D_', '.NETFramework4.8', '.NET']:
            key = '.NETFramework'
        elif key in ['Googleanalytics', 'GoogleAnalytics', 'GoogleAppScript', 'Spanner', 'GCPSpanner']:
            key = 'GCP'
        elif key in ['PosgreSQL', 'Postg', 'PGSQL']:
            key = 'PostgreSQL'
        elif key in ['Mysql', 'MySQL8.0']:
            key = 'MySQL'
        elif key in ['VBAマクロ', 'ExcelVBA', 'MSVBA', 'VBA/VBS']:
            key = 'VBA'
        elif key in ['Struts2']:
            key = 'Struts'
        elif key in ['・ubuntu']:
            key = 'Ubuntu'
        elif key in [
            'CiscoCatalyst9200/9300/9400', 'CiscoCRS-1', 'Cisco製ルーター、スイッチ', 'CiscoCatalyst1000,9000,3850,2900',
            'CiscoISR1000,4000', 'CiscoCatalyst1000', 'CiscoFirepower1000', 'CiscoCatalystLayer2switch',
            'CiscoCatalystLayer3switch', 'CiscoCatalyst', 'CiscoCatalyst2960,3650,3850,4500', 'CiscoCatalyst2960,3650,891,CSR1000v']:
            key = 'Cisco'
        elif key in ['JAVA']:
            key = 'Java'
        elif key in ['NetCOBOL']:
            key = 'COBOL'
        elif key in ['Symphony', 'symfony']:
            key = 'Symfony'
        elif key in ['RubyOnRails']:
            key = 'Ruby on Rails'
        elif key in ['dynamoDB']:
            key = 'DynamoDB'
        elif key in ['Nuxtjs']:
            key = 'Nuxt.js'
        elif key in ['graphQL']:
            key = 'GraphQL'
        elif key in ['ActiveDirectory']:
            key = 'AzureAD'
        elif key in ['AzureVDI']:
            key = 'Azure'
        elif key in ['Express.js']:
            key = 'Express'
        elif key in ['zabbix', 'Zabbixサーバ']:
            key = 'Zabbix'
        elif key in ['node.js']:
            key = 'Node.js'
        elif key in ['Windowsバッチ/PowerShell', 'Powershell']:
            key = 'PowerShell'
        elif key in ['・Unix', 'Unix']:
            key = 'UNIX'
        elif key in ['Falcon']:
            key = 'Phalcon'
        elif key in ['VMwarevSphere', 'VMware']:
            key = 'VMWare'
        elif key in ['ディレクション業務実績', 'ディレクション・進行管理', 'WEBディレクション']:
            key = 'ディレクション'
        elif key in ['']:
            key = ''
        elif key in ['']:
            key = ''

        elif 'CakePHP' in key:
            key = 'CakePHP'
        elif 'HTML' in key:
            key = 'HTML'
        elif 'Java' in key:
            key = 'Java'

        return key

    def exclution(self):
        return [
            '対応工程', '言語・フレームワーク', 'OS・NW機器・サーバー等',
            '言語・フレームワーク・DB・サーバー', '資格', '対応可能工程',
            '習得資格', 'OS・NW機器・サーバー・ツール等', '【NW機器】',
            '【ツール】', 'その他', 'VueRouter', 'VueTestUtils',
            '調査', '構築', '独自CMS', 'Devtools', '技能履歴', 'フロントエンド',
            '言語', 'フレームワーク', 'MicrosoftOffice', 'Slack', 'Zoom', 'AdobeAcrobatDC',
            '', '技能纏め', '技能歴等詳細', 'Webデザイン・DTPデザイン・言語', 'AdobeAcrobatPDF',
            '議事メモ作成', 'Teems', 'Teams', 'Outlook', 'AdobeAcrobat', '担当業務',
            'JPA', 'Jest', 'Pinia', 'Bootstrap', 'Windows', 'Mac', 'Linux', 'Koala',
            'Gulp', 'GIMP', 'AdobeAcrobatReader', 'レスポンシブ対応', 'AdobePhotoshopElements2021',
            'CMS', 'ALAYA', 'JSON', 'Ajax', 'Lightroom', 'Wacom', 'MediBangPaint', 'AfterEffect',
            'Premiere Pro', 'MOCA', 'Bshell', 'AdobeXD', 'BULMA', 'PHPTAL', 'DockerforWindows',
            'WindowsTerminal', 'WSL2', 'VSCODE', '顧客打ち合わせ', '備考', '【語学能力】', '日本語レベル'
            'No', 'Beego', 'XClarityController', 'iDRAC', 'Redmine', 'eclipseMars',
            'TeraTerm', 'Prott', 'レスポンシブウェブデザイン', 'Word', 'PowerPoint', 'Excel',
            'A5:SQLMk-2', 'XML', 'MovableType', 'DataSpider', '独自FW', '独自フレームワーク',
            'VisualBasicforApplications', 'VisualBasic', 'sitecore', 'Prepros', 'Selenium',
            'Jenkins', 'Miro', '写真撮影', '仕様書策定', 'MAMP', 'TeamSite', 'ecbeing', 'ネイティブアプリデザイン',
            'EJS', 'HandleBars', 'TweenMax', 'Riot.js', 'VirtualBox', 'AlmaLinux8', 'OracleSQLDeveloper',
            'Eclipse', 'サーバ対応', 'Systemwalker', 'NASSymantecAntivirus', 'SymantecAntivirus',
            'JP1', 'OS・その他', 'Backlog', 'SVN', 'Git', 'SourceTree', 'AIX', 'Teradata', 'AmazonLinux',
            'D3JS', 'Axios', 'npm', 'yarm', 'Beautify', 'Supabase', 'PostScript', 'HOLON',
            'LDL/YPS', 'ECCUBE', 'Twig', 'VBScript', 'PDFliB', 'SQLWorkBench', 'PgAdmin', 'Vagrant',
            'Virtualbox', 'DreamWeaver', 'AfterEffects', 'SITEPUBLIS', 'Scala', 'smartDB',
            'VB6', 'EC-CUBE', 'Grunt', 'composer', 'WSL', 'Autify', 'IntelliJ', 'Hutt', 'XAIML',
            'WACs', 'HAWK', 'HiRDB', 'A5SQL', 'Anaconda', 'VisualBasic6.0', 'VisualInterDev6.0',
            'DirectX', 'デザインガイドライン作成', 'ActionScript', 'RPGLE', 'MyBatis', 'JSF',
            'Doma', 'PrimeFaces', 'TQL', 'Biz/Browser', 'Groovy', 'AccessVBA', 'Android',
            'ECMAScript', 'Pug', 'Blade', 'Nextset', 'intra-mart', 'CodePipeline',
            'Devtools', 'AnimateCC', 'AdobeEncoder', 'OutSystemServiceStudio', 'OS',
            '・Windows', '・Mac', '', '・Linux', '・FileMarker', 'CLIPSTUDIOPAINT',
            'VenusFramework', 'JCL', 'EASY', 'DirectX9', 'OpenGL', '言語', 'フレームワーク',
            'Blazor', 'IDE等', 'Arduino', 'VisualStudio', 'AndroidStudio', 'XAMMP', 'AdobePremierePro',
            'NOREN', 'koala', 'Sitecore', 'Zeplin', 'XAMPP', 'DBBrowser', 'Almalinux8', 'RAD',
            'SQLSever2019Developer', 'EC-CUBE4', 'Proxmox', 'Growi', 'VSCode', 'Brackets', 'SublimeText',
            'WinMerge', 'KoaFramework', 'KendoUI', 'AdminLTE', 'electron', 'Svelte', 'Prisma',
            'Cordova', 'CAD', 'ColdFusion', 'SSMS', 'MySQLWorkbench', 'Putty', '業務効率化',
            'JuniperMX2020', 'MicrosoftOffice', 'SQLDwvwloper', '最寄り駅', '期間', '【業務概要】',
            '2年', '1年', 'VBE', 'LifeRay', 'SVG', 'Fireworks', 'Chart.js', 'pgadmin',
            'phpMyAdmin', 'Photshop', 'Tailwind', 'Maple', 'Sidekiq', 'SAI', 'ClipStudioPro', 'WinSCP',
            'ターミナル', 'SiteCore', 'webpack', 'VBS', 'Solaris11', 'Zoom', 'Cassandra', 'Salesforce',
            'RightNow', 'CGI', 'RealmDB', 'Characteristics', 'WorkAchievements', 'フレームワーク等', 'DB',
            'Rspecr', 'Capybara', 'AdobeExperienceManager', 'AdobeAcrobatDC', '機能設計', 'Indesign',
            'Redis', 'SemanticUI', 'ethna', 'sellenium', 'gRPC', 'Tarend', 'FujitsuSoftwareSymfowareServer',
            'MECM', 'WSUS', 'Primera', 'vCenter', 'DeepSecurity', 'Netprobe',
            'Metasequoia', 'SQLdeveloper', 'Dreameweaver', 'Canva', 'Davinciresolve', 'CapCut', 'ServiceNow', 'adminlte'
            'GridDB', 'Apache', 'Backbone.js', 'Playwright', 'Atom', 'MODXEvolution', 'WindowsForms',
            'MATLAB', 'ACCESS', 'RazerPage', 'Tomcat', 'openJDK', 'Fortinet',
            'FortiGate1100E,600F,100F', 'HPEAruba', 'AP-505-JP,AP-303-JP',
            '3CDaemon', 'SAP', 'Sketch', 'Protto', 'InVision', 'NPOI', 'Ethna',
            'PowerCMSX', 'AWSCertifiedSolutionsArchitect-Associate',
            'ITIL4ファンデーション', 'LPIC1', '技能歴等詳細', 'Webデザイン・DTPデザイン・言語',
            'VueCLI', 'PrimeNG', 'Stylus', 'yarn', 'gulp', 'grep', 'YAML', 'SEO',
            '資格/特技', 'INTARFRM', 'Symfoware', 'VC++', 'UML',
            'IBMRhapsody/TelelogicTau', 'PlantUML', 'アートディレクション',
            'スケジュール管理', 'terasoluna', 'AdobeAcrobatPDF', '議事メモ作成',
            'Androidstudio', 'T-SQL', 'VBscript', '2次元CAD', 'AviUtl',
            'FinalCutProX', '社内/企業向けマスターPCのキッティング', 'vSphereClient',
            'CitrixReceiver', 'CitrixDirector', 'CitrixXenApp', 'IBMDB2',
            'IBMNotes', 'ストアドルーチン', 'Teems', 'Outlook',
            'TransmissonNetworkDatabase', 'Nginx', 'IIS', 'Kibana', 'DataDog',
            'Grafana', 'AWSCertifiedSolutionsArchitect,Associate',
            'AWSCertifiedCloudPractitioner', 'Linux技術者認定Level-2',
            '基本情報技術者試験', 'Linux技術者認定Level-1', '情報セキュリティマネジメント',
            'Heroku', 'NESSUS', 'SKYSEA', 'HiveQL', 'Presto', 'SymfoWare',
            'Knockout.js', 'AdobeAcrobat', 'ライティング', 'SEO対策', 'コンクリート5',
            'SQLServerManagementStudio', 'ITIL4Foundation', '担当業務', 'ChakraUI',
            'SequelAce', 'pgAdmin4', 'K-shell', 'Gradle', 'SonarQube', 'PowerCMS',
            'VmwareWorkstationPlayer', 'McAfeeNSP', 'PaloAltoPA-850', 'JuniperSRX',
            'GNS3', 'OpenVas,OWASPZAP,BurpSuite', 'メンバー管理', 'ベンダー対応', 'Qt',
            'PyTorch', 'PHPStorm', 'FortiClient', 'Tensorflow', 'Pytorch',
            'scikit-learn', 'WPF', 'Bulma', 'PHPpgadmin', 'FreeBSD', 'SSG5',
            'FortiGate40F', 'YAMAHARTX', 'VB.NET2005', 'OpenAPI', 'HeartCoreCMS',
            'Access', 'Handlebars.js', 'JakartaEE', 'F5BIG-IPiSeries', 'Solaris',
            'F5BIG-IQ', 'PRIMERGY', 'fortigate', 'Bloomberg', 'OracleSuperCluster',
            'HPdlseries', 'Sparc', 'F5BIGIP-5250v', 'Fortigate1000D',
            'Alaxala2500s', 'A10Thunder6440', 'YAMAHASRT100,RTX1200', 'OpenStack',
            'Inspire', 'LotusNotes', 'Windows10', 'Windows7', 'WindowsXP',
            'IBMXIV', 'IBMDS6800/DS7000', 'SANSwitch', 'SQLServer2005', 'Apach',
            'Sencha'
        ]




