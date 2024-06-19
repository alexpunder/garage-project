from django.urls import path

from .order2pdf import order_pdf_file
from .send_email import send_user_mail
from .views import (
    create_order_view, order_details, orders_history, cancel_order,
)

app_name = 'order'

urlpatterns = [
    path(
        'create-order/',
        create_order_view,
        name='create_order'
    ),
    path(
        'cancel-order/<int:pk>/',
        cancel_order,
        name='cancel_order'
    ),
    path(
        'order-details/<int:pk>/',
        order_details,
        name='details'
    ),
    path(
        'order-history/',
        orders_history,
        name='history'
    ),
    path(
        'order-pdf-file/<int:pk>',
        order_pdf_file,
        name='pdf_file'
    ),
    path(
        'send-email/<int:pk>',
        send_user_mail,
        name='send_email'
    ),
]
