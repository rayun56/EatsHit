import datetime

from django.core.management.base import BaseCommand
from docmtu.helpers import collect_menu


class Command(BaseCommand):
    help = 'Updates the menus up to the specified number of days in the future'

    def add_arguments(self, parser):
        parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **options):
        collect_menu(through_date=datetime.date.today() + datetime.timedelta(days=options['days'][0]))
