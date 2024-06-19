from django.db import transaction
from django.shortcuts import get_object_or_404

from shop.models import Product

from .models import Cart, CartItem


class CartServices:

    @staticmethod
    def get_cart_and_items(user):
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.cartitem_set.prefetch_related('product').all()
        return cart, cart_items

    @staticmethod
    def add_to_cart(user, product, quantity=1):
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=user)
            cart_product, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            if not created:
                updated_quantity = cart_product.quantity + quantity
                final_quantity = min(updated_quantity, product.quantity)
                if cart_product.quantity != final_quantity:
                    cart_product.quantity = final_quantity
                    cart_product.save()
                else:
                    return False
            else:
                cart_product.quantity = min(quantity, product.quantity)
                cart_product.save()

            return True

    @staticmethod
    def delete_cart_item(user, pk):
        with transaction.atomic():
            cart_item = CartItem.objects.get(
                cart=get_object_or_404(Cart, user=user),
                product=get_object_or_404(Product, pk=pk)
            )
            cart_item.delete()
