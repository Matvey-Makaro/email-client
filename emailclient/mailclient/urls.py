from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register, name='register'),
    path('add_mailbox', add_mailbox, name='add_mailbox'),
    path('send_email', send_email, name='send_mail'),
    path('mail/<int:mail_id>/', mail, name='mail'),
    path('mailbox/<int:mailbox_id>/', mailbox, name='mailbox'),
    path('about', about, name='about'),
    path('archive/<int:year>/', archive),
]
