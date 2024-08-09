from django.core.management.base import BaseCommand, CommandError
from .utils.crawling_util import CrawlingUtils

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
            "-b",
            "--beautifulsoup",
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
        crawling = options.get('crawling', False)

    def startup(self):

