from django.contrib.auth import logout, authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mailclient.models import User


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, 'mailclient/inbox.html')

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse('login'))


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'mailclient/login.html', {
                'message': 'Invalid email and/or password.'
            })
    else:
        return render(request, 'mailclient/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'mailclient/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'mailclient/register.html', {
                'message': 'Email address already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'mailclient/register.html')


def mails(request, mailid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Письмо номер</h1><p>{mailid}</p>")


def archive(request, year): # Удалить потом, это просто для теста
    if int(year) > 2022:
        raise Http404()


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')