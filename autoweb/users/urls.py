from django.urls import path

from .views import (AutoDeleteView, AutoListView,
                    CustomUserDeleteView, CustomUserUpdateView,
                    AddAutoView, profile, UpdateAutoView)

app_name = 'account'

urlpatterns = [
    path(
        '',
        profile,
        name='profile'
    ),
    path(
        'edit-profile/',
        CustomUserUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'delete-profile/',
        CustomUserDeleteView.as_view(),
        name='delete_profile'
    ),
    path(
        'auto/',
        AutoListView.as_view(),
        name='users_auto'
    ),
    path(
        'add-auto/',
        AddAutoView.as_view(),
        name='add_auto'
    ),
    path(
        'edit-auto/<int:auto_pk>/',
        UpdateAutoView.as_view(),
        name='edit_auto'
    ),
    path(
        'delete-auto/<int:auto_pk>/',
        AutoDeleteView.as_view(),
        name='delete_auto'
    ),
]
