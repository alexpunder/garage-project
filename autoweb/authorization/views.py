from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView
)
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import (
    CustomUserCreationForm, CustomAuthForm,
    CustomePasswordChangeForm, CustomePasswordResetForm
)


class CustomUserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('shop:homepage')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(
            self.request, self.object,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация нового пользователя'
        context['description'] = 'Страница регистрации нового пользователя.'
        return context


class CustomAuthView(LoginView):
    form_class = CustomAuthForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Войти в профиль'
        context['description'] = 'Страница входа в профиль.'
        return context


class CustomePasswordChangeView(PasswordChangeView):
    form_class = CustomePasswordChangeForm


class CustomePasswordResetView(PasswordResetView):
    form_class = CustomePasswordResetForm
