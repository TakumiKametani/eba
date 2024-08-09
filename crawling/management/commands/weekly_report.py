from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--target",
            help="",
        )

    def handle(self, *args, **options):
        target = options.get('target', False)



