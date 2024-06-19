import re

from django import forms

from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import Auto, CarMark, CustomUser
from autoweb.constants import VIN_CODE_VALIDATOR


class CustomUserEditForm(forms.ModelForm):
    phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['phone_number'].label = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = (
            '8-999-777-55-33'
        )
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'user@example.ru'
        self.fields['email'].error_messages = {
            'unique': 'Пользователь с такой почтой уже существует',
            'required': 'Необходимо указать электронную почту'
        }

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'phone_number',
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(
            phone_number=phone_number
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise ValidationError('Этот номер уже существует')
        return phone_number


class CustomUserEditFormCheckout(forms.ModelForm):
    phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].required = True
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['phone_number'].required = True
        self.fields['phone_number'].label = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = (
            'Номер телефона'
        )

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'phone_number',
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(
            phone_number=phone_number
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise ValidationError('Этот номер уже существует')
        return phone_number


class AutoForm(forms.ModelForm):
    mark = forms.ModelChoiceField(
        queryset=CarMark.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mark'].label = 'Марка'

    class Meta:
        model = Auto
        fields = (
            'vin_code', 'mark', 'model'
        )
        widgets = {
            'vin_code': forms.TextInput(attrs={
                'placeholder': '...или номер кузова'
            })
        }

    def clean_vin_code(self):
        vin_code = self.cleaned_data.get('vin_code')
        if vin_code:
            if re.match(VIN_CODE_VALIDATOR, vin_code):
                return vin_code
            raise ValidationError(
                'Возможно использовать только большие и/или маленькие '
                'буквы латинского алфавита; цифры в диапазоне от 0 до 9.'
            )
        return ''
