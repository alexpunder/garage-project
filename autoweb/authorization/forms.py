from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm,
    PasswordResetForm
)
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].error_messages = {
            'unique': 'Пользователь с такой почтой уже существует',
            'required': 'Необходимо указать электронную почту'
        }
        self.fields['email'].widget.attrs['placeholder'] = 'user@example.ru'

        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['placeholder'] = (
            'Подтвердите пароль'
        )
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password1', 'password2', 'captcha'
        ]


class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            'Пожалуйста, введите правильные значения электронной почты '
            'и пароля. Оба поля могут быть чувствительны к регистру.'
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'user@example.ru'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class CustomePasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = ''
        self.fields['old_password'].widget.attrs['placeholder'] = (
            'Введите старый пароль'
        )
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = (
            'Новый пароль'
        )
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['placeholder'] = (
            'Подтвердите новый пароль'
        )


class CustomePasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = (
            'user@example.ru'
        )
