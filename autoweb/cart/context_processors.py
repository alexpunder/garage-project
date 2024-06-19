from .models import Cart, CartItem


def cart_context_processor(request):
    context = {}

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            cart = Cart.objects.create(user=request.user)

        context = {
            'cart_products': CartItem.objects.filter(cart=cart),
            'cart': cart
        }
        return context

    return context
