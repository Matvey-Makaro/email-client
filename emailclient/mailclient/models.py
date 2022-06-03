from django.db import models


class User(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    registration_time = models.DateTimeField(auto_now_add=True)


