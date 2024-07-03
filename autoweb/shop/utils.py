from csv import DictReader
from io import TextIOWrapper

from django.core.paginator import Paginator

from .models import Product, Category, Subcategory, Brand
from autoweb.constants import FILTERED_DATA


def paginate_items(request, items, items_on_page):
    paginator = Paginator(items, items_on_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def convert_specification_and_crosslist_to_valid_data(
    context, specification, cross_list
):
    try:
        specification_dict = {}
        text = specification.split('\n')
        for item in text:
            key, value = item.split(':')
            specification_dict[key + ':'] = value
        text_cross_list = cross_list.split('\n')

        context['specification_dict'] = specification_dict
        context['text_cross_list'] = text_cross_list

        return context

    except (ValueError, KeyError, TypeError) as error:
        print(f'Возникла ошибка при форматирования данных: {error}')
        return None


def get_filters_count(items_data):
    filters_count = 0

    for key, value in items_data.data.items():
        if key in FILTERED_DATA and value != '':
            filters_count += 1

    return filters_count


def handle_uploaded_file(csv_loader_instance):
    if csv_loader_instance.file:
        with csv_loader_instance.file.open(mode='r') as file:
            text_wrapper = TextIOWrapper(file, encoding='cp1251')
            reader = DictReader(text_wrapper, delimiter=';')
            for row in reader:

                if not Product.objects.filter(id=row['id']).exists():
                    continue

                qty = row['quantity'].split(',')[0]
                price = row['price'].split(',')[0]
                price = price.replace('\xa0', '')

                product = Product.objects.get(id=row['id'])
                product.quantity = int(qty)
                product.price = int(price)
                product.save()


def handler_upload_new_products_file(file_instance):
    if file_instance.file:
        with file_instance.file.open(mode='r') as file:
            text_wrapper = TextIOWrapper(file, encoding='utf-8-sig')
            reader = DictReader(text_wrapper, delimiter=';')

            products_data = []
            for row in reader:
                if Product.objects.filter(id=row['id']).exists():
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
                product = Product(
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
                products_data.append(product)
            Product.objects.bulk_create(products_data)
