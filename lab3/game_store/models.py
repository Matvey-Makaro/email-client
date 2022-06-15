from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Category's name")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
        ordering = ['name']


class Game(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name="Game's name")
    price = models.IntegerField(default=0, blank=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Description")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Photo")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Time of editing")
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Category ID")
    authorEmail = models.EmailField(max_length=255, default="xxx@gmail.com")

    def __str__(self):
        return self.name

    def get_products_by_id(cart_product_id):
        return Game.objects.filter(id__in=cart_product_id)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ['name', 'time_create']


class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First name", default=None)
    last_name = models.CharField(max_length=100, verbose_name="Last name", default=None)
    phone = models.CharField(max_length=30, verbose_name="phone", default=None)
    email = models.EmailField(verbose_name="Email", default=None)
    password = models.CharField(max_length=255, verbose_name="Password")

    def __str__(self):
        return self.first_name + " " + self.last_name

    def does_exits(self):
        return Customer.objects.filter(email=self.email)

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['email']


class Order(models.Model):
    product = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Game id")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer id")
    quantity = models.IntegerField(verbose_name="Quantity")
    price = models.IntegerField(verbose_name="Price")
    address = models.CharField(max_length=100, default=None, verbose_name="Address")
    phone = models.CharField(max_length=30, verbose_name="Phone")
    date = models.DateTimeField(default=datetime.datetime.today, verbose_name="Date")

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['customer']
