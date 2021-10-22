from django.contrib import admin
from .models import Client, Event, Contrat


class ClientAdmin(admin.ModelAdmin):
    list_display = ('sales_admin', "company_name", "first_name", 'last_name', "email", "phone", 'mobile', "date_created", "date_updated", "Convert")


class EventAdmin(admin.ModelAdmin):
    list_display = ('contrat', "support_contact", "date_created", 'event', "date_updated", "note", 'attendees')


class ContratAdmin(admin.ModelAdmin):
    list_display = ('status', "amont", "payment_due", 'date_created', "date_updated", "date_signature", 'client_id')


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contrat, ContratAdmin)
