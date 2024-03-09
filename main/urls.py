from django.urls import path

from main.views import (
    RegisterView,
    HomeView,
    CustomLogoutView,
    AboutView,
    service_worker_view,
    send_push_notification
)
from contacts.views import (
    NotificationsView
)


app_name = 'main'

urlpatterns = [
    path('', NotificationsView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('log-out/', CustomLogoutView.as_view(), name='log-out'),
    path('about/', AboutView.as_view(), name='about'),

    path('service-worker', service_worker_view, name='hand_scope'),
    path('subscribe/', send_push_notification, name='push_notification'),
]