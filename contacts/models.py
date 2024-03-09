from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    info = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True)
    frequency = models.DurationField(null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    refresh = models.DateTimeField(null=True)

    class Meta:
        ordering = ['fullname']

    def __str__(self):
        return self.fullname
    

class Notification(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.contact.fullname
