from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--crawling",
            action="store_true",
            help="",
        )

    def handle(self, *args, **options):
        crawling = options.get('crawling', False)
