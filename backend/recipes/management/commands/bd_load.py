import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient
from foodgram_backend.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Команда для заполнение базы данных ингредиентами.'

    def handle(self, *args, **options):
        self.ingredients(self, *args)

    def ingredients(self, *args):
        with open(
            BASE_DIR / 'data/ingredients.json', 'r', encoding='utf-8'
        ) as file:
            try:
                data = json.load(file)
                for index, row in enumerate(data):
                    data[index]['id'] = index
                records = [Ingredient(**row) for row in data]
                Ingredient.objects.bulk_create(records)
                self.stdout.write(
                    self.style.SUCCESS(
                        'База успешно заполнена ингредиентами'
                    )
                )
            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(
                        f'Ошибка {error} при записи в базу данных'
                    )
                )
