from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from shop.models import Product
from .tasks import send_telegram_message

from cart.validators import check_items_in_cart


class OrderServices:

    @staticmethod
    def confirm_order(order, order_items):

        if order_items:
            with transaction.atomic():
                updated_data = []

                for item in order_items:
                    updated_data.append(
                        Product(
                            id=item.product.id,
                            quantity=F('quantity') - item.quantity
                        )
                    )

                Product.objects.bulk_update(updated_data, ['quantity'])
                order.is_confirmed = True
                order.status = 'Обработка заказа'
                order.save()
            return True
        return False

    @staticmethod
    def create_order(request, cart_items, cart):

        if not check_items_in_cart(request, cart_items):
            return False, None

        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            order_items = []

            for item in cart_items:
                order_items.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price_at_time_of_order=item.product.price,
                    )
                )

            OrderItem.objects.bulk_create(order_items)
            cart.clear_cart()

        created = order.created_at.strftime('%d.%m.%Y')
        message = (
            f'Создан новый заказ: №{order.id}. Создан: {created}\n'
            f'Заказчик: {order.user.first_name} {order.user.last_name}.\n'
            f'Тел.: {order.user.phone_number}'
        )
        send_telegram_message.delay(message)
        return True, order.id

    @staticmethod
    def cancel_order(order, order_items):

        with transaction.atomic():
            order.status = 'Отменен клиентом'
            order.save()

            updated_data = []
            for item in order_items:
                updated_data.append(
                    Product(
                        id=item.product.id,
                        quantity=F('quantity') + item.quantity
                    )
                )
            Product.objects.bulk_update(updated_data, ['quantity'])

        message = (
            f'Клиент ОТМЕНИЛ заказ: {order.user.get_full_name()}.\n'
            f'Номер заказа на сайте: #{order.id}.'
        )
        send_telegram_message.delay(message)

    @staticmethod
    def get_order_and_items(user, pk, need_items_too=True):
        order = get_object_or_404(Order, user=user, pk=pk)

        if need_items_too:
            order_items = order.get_order_items()
            return order, order_items

        return order
