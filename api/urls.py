from django.urls import path

from api.views import (
    RegisterViewAPI,
    LoginViewAPI,
    AllNotificationsAPI
)
from contacts.views import (
    ContactsAPI,
    ContactDetailAPI,
    NotificationsAPI,
    NotificationsContactDetailAPI,
    NotificationDetailAPI
)


app_name = 'api'

urlpatterns = [
    path('register/', RegisterViewAPI.as_view(), name='register'),
    path('login/', LoginViewAPI.as_view(), name='login'),
    path('contacts/', ContactsAPI.as_view(), name='contacts'),
    path('contacts/<int:pk>/', ContactDetailAPI.as_view(), name='contact_detail'),
    path('contacts/<int:pk>/notifications/', NotificationsContactDetailAPI.as_view(), name='notifications_detail'),
    path('notifications/', NotificationsAPI.as_view(), name='notifications'),
    path('notifications/<int:pk>/', NotificationDetailAPI.as_view(), name='notification_detail'),
    path('createallnotifications/', AllNotificationsAPI.as_view(), name='allnotifications')
]