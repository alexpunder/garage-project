from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from .services import OrderServices

from cart.services import CartServices
from orders.models import Order
from autoweb.constants import ORDER_STATUS_CHECK


@login_required
def cancel_order(request, pk):
    template = 'orders/confirm_order_cancel.html'
    order, order_items = OrderServices.get_order_and_items(
        request.user, pk
    )

    if request.method == 'POST':
        OrderServices.cancel_order(order, order_items)
        return redirect('order:details', pk=pk)

    return render(request, template, context={'order': order})


@login_required
def create_order_view(request):
    if request.method == 'POST':
        cart, cart_items = CartServices.get_cart_and_items(request.user)

        if all([
            request.user.first_name,
            request.user.last_name,
            request.user.phone_number
        ]):
            check_order_exist, order_id = OrderServices.create_order(
                request, cart_items, cart
            )

            if not check_order_exist and not order_id:
                return redirect('cart:cart')

            messages.success(
                request, 'Благодарим за заказ!'
            )
            return redirect('cart:thank_you', pk=order_id)

        messages.info(
            request, 'Пожалуйста, проверьте и подтвердите заполнение полей.'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def order_details(request, pk):
    template = 'orders/order_details.html'
    order, order_items = OrderServices.get_order_and_items(
        request.user, pk
    )
    context = {
        'order': order,
        'order_items': order_items,
        'order_status_check': ORDER_STATUS_CHECK,
        'title': f'Заказа номер #{order.id}',
        'description': 'Страница с заказом.'
    }
    return render(request, template, context)


@login_required
def orders_history(request):
    template = 'orders/orders_history.html'
    orders_list = Order.objects.filter(
        user=request.user
    ).order_by('-id')
    context = {
        'orders_list': orders_list,
        'title': 'История заказов',
        'description': 'Страница с историей заказов.'
    }
    return render(request, template, context)
