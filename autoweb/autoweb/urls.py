from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler403 = 'pages.views.page_forbidden'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.socialaccount.urls')),
    path(
        'accounts/', include('allauth.socialaccount.providers.google.urls')
    ),
    path(
        'accounts/', include('allauth.socialaccount.providers.yandex.urls')
    ),
    path('auth/', include('authorization.urls')),
    path('profile/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('shop.urls')),
    path('pages/', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
