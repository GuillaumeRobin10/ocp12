from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):

    sales_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_admin")
    company_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    Convert = models.BooleanField(default=False)

    @staticmethod
    def get_client_by_id(identity):
        return Client.objects.get(id__in=identity)


class Contrat(models.Model):
    status = models.BooleanField(default=False)
    amont = models.FloatField(null=True)
    payment_due = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_signature = models.DateTimeField(null=True, blank=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client")

    @staticmethod
    def get_contrat_by_id(identity):
        return Contrat.objects.get(id__in=identity)


class Event(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name="contrat")
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Support_contact")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    event = models.DateTimeField(auto_now_add=False)
    note = models.TextField(max_length=1000)
    attendees = models.IntegerField(null=True)
