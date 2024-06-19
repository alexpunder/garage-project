import pytest

from shop.models import Product, Category, Subcategory, Brand
from cart.models import Cart, CartItem


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        email='test@ya.ru',
        username='testovich'
    )


@pytest.fixture
def auth_user(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def category():
    category = Category.objects.create(
        slug='kolodki'
    )
    return category


@pytest.fixture
def subcategory():
    subcategory = Subcategory.objects.create(
        slug='perednie'
    )
    return subcategory


@pytest.fixture
def brand():
    brand = Brand.objects.create(
        slug_brand='sangsin'
    )
    return brand


@pytest.fixture
def product(category, subcategory, brand):
    product = Product.objects.create(
        article='1399A',
        category=category,
        subcategory=subcategory,
        brand=brand,
        price=1000
    )
    return product


@pytest.fixture
def auth_user_cart(auth_user):
    cart = Cart.objects.create(
        user=auth_user
    )
    return cart


@pytest.fixture
def cart_item(product, auth_user_cart):
    cart_item = CartItem.objects.create(
        cart=auth_user_cart,
        product=product,
        quantity=1
    )
    return cart_item
