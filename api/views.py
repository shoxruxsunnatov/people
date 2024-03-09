from datetime import timedelta, timezone, datetime

from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from contacts.models import (
    Contact,
    Notification
)


class RegisterViewAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):

        username = req.POST.get('username', '').strip().lower()
        password = req.POST.get('password', '').strip()
        fullname = req.POST.get('fullname', '')
        password_repeat = req.POST.get('password_repeat')

        errors = []

        if len(password) < 8:
            errors.append('password')
        
        if password != password_repeat:
            errors.append('password-repeat')

        if not 2 < len(fullname) < 50:
            errors.append('fullname')
        
        if not 2 < len(username) < 30 or User.objects.filter(username=username).first():
            errors.append('username')

        if errors:
            return JsonResponse({'errors': errors}, safe=False)
        else:
            user = User.objects.create(
                username=username,
                is_staff=True
            )
            user.set_password(password)
            user.save()
            login(req, user)

            return JsonResponse({'message': 'success', 'errors': errors})                


class LoginViewAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):

        username = req.POST.get('username', '').strip().lower()
        password = req.POST.get('password', '')
        
        user = authenticate(username=username, password=password)
        if user:
            login(req, user)

            return JsonResponse({'message': 'success'})
                
        return JsonResponse({'message': 'failed'})


class AllNotificationsAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):
        contacts = Contact.objects.filter( frequency__gt=timedelta())
        now = datetime.now(tz=timezone.utc)

        for contact in contacts:
            if contact.frequency and contact.refresh + contact.frequency < now:
                Notification(
                    user=contact.user,
                    contact=contact,
                ).save()
                contact.refresh = now
                contact.save()
        
        return JsonResponse({'message': 'success', 'reminders': contacts.count()}, safe=False)
