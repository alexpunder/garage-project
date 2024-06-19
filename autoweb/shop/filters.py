import django_filters
from django import forms
from django.db.models import Q
from django_filters.widgets import RangeWidget

from .models import Brand, Category, Product, Subcategory


class CustomRangeWidget(RangeWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets[0].attrs.update({
            'placeholder': 'Минимальная',
            'class': 'form-control'
        })
        self.widgets[1].attrs.update({
            'placeholder': 'Максимальная',
            'class': 'form-control'
        })


class SearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_multiple_fields')

    class Meta:
        model = Product
        fields = ['search']

    def filter_by_multiple_fields(self, queryset, name, value):
        return queryset.filter(
            Q(article__icontains=value)
            | Q(specification__icontains=value)
            | Q(cross_list__icontains=value)
            | Q(brand__title__icontains=value)
        )


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all().order_by('id'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-label'
        }),
        label=''
    )
    subcategory = django_filters.ModelMultipleChoiceFilter(
        queryset=Subcategory.objects.all().order_by('id'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-label'
        }),
        label=''
    )
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all().order_by('title'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-label'
        }),
        label=''
    )
    price = django_filters.RangeFilter(
        widget=CustomRangeWidget(),
        label=''
    )

    class Meta:
        model = Product
        fields = [
            'category', 'subcategory', 'brand', 'price'
        ]
