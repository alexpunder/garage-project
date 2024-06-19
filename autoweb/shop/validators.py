from django.contrib import messages
from django.core.exceptions import ValidationError


def validate_csv_file(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('Допустимы только .csv-файлы')


def check_filtered_products(request, products_data):

    if products_data.qs and request.GET.get('search') != '':
        messages.success(
            request, f'Совпадений найдено: {products_data.qs.count()}'
        )
        return True
    elif products_data.qs and request.GET.get('search') == '':
        messages.warning(
            request, 'Введите данные для поиска.'
        )
        return False
    else:
        messages.info(
            request, 'К сожалению, ничего не найдено...'
        )
        return False
