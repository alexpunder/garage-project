from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(
        'Электронная почта',
        unique=True
    )
    username = models.CharField(
        max_length=17,
        unique=False,
        blank=True,
        default=''
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        default=''
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('account:profile')


class Auto(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Владелец'
    )
    vin_code = models.CharField(
        'Вин-код автомобиля',
        max_length=17,
        blank=True,
        null=True
    )
    mark = models.ForeignKey(
        'CarMark',
        on_delete=models.CASCADE,
        verbose_name='Марка',
    )
    model = models.CharField(
        'Модель',
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Авто'

    def __str__(self):
        return f'{self.mark} {self.model}'

    def get_absolute_url(self):
        return reverse('account:users_auto')


class CarMark(models.Model):
    mark = models.CharField(
        'Марка авто',
        max_length=50
    )

    class Meta:
        verbose_name = 'Марка авто'
        verbose_name_plural = 'Марки авто'

    def __str__(self):
        return self.mark
