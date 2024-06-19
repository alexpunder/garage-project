from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import (CustomUserCreateView, CustomAuthView,
                    CustomePasswordChangeView, CustomePasswordResetView)

app_name = 'auth'

urlpatterns = [
    path(
        'registration/',
        CustomUserCreateView.as_view(),
        name='registration'
    ),
    path(
        'login/',
        CustomAuthView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'password-reset/',
        CustomePasswordResetView.as_view(
            success_url=reverse_lazy('auth:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('auth:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'password-change/',
        CustomePasswordChangeView.as_view(
            success_url=reverse_lazy('auth:password_change_done')
        ),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
]
