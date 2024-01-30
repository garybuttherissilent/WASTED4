from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'Delete all data from the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Get a list of all table names in your Django app
            table_names = connection.introspection.table_names(cursor)
            table_names = [table for table in table_names if table.startswith('api')]

            cursor.execute(f'TRUNCATE {", ".join(table_names)} RESTART IDENTITY CASCADE;')

            self.stdout.write(self.style.SUCCESS('Successfully deleted all data from the database'))
