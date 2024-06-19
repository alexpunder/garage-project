from django.urls import path

from .views import About, Confidential, Contacts, Terms

app_name = 'pages'

urlpatterns = [
    path('about/', About.as_view(), name='about'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('confidential/', Confidential.as_view(), name='confidential'),
    path('terms-and-conditions/', Terms.as_view(), name='terms'),
]
