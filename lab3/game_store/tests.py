import rest_framework.status as status
from django.test import Client
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from game_store.models import Category, Game


class GameStoreApiTestCase(APITestCase):
    def test_homePage_get(self):
        url = reverse_lazy('home')
        code = self.client.get(url).status_code
        self.assertEqual(status.HTTP_200_OK, code)

    def test_signUp_get(self):
        url = reverse_lazy('signup')
        code = self.client.get(url).status_code
        self.assertEqual(status.HTTP_200_OK, code)

    def test_login_get(self):
        url = reverse_lazy('login')
        code = self.client.get(url).status_code
        self.assertEqual(status.HTTP_200_OK, code)

    def test_chekout_get(self):
        url = reverse_lazy('checkout')
        code = self.client.get(url).status_code
        self.assertEqual(status.HTTP_200_OK, code)

    def test_fail_login(self):
        c = Client()
        response = c.post(reverse('login'), {'email': 'user6@gmail.com', 'password': 'qwerty'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_login(self):
        c = Client()
        response = c.post(reverse('signup'), {'firstname': 'aaaa', 'lastname': 'aaaa',
                                              'phone': '1234567890123', 'email': 'user123@gmail.com',
                                              'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        response = c.post(reverse('login'), {'email': 'user123@gmail.com', 'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_signup(self):
        c = Client()
        response = c.post(reverse('signup'), {'firstname': 'aaaa', 'lastname': 'aaaa',
                                              'phone': '1234567890123', 'email': 'user123@gmail.com',
                                              'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_fail_signup(self):
        c = Client()
        response = c.post(reverse('signup'), {'firstname': 'aaaa', 'lastname': 'aaaa',
                                              'phone': '1234567890123', 'email': 'user123@gmail.com',
                                              'password': ''})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_cart(self):
        c = Client()
        response = c.post(reverse('signup'), {'firstname': 'aaaa', 'lastname': 'aaaa',
                                              'phone': '1234567890123', 'email': 'user123@gmail.com',
                                              'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        response = c.post(reverse('login'), {'email': 'user123@gmail.com', 'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        response = c.post(reverse('cart'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_logout(self):
        c = Client()
        response = c.post(reverse('logout'))
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_checkout(self):
        c = Client()
        response = c.post(reverse('signup'), {'firstname': 'aaaa', 'lastname': 'aaaa',
                                              'phone': '1234567890123', 'email': 'user123@gmail.com',
                                              'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        response = c.post(reverse('login'), {'email': 'user123@gmail.com', 'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        response = c.post(reverse('checkout'), {'address': 'Minsk', 'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_homePage_post(self):
        c = Client()
        response = c.post(reverse('signup'), {'firstname': 'aaaa', 'lastname': 'aaaa',
                                              'phone': '1234567890123', 'email': 'user123@gmail.com',
                                              'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        response = c.post(reverse('login'), {'email': 'user123@gmail.com', 'password': 'qwerty'})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        a = Category.objects.create(name='a', slug='a')
        b = Category.objects.create(name='b', slug='b')
        d = Category.objects.create(name='d', slug='d')
        Game.objects.create(name='a', price=5, slug='a', content='a', photo='a', cat=a)
        Game.objects.create(name='b', price=5, slug='b', content='b', photo='b', cat=b)
        Game.objects.create(name='d', price=5, slug='d', content='d', photo='d', cat=d)
        response = c.post(path='/?category=3/', data={'product': 3})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
