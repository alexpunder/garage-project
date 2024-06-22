from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import AutoForm, CustomUserEditForm
from .models import Auto, CustomUser


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserEditForm
    template_name = 'profile/edit_profile.html'
    context_object_name = 'cars'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('account:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать профиль'
        context['description'] = 'Страница редактирования профиля.'
        return context


class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'profile/delete_profile.html'
    context_object_name = 'cars'
    success_url = reverse_lazy('shop:homepage')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить профиль'
        context['description'] = 'Страница удаления профиля.'
        return context


class AutoListView(LoginRequiredMixin, ListView):
    model = Auto
    template_name = 'profile/users_auto.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Auto.objects.select_related(
            'owner',
        ).filter(
            owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Автомобили'
        context['description'] = 'Страница автомобилей пользователя.'
        return context


class AddAutoView(LoginRequiredMixin, CreateView):
    model = Auto
    form_class = AutoForm
    template_name = 'profile/add_auto.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account:users_auto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить автомобиль'
        context['description'] = 'Страница добавления автомобиля.'
        return context


class UpdateAutoView(LoginRequiredMixin, UpdateView):
    model = Auto
    form_class = AutoForm
    template_name = 'profile/edit_auto.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Auto, owner=self.request.user, pk=self.kwargs.get('auto_pk')
        )

    def get_success_url(self):
        return reverse('account:users_auto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать автомобиль'
        context['description'] = 'Страница редактирования автомобиля.'
        return context


class AutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Auto
    template_name = 'profile/delete_auto.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Auto, owner=self.request.user, pk=self.kwargs.get('auto_pk')
        )

    def get_success_url(self):
        return reverse('account:users_auto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить автомобиль'
        context['description'] = 'Страница удаления автомобиля.'
        return context


@login_required
def profile(request):
    template_name = 'profile/profile.html'
    user = get_object_or_404(CustomUser, email=request.user.email)
    cars = user.cars.all()
    context = {
        'user': user,
        'cars': cars,
        'title': 'Профиль',
        'description': 'Страница профиля пользователя.'
    }
    return render(request, template_name, context)
