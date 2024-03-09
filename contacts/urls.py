from django.urls import path

from contacts.views import (
    ContactsView,
    ContactDetailView
)


app_name = 'contacts'

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
]