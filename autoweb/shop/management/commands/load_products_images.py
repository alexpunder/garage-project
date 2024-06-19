import os
from csv import DictReader, DictWriter

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
        file_path_not_images = 'shop/data/not_images.csv'

        with open(
            BASE_DIR.joinpath(file_path), 'r', encoding='utf-8-sig'
        ) as f:
            with open(
                BASE_DIR.joinpath(file_path_not_images), 'w',
                encoding='utf-8-sig', newline=''
            ) as f_not_image:
                reader = DictReader(f, delimiter=';')
                writer = DictWriter(f_not_image, delimiter=';', fieldnames=['ids'])
                for row in reader:
                    try:
                        image_path = BASE_DIR.joinpath(
                            'media', row['image']
                        )
                        if not os.path.exists(image_path):
                            writer.writerow({'ids': row['image']})
                            print(f'Файл {image_path} не найден, пропускаем.')

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
