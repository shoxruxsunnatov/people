from django.contrib import admin

from contacts.models import Contact, Notification

admin.site.register(Contact)
admin.site.register(Notification)