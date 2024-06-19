import pytest

from users.models import Auto, CarMark


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        email='test@ya.ru',
        username='testovich',
        first_name='Test_name',
        last_name='Testovich_last_name',
        phone_number='89278882730'
    )


@pytest.fixture
def auth_user(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def car_mark():
    return CarMark.objects.create(
        mark='Audi'
    )


@pytest.fixture
def one_more_car_mark():
    return CarMark.objects.create(
        mark='BMW'
    )


@pytest.fixture
def auto_create_data(car_mark):
    return {
        'mark': car_mark.id,
        'model': 'A4'
    }


@pytest.fixture
def user_auto(user, car_mark):
    auto = Auto.objects.create(
        owner=user,
        vin_code='WAUZZZ44ZEN096063',
        mark=car_mark,
        model='Q5'
    )
    return auto


@pytest.fixture
def user_auto_valid_data(one_more_car_mark):
    return {
        'vin_code': 'WBAAM3334XCD12345',
        'mark': one_more_car_mark.id,
        'model': 'X6'
    }


@pytest.fixture
def auto_id(user_auto):
    return user_auto.id,


@pytest.fixture
def auth_user_valid_data():
    return {
        'email': 'new@mail.com',
        'first_name': 'New_name',
        'last_name': 'New_last_name',
        'phone_number': '88007775533'
    }
