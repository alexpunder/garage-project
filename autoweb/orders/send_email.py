from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from autoweb.settings import DEFAULT_FROM_EMAIL

from .services import OrderServices
from .tasks import send_email_task


def send_user_mail(request, pk):
    user = request.user
    email = user.email

    order, order_items = OrderServices.get_order_and_items(
        user, pk
    )

    data = []

    for order_item in order_items:
        data.append([
            order_item.product.article,
            order_item.product.brand.title,
            order_item.product.title,
            order_item.quantity,
            order_item.price_at_time_of_order,
            order_item.total_price,
        ])

    subject = 'Оформлен заказ на сайте "Автозапчасти ГАРАЖ".'
    html_message = render_to_string(
        'orders/user_email.html',
        {'data': data, 'title': subject, 'order': order}
    )
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL
    to_email = [email]

    send_email_task.delay(
        subject, plain_message, from_email, to_email, html_message
    )
    messages.success(
        request,
        'Сообщение успешно отправлено на почту!'
    )
    return redirect('cart:thank_you', pk=order.pk)
