import random

from django.shortcuts import render
from django.views.generic import TemplateView

from autoweb.constants import NOTES


def page_forbidden(request, exception):
    """
    Представление для обработки страницы 403 ошибки.
    """
    return render(request, 'util_pages/403.html', status=403)


def page_not_found(request, exception):
    """
    Представление для обработки страницы 404 ошибки.
    """
    return render(
        request,
        'util_pages/404.html',
        context={
            'title': 'Страница не найдена',
            'description': 'Страница с ошибкой 404.'
        },
        status=404
    )


def csrf_failure(request, reason=''):
    return render(request, 'util_pages/403csrf.html', status=403)


def server_error(request):
    """
    Представление для обработки страницы 500 ошибки.
    """
    note = random.choice(NOTES)
    context = {
        'note': note,
        'title': 'Сервер недоступен',
        'description': 'Страница с ошибкой 500.'
    }
    return render(
        request, 'util_pages/500.html', context, status=500)


class About(TemplateView):
    """
    Представление для страницы 'О нас'.
    """
    template_name = 'util_pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['description'] = 'Страница с описанием нашего магазина.'
        return context


class Contacts(TemplateView):
    """
    Представление для страницы 'Контакты'.
    """
    template_name = 'util_pages/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['description'] = 'Страница с контактами нашего магазина.'
        return context


class Confidential(TemplateView):
    """
    Представление для страницы 'Конфиденциальность'.
    """
    template_name = 'util_pages/confidential.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Конфиденциальность'
        context['description'] = 'Страница с конфиденциальностью.'
        return context


class Terms(TemplateView):
    """
    Представление для страницы 'Пользовательское соглашение'.
    """
    template_name = 'util_pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользовательское соглашение'
        context['description'] = 'Страница с пользовательским соглашением.'
        return context
