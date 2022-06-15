from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage.as_view(), name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout")
]