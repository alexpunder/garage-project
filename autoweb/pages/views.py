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
    return render(request, 'util_pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'util_pages/403csrf.html', status=403)


def server_error(request):
    """
    Представление для обработки страницы 500 ошибки.
    """
    note = random.choice(NOTES)
    context = {
        'note': note,
    }
    return render(
        request, 'util_pages/500.html', context, status=500)


class About(TemplateView):
    """
    Представление для страницы 'О нас'.
    """
    template_name = 'util_pages/about.html'


class Contacts(TemplateView):
    """
    Представление для страницы 'Контакты'.
    """
    template_name = 'util_pages/contacts.html'


class Confidential(TemplateView):
    """
    Представление для страницы 'Конфиденциальность'.
    """
    template_name = 'util_pages/confidential.html'


class Terms(TemplateView):
    """
    Представление для страницы 'Пользовательское соглашение'.
    """
    template_name = 'util_pages/terms.html'
