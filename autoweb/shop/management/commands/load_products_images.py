import os
from csv import DictReader

from django.core.management import BaseCommand

from autoweb.settings import BASE_DIR
from shop.models import ProductImage


class Command(BaseCommand):
    """
    Команда для импорта данных из .csv-файлов в базу данных.
    """

    def handle(self, *args, **options):
        print('Загружаем картинки товаров..')
        file_path = 'shop/data/load_products_images.csv'

        with open(
            BASE_DIR.joinpath(file_path), 'r', encoding='utf-8-sig'
        ) as f:
            reader = DictReader(f, delimiter=';')
            for row in reader:
                try:
                    image_path = BASE_DIR.joinpath(
                        'media', row['image']
                    )
                    if not os.path.exists(image_path):
                        continue

                    else:
                        product_images = ProductImage(
                            id=row['id'],
                            image=row['image'],
                            product_id=row['product_id']
                        )
                        product_images.save()
                except Exception:
                    continue

        print('Загрузка завершена успешно!')
