from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('mail/<int:mailid>/', mails),
    path('archive/<int:year>/', archive),
]
