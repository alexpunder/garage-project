from django.db import models
from django.urls import reverse

from users.models import CustomUser
from shop.models import Product
from autoweb.constants import ORDER_STATUS_CHOICES


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа',
    )
    is_confirmed = models.BooleanField(
        'Подтверждение заказа',
        default=False,
        help_text='Был ли уже оформлен заказ',
        blank=True
    )
    status = models.CharField(
        'Статус заказа',
        default='Без статуса',
        choices=ORDER_STATUS_CHOICES,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_order_items(self):
        order_items = self.orderitem_set.prefetch_related('product').all()
        return order_items

    @property
    def total_price(self):
        total_price = 0
        for item in self.get_order_items():
            total_price += item.total_price
        return total_price

    @property
    def count(self):
        return self.get_order_items().count()

    def __str__(self):
        return f'Заказ №{self.id} от {self.created_at}.'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество товара',
    )
    price_at_time_of_order = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Цена товара при заказе',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    @property
    def total_price(self):
        return self.price_at_time_of_order * self.quantity

    def __str__(self):
        return f'Товар {self.product}, заказ №{self.order.id}.'

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            kwargs={
                'category_slug': self.product.category.slug,
                'subcategory_slug': self.product.subcategory.slug,
                'pk': self.pk
            }
        )
