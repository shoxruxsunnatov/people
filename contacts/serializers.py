from rest_framework.serializers import ModelSerializer

from contacts.models import Contact, Notification


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'fullname', 'info')


class NotificationSerializer(ModelSerializer):

    contact = ContactSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'contact', 'date_created')
