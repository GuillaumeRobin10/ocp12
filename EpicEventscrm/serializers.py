from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Client, Contrat, Event


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('sales_admin', "company_name", "first_name", 'last_name', "email", "phone", 'mobile', "Convert", "date_created", "date_updated")
        extra_kwargs = {
            'sales_admin': {'required': False},
            'Convert': {'required': False},
            'date_created': {'required': False},
            'date_updated': {'required': False},
        }

    def create(self, validated_data, user):
        client = Client.objects.create(
            sales_admin=user,
            company_name=validated_data['company_name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            mobile=validated_data['mobile'],
        )
        client.save()
        return client


class ClientSerializerupdate(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('sales_admin', "company_name", "first_name", 'last_name', "email", "phone", 'mobile', "Convert", "date_created", "date_updated")
        extra_kwargs = {
            'sales_admin': {'required': False},
            'company_name': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'mobile': {'required': False},
            'Convert': {'required': False},
            'date_created': {'required': False},
            'date_updated': {'required': False},
        }


class ContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = ('status', "amont", "payment_due", 'date_created', "date_updated", "date_signature", 'client_id')
        extra_kwargs = {
            'date_signature': {'required': False},
            'date_created': {'required': False},
            'date_updated': {'required': False},
        }


class ContratupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = ('status', "amont", "payment_due", "date_updated", "date_signature")
        extra_kwargs = {
            'status': {'required': False},
            'amont': {'required': False},
            'payment_due': {'required': False},
            'date_signature': {'required': False},
            'date_updated': {'required': False},
        }


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('contrat', "support_contact", "date_created", 'event', "date_updated", "note", 'attendees')

        extra_kwargs = {
            'date_created': {'required': False},
            'date_updated': {'required': False},
        }


class EventSerializerupdate(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event', "date_updated", "note", 'attendees')

        extra_kwargs = {
            'event': {'required': False},
            'date_updated': {'required': False},
            'note': {'required': False},
            'attendees': {'required': False},

        }


class CreateUserSerializer(serializers.ModelSerializer):
    """
    serializer
    use to create a new user
    didn't return the password 'cause of the write_of parameters
    method create, add and save a new user in db
    """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
