from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from emailclient import settings
from mailclient.forms import *
from mailclient.models import *

from .mail_fetcher import MailFetcher
from .mail_parser import MailParser


###################################################################
# DEBUG
# from mailclient.test_email_tools.mail_fetcher import *
# from mailclient.test_email_tools.mail_parser import *
#
# def test_mail_fetch():
#     mail_fetcher = MailFetcher("pop.gmail.com", "matvey.makaro@gmail.com", 'lgfjsjbceckawxgg')
#     all_messages, allsizes, limit = mail_fetcher.downloadAllMessages()
#
#     # print(all_messages[0])
#     # print(type(all_messages))
#     print(type(all_messages[0]))
#
#     mail_parser = MailParser()
#     mail = mail_parser.parseMessage(all_messages[0])
#
#     print("Main Text:")
#     main_text = mail_parser.findMainText(mail)
#     print(main_text)
#     print("main_test[0]", main_text[0])
#     print(type(main_text))
#     print(type(main_text[0]))
#     print(f"Header: {mail.get}")
#
#     print(
#        "##############################################################################################################")

# mail_fetcher.disconnect(server)

##############################################################################


def test_imap_mail():
    mail_fetch = MailFetcher("matvey.makaro@gmail.com", 'lgfjsjbceckawxgg', "pop.gmail.com", 993)
    mail_fetch.get_messages(3)


##############################################################################

menu = [{'title': 'Send', 'url_name': 'send_mail'},
        {'title': 'Add mailbox', 'url_name': 'add_mailbox'},
        {'title': 'Log out', 'url_name': 'logout'},
        {'title': "About", 'url_name': 'about'}
        ]


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        context = {"title": "Mail",
                   "mailboxes": Mailbox.objects.filter(user=request.user),
                   # TODO: Возможно надо показывать все сообщение пользователя, а возможно и нет
                   # "emails": Email.objects.filter(user=request.user),
                   "menu": menu}
        return render(request, 'mailclient/index.html', context)

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse('login'))


# TODO: Удалить перед сдачей
# def index(request):
#     # Authenticated users view their inbox
#     test_imap_mail()
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = SendEmailFrom(request.POST)
#             if form.is_valid():
#                 sender = form.cleaned_data["from_email"]
#                 receiver = form.cleaned_data["to_email"]
#                 subject = form.cleaned_data["subject"]
#                 message = form.cleaned_data["message"]
#
#             # tmp = send_mail(subject, message, sender, receiver, auth_user=sender, auth_password=password)
#             # try:
#             #     password = 'lgfjsjbceckawxgg'
#             #     tmp = send_mail("Test programm", "Test programm", "matvey.makaro@gmail.com", ["makaro.matvey@gmail.com"],
#             #                 auth_user="matvey.makaro@gmail.com", auth_password=password)
#             #     print(f"Num of messages: {tmp}")
#             # except ConnectionRefusedError:
#             #     print(f"Exception ConnectionRefusedError")
#
#             # try:
#             #     send_mail(f'{subject} от {from_email}', message,
#             #               DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
#             # except BadHeaderError:
#             #     return HttpResponse('Ошибка в теме письма.')
#             # return redirect('success')
#
#         else:
#             form = SendEmailFrom()
#         return render(request, 'mailclient/inbox.html', {'form': form})
#
#     # Everyone else is prompted to sign in
#     else:
#         return HttpResponseRedirect(reverse('login'))


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


def mail(request, mail_id):
    if request.user.is_authenticated:
        try:
            curr_mail = Email.objects.get(id=mail_id)
            if request.user == curr_mail.user:
                context = {"title": "Mail",
                           "mailboxes": Mailbox.objects.filter(user=request.user),
                           "menu": menu,
                           "mail": curr_mail}
                return render(request, 'mailclient/mail.html', context)
            else:
                return HttpResponseRedirect(reverse('index'))
        except Exception:
            raise Http404
    else:
        return HttpResponseRedirect(reverse('login'))


def mailbox(request, mailbox_id):
    # TODO: Добавить отправителя и время отправки сообщения в mail.html
    context = {"title": "Mailbox",
               "mailboxes": Mailbox.objects.filter(user=request.user),
               "menu": menu}
    if request.user.is_authenticated:
        try:
            mailbox = Mailbox.objects.get(id=mailbox_id)
            if mailbox.user != request.user:
                raise Http404()
        except Exception:
            raise Http404

        address = mailbox.address
        password = mailbox.password
        imap4_server_name, server_port = MailParser.get_imap_server_by_address(address)
        mail_fetcher = MailFetcher(address, password, imap4_server_name, server_port)

        try:
            messages, last_email_id = mail_fetcher.get_messages(Mailbox.objects.get(pk=mailbox_id).last_email_id)
            Mailbox.objects.update(last_email_id=last_email_id)
        except Exception:
            context["message"] = "Unable to access the server, please try again later"
            return render(request, 'mailclient/index.html', context)

        try:
            MailParser.save_messages(messages, request.user)
        except Exception:
            pass

        try:
            mailbox = Mailbox.objects.get(id=mailbox_id)
            context["emails"] = Email.objects.filter(user=request.user).filter(recipients=mailbox.address). \
                order_by("-timestamp")
        except Exception:
            pass

        return render(request, 'mailclient/index.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def archive(request, year):  # Удалить потом, это просто для теста
    if int(year) > 2022:
        raise Http404()


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def add_mailbox(request):
    context = {"title": "Mail",
               "menu": menu,
               "mailboxes": Mailbox.objects.filter(user=request.user),
               }
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = GetMailBox(request.POST)
            if form.is_valid():
                address = form.cleaned_data["address"]
                password = form.cleaned_data["password"]
                is_exist = False
                try:
                    for u in User.objects.filter(mailbox__address=address):
                        if u == request.user:
                            context['message'] = "This mailbox already exists"
                            context['form'] = form
                            is_exist = True
                except User.DoesNotExist:
                    print("User.DoesNotExist in add_mailbox")
                if not is_exist:
                    # TODO: Заменить на нормальные server и port
                    server_name, port = MailParser.get_imap_server_by_address(address)
                    mail_fetcher = MailFetcher(address, password, server_name, port)
                    if mail_fetcher.is_valid_mailbox():
                        Mailbox.objects.create(address=address, password=password, user=request.user)
                        form = GetMailBox()
                        context["form"] = form
                    else:
                        context['message'] = "No such mailbox"
                        context['form'] = form
        else:
            form = GetMailBox()
            context["form"] = form
        return render(request, 'mailclient/addmailbox.html', context)
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse('login'))


def send_email(request):
    context = {"title": "Mail",
               "menu": menu,
               "mailboxes": Mailbox.objects.filter(user=request.user),
               }
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = SendEmailForm(request.POST)
                if form.is_valid():
                    from_email = form.cleaned_data["from_email"]
                    to_email = form.cleaned_data["to_email"]
                    subject = form.cleaned_data["subject"]
                    message = form.cleaned_data["message"]

                    is_authorized = True
                    try:
                        password = Mailbox.objects.filter(address=from_email).get(user=request.user).password
                    except Exception:
                        context["message"] = "You are not authorized in this mailbox"
                        is_authorized = False

                    if is_authorized:
                        smtp_server_name, port = MailParser.get_smtp_server_by_address(from_email)
                        settings.EMAIL_HOST = smtp_server_name
                        settings.EMAIL_PORT = port
                        send_mail(subject, message, from_email, [to_email], auth_user=from_email,
                                  auth_password=password)
                        form = SendEmailForm()
            else:
                form = SendEmailForm()
            context["form"] = form
            return render(request, "mailclient/sendemail.html", context)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception:
        context["message"] = "Failed to send message"
        form = SendEmailForm(request.POST)
        context["form"] = form
        return render(request, "mailclient/sendemail.html", context)


def about(request):
    return HttpResponse("Страница about")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
