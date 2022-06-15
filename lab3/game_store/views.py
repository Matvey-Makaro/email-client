# from pure_pagination.mixins import PaginationMixin
import logging
import smtplib
import threading

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from game_store.models import Game, Category, Customer, Order
from lab3.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)


class OwnThread(threading.Thread):
    def __init__(self, gameName, gameCount, send_to):
        threading.Thread.__init__(self)
        self.send_to = send_to
        self.subject = 'Keys for vKiiNGz Game Store'
        self.msg = f'Hello, this is a vKiiNGz Game Store, we bought {gameCount} keys for your game {gameName},' \
                   f' please send them to us'

    def run(self) -> None:
        send_mail(
            subject=self.subject,
            from_email=EMAIL_HOST_USER,
            message=self.msg,
            recipient_list=[self.send_to],
            fail_silently=False,
        )


def send_message(gameName, gameCount, authorAddress):
    message = f'Hello, this is a vKiiNGz Game Store, we bought {gameCount} keys for your game {gameName},' \
              f' please send them to us'
    print(message)
    try:
        send_mail(
            subject='Keys for vKiiNGz Game Store',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[authorAddress],
            fail_silently=False
        )
    except(smtplib.SMTPDataError):
        print('Need real mail')
    return 0


class HomePage(TemplateView):
    model = Game
    template_name = 'game_store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = None
        category_id = self.request.GET.get('category')
        if category_id:
            return Game.objects.filter(cat=category_id)
        else:
            return Game.objects.filter(cat=1)

    def get(self, request, *args, **kwargs):
        logger.debug("homePage get request: " + str(request))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        logger.debug("homePage post request: " + str(request))
        logger.debug("homePage post request=" + str(request))
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        logger.debug("homePage cart contents: " + str(request.session['cart']))
        # print(request.session['cart'])

        cat = Game.objects.filter(id=product)
        category_id = cat[0].cat.pk
        if category_id:
            return redirect(reverse('home') + '?category=' + str(category_id))
        return redirect('home')

    def get_context_data(self, **kwargs):
        products = None
        category_id = self.request.GET.get('category')
        if category_id:
            products = Game.objects.filter(cat=category_id)
        else:
            products = Game.objects.filter(cat=1)
        categories = Category.objects.all()
        context = super(HomePage, self).get_context_data(**kwargs)
        context['categories'] = categories
        context['products'] = products
        return context


def login(request):
    if request.method == "GET":
        return render(request, 'game_store/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_msg = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                logger.debug("login customer mail: " + str(customer.email))
                request.session['cart'] = {}
                return redirect("home")
            else:
                error_msg = "Email or Password is incorrect."
        else:
            error_msg = "Email or Password is incorrect."
        return render(request, 'game_store/login.html', {'error_msg': error_msg})


def validate_customer(customer):
    err_msg = None
    if not customer.first_name:
        err_msg = "First Name Required."
    elif len(customer.first_name) < 3:
        err_msg = "First Name must be 3 characters long."
    elif not customer.last_name:
        err_msg = "Last Name Required."
    elif len(customer.last_name) < 3:
        err_msg = "Last Name must be 3 characters long."
    elif not customer.phone:
        err_msg = "Phone is Required."
    elif len(customer.phone) < 10:
        err_msg = "Phone Number must be 10 characters long."
    elif not (customer.phone.isdecimal()):
        err_msg = "Phone Number must contains only numbers."
    elif not customer.email:
        err_msg = "Email is Required."
    elif customer.does_exits():
        err_msg = "User with this email address already registered."
    elif not (customer.password):
        err_msg = "Password Required."
    return err_msg


def register_customer(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    values = {
        'firstname': first_name,
        'lastname': last_name,
        'phone': phone,
        'email': email,
    }
    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

    err_msg = None
    err_msg = validate_customer(customer)

    if not err_msg:
        customer.password = make_password(customer.password)
        customer.save()
        logger.debug("successful signup customer with mail: " + str(customer.email))
        return redirect('home')
    else:
        return render(request, 'game_store/signup.html', {'error_msg': err_msg, 'values': values})


def signup(request):
    if request.method == 'GET':
        return render(request, 'game_store/signup.html')
    else:
        return register_customer(request)


def logout(request):
    request.session.clear()
    return redirect('login')


def cart(request):
    cart_product_id = list(request.session.get('cart').keys())
    cart_product = Game.get_products_by_id(cart_product_id)
    return render(request, 'game_store/cart.html', {'cart_product': cart_product})


def checkout(request):
    if request.method == "POST":
        # sendMessage('GTA', 99, 'asdsda')
        address = request.POST.get("address")
        phone = (Customer.objects.filter(email=request.session.get("email")).first()).phone
        customer_id = request.session.get("customer_id")
        cart = request.session.get("cart")
        products = Game.get_products_by_id(list(cart.keys()))
        email_list = []
        for product in products:
            order = Order(customer=Customer(id=customer_id), product=product, price=product.price, address=address,
                          phone=phone, quantity=cart.get(str(product.id)))
            helpdict = {
                'gameName': product.name,
                'gameCount': cart.get(str(product.id)),
                'authorAddress': product.authorEmail
            }
            email_list.append(helpdict)
            if address:
                order.save()
        for i in range(len(email_list)):
            thread = OwnThread(email_list[i]['gameName'], email_list[i]['gameCount'], email_list[i]['authorAddress'])
            thread.start()

        request.session['cart'] = {}
        logger.debug("checkout successful order customer mail: " + str(request.session.get("email")))
        return redirect("cart")
    else:
        return render(request, 'game_store/checkout.html')
