from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from autoweb.constants import TITELES_DATA
from orders.services import OrderServices
from shop.models import Product
from users.forms import CustomUserEditFormCheckout

from .models import Cart, CartItem
from .services import CartServices
from .utils import get_pk_from_path
from .validators import check_items_in_cart, check_product_price_and_qty


@login_required
def cart(request):
    template = 'cart/cart.html'
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)

    context = {
        'cart_products': CartItem.objects.filter(cart=cart),
        'cart': cart,
        'title': TITELES_DATA['cart']
    }

    return render(request, template, context)


@login_required
def add_to_cart(request, pk):

    if request.method == 'GET':
        path_of_next = request.build_absolute_uri()
        product_pk = get_pk_from_path(path_of_next)
        product = get_object_or_404(Product, pk=product_pk)
        return redirect(
            'shop:product_detail',
            category_slug=product.category.slug,
            subcategory_slug=product.subcategory.slug,
            pk=product_pk
        )

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        if not check_product_price_and_qty(request, product):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        quantity = int(request.POST.get('quantity', 1))
        success_cart = CartServices.add_to_cart(
            request.user, product, quantity
        )

        if success_cart:
            messages.success(
                request, 'Товар добавлен в корзину.'
            )
        else:
            messages.warning(
                request, 'Добавлено максимально возможное количество товара.'
            )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_cart_item(request, pk):
    CartServices.delete_cart_item(request.user, pk)

    messages.success(
        request, 'Товар успешно удалён из корзины.'
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_cart_item(request):
    if (
        request.method == 'POST'
        and request.headers.get('x-requested-with') == 'XMLHttpRequest'
    ):
        with transaction.atomic():
            cart_item_id = request.POST.get('cart_item_id')
            new_quantity = int(request.POST.get('new_quantity'))
            cart_id_value = request.POST.get('cart_id')
            if not cart_id_value:
                return JsonResponse({
                    'success': False,
                    'error': 'cart_id не обнаружен.'
                })

            cart_id = int(cart_id_value)

            cart = Cart.objects.get(pk=cart_id)
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            if new_quantity > cart_item.product.quantity:
                return JsonResponse({
                    'success': False,
                    'error': 'Нельзя добавить больше, чем есть.'
                })
            cart_item.quantity = new_quantity
            cart_item.save()
            return JsonResponse({
                'success': True,
                'cart_item_id': cart_item.id,
                'cart_item_quantity': cart_item.quantity,
                'cart_item_total_price': cart_item.total_price,
                'cart_total_price': cart.total_price
            })
    else:
        return JsonResponse({
            'success': False, 'error': 'Неверный метод запроса'
        })


@login_required
def checkout(request):
    template = 'cart/checkout.html'
    cart, cart_products = CartServices.get_cart_and_items(request.user)

    if not check_items_in_cart(request, cart_products):
        return redirect('cart:cart')

    form = CustomUserEditFormCheckout(instance=request.user)
    context = {
        'cart': cart,
        'cart_products': cart_products,
        'user': request.user,
        'form': form,
        'title': TITELES_DATA['checkout']
    }
    return render(request, template, context)


@login_required
def update_user_checkout(request):
    if request.method == 'POST':
        form = CustomUserEditFormCheckout(
            request.POST, instance=request.user
        )
        if form.is_valid():
            with transaction.atomic():
                form.save()
                messages.success(
                    request, 'Данные пользователя обновлены.'
                )
                return HttpResponseRedirect(reverse('cart:checkout'))
        else:
            cart, cart_products = CartServices.get_cart_and_items(request.user)
            context = {
                'cart': cart,
                'cart_products': cart_products,
                'user': request.user,
                'form': form
            }
            messages.error(
                request,
                (
                    'Пожалуйста, проверьте корректность введённых '
                    'данных пользователя.'
                )
            )
            return render(request, 'cart/checkout.html', context)
    else:
        return HttpResponseRedirect(reverse('cart:checkout'))


@login_required
def thank_you_page(request, pk):
    template = 'cart/thank_you.html'
    order, order_items = OrderServices.get_order_and_items(
        request.user, pk
    )

    if not order.is_confirmed:
        if OrderServices.confirm_order(order, order_items):
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, template, context)
        else:
            messages.error(
                request, 'Ошибка при подтверждении заказа.'
            )
            return HttpResponseRedirect(
                reverse('cart:cart')
            )
    else:
        context = {
            'order': order,
            'order_items': order_items
        }
        return render(request, template, context)
