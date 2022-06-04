from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mailclient.forms import SendEmailFrom
from mailclient.models import User


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SendEmailFrom(request.POST)
            if form.is_valid():
                sender = form.cleaned_data["from_email"]
                receiver = form.cleaned_data["to_email"]
                subject = form.cleaned_data["subject"]
                message = form.cleaned_data["message"]

            # TODO: Получить пароль для почты из бд и послать сообщение
            # tmp = send_mail(subject, message, sender, receiver, auth_user=sender, auth_password=password)
            # try:
            #     password = 'lgfjsjbceckawxgg'
            #     tmp = send_mail("Test programm", "Test programm", "matvey.makaro@gmail.com", ["makaro.matvey@gmail.com"],
            #                 auth_user="matvey.makaro@gmail.com", auth_password=password)
            #     print(f"Num of messages: {tmp}")
            # except ConnectionRefusedError:
            #     print(f"Exception ConnectionRefusedError")

            # try:
            #     send_mail(f'{subject} от {from_email}', message,
            #               DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
            # except BadHeaderError:
            #     return HttpResponse('Ошибка в теме письма.')
            # return redirect('success')

        else:
            form = SendEmailFrom()
        return render(request, 'mailclient/inbox.html', {'form': form})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse('login'))


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'mailclient/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'mailclient/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'mailclient/register.html', {
                'message': 'User name already taken.'
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
