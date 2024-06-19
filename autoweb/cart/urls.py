from django.urls import path

from .views import (add_to_cart, cart, checkout, delete_cart_item,
                    thank_you_page, update_cart_item, update_user_checkout)

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('add/<int:pk>/', add_to_cart, name='cart_add'),
    path('update-cart-item/', update_cart_item, name='update_cart_item'),
    path('delete/<int:pk>', delete_cart_item, name='cart_delete'),
    path('checkout/', checkout, name='checkout'),
    path(
        'update-user-checkout/', update_user_checkout, name='update_checkout'
    ),
    path(
        'checkout/thank-you/<int:pk>', thank_you_page, name='thank_you'
    ),
]
