import pytest
from django.urls import reverse

from pytest_django.asserts import assertRedirects

from users.models import Auto


def test_auth_user_can_edit_profile(
    auth_user, auth_user_valid_data, django_user_model
):
    url = reverse('account:edit_profile')
    response = auth_user.post(url, data=auth_user_valid_data)
    assertRedirects(response, reverse('account:profile'))
    check_user = django_user_model.objects.get()
    assert check_user.email == auth_user_valid_data['email']
    assert check_user.first_name == auth_user_valid_data['first_name']
    assert check_user.last_name == auth_user_valid_data['last_name']
    assert check_user.phone_number == auth_user_valid_data['phone_number']


def test_auth_user_can_delete_profile(
    auth_user, django_user_model
):
    url = reverse('account:delete_profile')
    response = auth_user.post(url)
    assertRedirects(response, '/')
    check_user_exist = django_user_model.objects.exists()
    assert not check_user_exist


@pytest.mark.django_db
def test_auth_user_can_add_auto(
    auth_user, auto_create_data
):
    url = reverse('account:add_auto')
    response = auth_user.post(url, data=auto_create_data)
    assertRedirects(response, reverse('account:users_auto'))
    check_user_auto_exist = Auto.objects.exists()
    assert check_user_auto_exist


@pytest.mark.parametrize(
    'name, args',
    (
        ('account:edit_auto', pytest.lazy_fixture('auto_id')),
    )
)
def test_auth_user_can_update_auto(
    auth_user, user_auto, user_auto_valid_data, name, args
):
    url = reverse(name, args=args)
    response = auth_user.post(url, data=user_auto_valid_data)
    assertRedirects(response, reverse('account:users_auto'))
    check_user_auto = Auto.objects.get()
    assert check_user_auto.vin_code == user_auto_valid_data['vin_code']
    assert check_user_auto.mark.id == user_auto_valid_data['mark']
    assert check_user_auto.model == user_auto_valid_data['model']


@pytest.mark.parametrize(
    'name, args',
    (
        ('account:delete_auto', pytest.lazy_fixture('auto_id')),
    )
)
def test_auth_user_can_delete_auto(
    auth_user, user_auto, name, args
):
    url = reverse(name, args=args)
    response = auth_user.post(url)
    assertRedirects(response, reverse('account:users_auto'))
    check_auto_exist = Auto.objects.exists()
    assert not check_auto_exist
