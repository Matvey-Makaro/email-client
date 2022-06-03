from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render


def index(request):
    return HttpResponse("Страница приложения почтового клиента.")


def mails(request, mailid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Письмо номер</h1><p>{mailid}</p>")


def archive(request, year): # Удалить потом, это просто для теста
    if int(year) > 2022:
        raise Http404()



def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')