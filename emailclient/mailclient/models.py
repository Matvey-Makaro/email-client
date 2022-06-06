from django.contrib.auth.models import AbstractUser
from django.db import models
from pkg_resources import _


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class Mailbox(models.Model):
    address = models.EmailField()
    password = models.CharField(_('password'), max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailboxes')


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    sender = models.ForeignKey(Mailbox, on_delete=models.CASCADE, related_name='emails_sender')
    # recipients = models.ManyToManyField(Mailbox, related_name='emails_received')
    recipients = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def serialize(self):
        return {
            'id': self.id,
            'sender': self.sender.email,
            'recipients': [user.email for user in self.recipients.all()],
            'subject': self.subject,
            'body': self.body,
            'timestamp': self.timestamp.strftime('%b %d %Y, %I:%M %p'),
            'read': self.read,
            'archived': self.archived
        }





