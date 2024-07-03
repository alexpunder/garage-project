from csv import DictReader

from django.core.management import BaseCommand

from autoweb.constants import DB_DATA
from autoweb.settings import BASE_DIR
from shop.models import Brand, Category, Product, Subcategory
from users.models import CarMark


class Command(BaseCommand):
    """
    Команда для импорта данных из .csv-файлов в базу данных.
    """

    def load_categories(self, reader):
        for row in reader:
            category = Category(
                id=row['id'],
                title=row['title'],
                slug=row['slug'],
                image=row['image']
            )
            category.save()

    def load_subcategories(self, reader):
        for row in reader:
            category_instance = Category(
                id=row['category']
            )
            subcategory = Subcategory(
                id=row['id'],
                title=row['title'],
                category=category_instance,
                slug=row['slug'],
                image=row['image']
            )
            subcategory.save()

    def load_brands(self, reader):
        for row in reader:
            check_uniq = Brand.objects.filter(title=row['title']).exists()
            if check_uniq:
                continue
            brand = Brand(
                id=row['id'],
                title=row['title'],
                slug_brand=row['slug_brand'],
                producing_country=row['producing_country'],
                image=row['image']
            )
            brand.save()

    def load_products(self, reader):
        for row in reader:
            check_uniq = Product.objects.filter(id=row['id']).exists()
            if check_uniq:
                continue

            category_instance = Category.objects.get(
                id=row['category']
            )
            if row['subcategory']:
                subcategory_instance = Subcategory.objects.get(
                    id=row['subcategory']
                )
            brand_instance = Brand.objects.get(
                title=row['brand']
            )
            products = Product(
                id=row['id'],
                title=row['title'],
                article=row['article'],
                quantity=0,
                category=category_instance,
                subcategory=subcategory_instance,
                brand=brand_instance,
                price=0,
                specification=row['specification'],
                cross_list=row['cross_list']
            )
            products.save()

    def load_mark_auto(self, reader):
        for row in reader:
            mark = CarMark(
                mark=row['mark'],
            )
            mark.save()

    def handle(self, *args, **options):
        print('Загружаем данные')

        for key in DB_DATA.keys():
            file_path = DB_DATA[key]
            with open(
                BASE_DIR.joinpath(file_path), 'r', encoding='utf-8-sig'
            ) as f:
                reader = DictReader(f, delimiter=';')
                if key == 'category':
                    self.load_categories(reader)
                elif key == 'subcategory':
                    self.load_subcategories(reader)
                elif key == 'brand':
                    self.load_brands(reader)
                elif key == 'product':
                    self.load_products(reader)
                elif key == 'mark_auto':
                    self.load_mark_auto(reader)

                print(f'Загрузка {DB_DATA[key]} завершена успешно!')

        print('Загрузка завершена успешно!')
