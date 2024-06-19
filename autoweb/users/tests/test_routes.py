import pytest

from http import HTTPStatus
from pytest_django.asserts import assertRedirects

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('shop:homepage', None),
        ('account:profile', None),
        ('account:edit_profile', None),
        ('account:delete_profile', None),
        ('account:users_auto', None),
        ('account:add_auto', None),
        ('account:edit_auto', pytest.lazy_fixture('auto_id')),
        ('account:delete_auto', pytest.lazy_fixture('auto_id')),
    )
)
def test_auth_user_pages_availability(
        auth_user, name, args
):
    url = reverse(name, args=args)
    response = auth_user.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('account:profile', None),
        ('account:edit_profile', None),
        ('account:delete_profile', None),
        ('account:users_auto', None),
        ('account:add_auto', None),
        ('account:edit_auto', pytest.lazy_fixture('auto_id')),
        ('account:delete_auto', pytest.lazy_fixture('auto_id')),
    )
)
def test_anon_pages_redirect(
        client, name, args
):
    login_url = reverse('auth:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
