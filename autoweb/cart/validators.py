from django.contrib import messages


def check_product_price_and_qty(request, product):

    if product.quantity <= 0:
        messages.error(
            request,
            'Товара нет в наличии.'
        )
        return False

    if product.price <= 0:
        messages.error(
            request,
            (
                'К сожалению, у товара указана некорректная цена. '
                'Приносим извинения за доставленные неудобства.'
            )
        )
        return False

    return True


def check_items_in_cart(request, cart_items):

    if not cart_items:
        messages.error(
            request,
            'При оформлении заказа, корзина не может быть пустой.'
        )
        return False

    for item in cart_items:
        if item.product.quantity < item.quantity:
            messages.error(
                request,
                (
                    f'Недостаточно товара {item.product.title}. '
                    f'На складе: {item.product.quantity} шт.'
                )
            )
            return False

    return True
