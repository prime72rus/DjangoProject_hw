from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add test data to the database'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        call_command('loaddata', 'catalog/fixtures/category_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))

        call_command('loaddata', 'catalog/fixtures/product_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
