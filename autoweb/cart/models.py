from django.contrib.auth import get_user_model
from django.db import models

from shop.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    products = models.ManyToManyField(
        Product,
        through='CartItem',
        verbose_name='Товар'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def get_cart_items(self):
        cart_items = self.cartitem_set.prefetch_related('product').all()
        return cart_items

    def clear_cart(self):
        return self.get_cart_items().delete()

    @property
    def total_price(self):
        cart_items = self.get_cart_items()
        total_price = sum(
            cart_item.total_price for cart_item in cart_items
        )
        return total_price

    @property
    def count(self):
        return self.get_cart_items().count()

    def __str__(self):
        return f'Корзина {self.id} пользователя: {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    @property
    def total_price(self):
        total_price = self.quantity * self.product.price
        return total_price

    def __str__(self):
        return f'Итого: {self.quantity} x {self.product.title}'
