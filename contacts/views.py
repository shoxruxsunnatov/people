from datetime import datetime, timedelta, timezone

from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.shortcuts import redirect

from contacts.serializers import (
    ContactSerializer,
    NotificationSerializer
)

from contacts.models import (
    Contact,
    Notification
)


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class ContactsView(TemplateView):
    template_name = 'contacts.html'


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class NotificationsView(TemplateView):
    template_name = 'notifications.html'


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class ContactDetailView(TemplateView):
    template_name = 'contact_detail.html'

    def get(self, req, *args, **kwargs):
        self.contact = Contact.objects.filter(id=kwargs.get('pk')).first()

        if not self.contact:
            return redirect('contacts:contacts')
        
        return super().get(req, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contact'] = self.contact
        return context


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class ContactsAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):
        fullname = req.POST.get('fullname', '').strip()
        info = req.POST.get('info', '').strip()
        birthday = req.POST.get('birthday', '').strip()
        frequency = req.POST.get('frequency', '').split('_')

        if fullname:
            data = {
                'user': req.user,
                'fullname': fullname,
                'info': info,
                'refresh': datetime.now()
            }

            if birthday:
                data['birthday'] = datetime.strptime(birthday, "%Y-%m-%d")
            
            if len(frequency) == 3:
                data['frequency'] = timedelta(
                    days=int(frequency[0]),
                    hours=int(frequency[1]),
                    minutes=int(frequency[2])
                )

            contact = Contact(**data)
            contact.save()

            return JsonResponse({
                'fullname': fullname,
                'info': info,
                'birthday': birthday,
                'frequency': frequency
            }, safe=False)

        return JsonResponse({'message': 'failed'}, safe=False)
    
    def get(self, req, *args, **kwargs):

        serializer = ContactSerializer(
            Contact.objects.filter(user=req.user).order_by('fullname'),
            many=True
        )

        return JsonResponse(serializer.data, safe=False)


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class ContactDetailAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):
        contact = Contact.objects.filter(id=kwargs.get('pk')).first()

        if not contact:
            return JsonResponse({'message': 'Not found'}, safe=False)
        
        fullname = req.POST.get('fullname', '').strip()
        info = req.POST.get('info', '').strip()
        birthday = req.POST.get('birthday', '').strip()
        frequency = req.POST.get('frequency', '').split('_')

        if fullname:

            contact.fullname = fullname
            contact.info = info

            if birthday:
                contact.birthday = datetime.strptime(birthday, "%Y-%m-%d")
            
            if len(frequency) == 3:
                new_requency = timedelta(
                    days=int(frequency[0]),
                    hours=int(frequency[1]),
                    minutes=int(frequency[2])
                )
                if new_requency != contact.frequency:
                    contact.frequency = new_requency
                    contact.refresh = datetime.now()

            contact.save()

            return JsonResponse({
                'fullname': fullname,
                'info': info,
                'birthday': birthday,
                'frequency': frequency
            }, safe=False)

        return JsonResponse({'message': 'failed'}, safe=False)
    
    def get(self, req, *args, **kwargs):
        contact = Contact.objects.filter(id=kwargs.get('pk')).first()

        if not contact:
            return JsonResponse({'message': 'Not found'}, safe=False)

        data = {
            'id': contact.id,
            'fullname': contact.fullname,
            'info': contact.info
        }

        if contact.birthday:
            data['birthday'] = contact.birthday.strftime('%Y-%m-%d')

        if contact.frequency:
            data['frequency'] = [
                contact.frequency.days,
                contact.frequency.seconds // 3600,
                (contact.frequency.seconds % 3600) // 60
            ]

        return JsonResponse(data, safe=False)

    def delete(self, req, *args, **kwargs):
        contact = Contact.objects.filter(id=kwargs.get('pk')).first()

        if not contact:
            return JsonResponse({'message': 'Not found'}, safe=False)
        
        contact.delete()

        return JsonResponse({'message': 'success'}, safe=False)


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class NotificationsAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):
        pass
    
    def get(self, req, *args, **kwargs):
        contacts = Contact.objects.filter(user=req.user, frequency__gt=timedelta())
        now = datetime.now(tz=timezone.utc)

        for contact in contacts:
            if contact.refresh + contact.frequency < now:
                Notification(
                    user=req.user,
                    contact=contact,
                ).save()
                contact.refresh = now
                contact.save()

        serializer = NotificationSerializer(
            Notification.objects.filter(user=req.user, seen=False),
            many=True
        )

        return JsonResponse(serializer.data, safe=False)


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class NotificationsContactDetailAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def get(self, req, *args, **kwargs):
        contact = Contact.objects.filter(id=kwargs.get('pk')).first()

        if not contact:
            return JsonResponse({'message': 'Not found'}, safe=False)
        
        now = datetime.now(tz=timezone.utc)

        if contact.frequency and contact.refresh + contact.frequency < now:
            Notification(
                user=req.user,
                contact=contact,
            ).save()
            contact.refresh = now
            contact.save()

        serializer = NotificationSerializer(
            Notification.objects.filter(user=req.user, contact=contact),
            many=True
        )

        return JsonResponse(serializer.data, safe=False)


@method_decorator(login_required(login_url='main:register'), name='dispatch')
class NotificationDetailAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):
        notification = Notification.objects.filter(id=kwargs.get('pk')).first()

        if not notification:
            return JsonResponse({'message': 'Not found'}, safe=False)
        
        notification.seen = True
        notification.save()

        return JsonResponse({'message': 'success'}, safe=False)


    def delete(self, req, *args, **kwargs):
        notification = Notification.objects.filter(id=kwargs.get('pk')).first()

        if not notification:
            return JsonResponse({'message': 'Not found'}, safe=False)
        
        notification.delete()

        return JsonResponse({'message': 'success'}, safe=False)
