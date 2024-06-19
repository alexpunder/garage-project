from django.core.paginator import Paginator

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
