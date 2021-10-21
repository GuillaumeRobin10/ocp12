"""
document avec tous les filters
"""
import django_filters.rest_framework as filters
from .models import Client, Contrat, Event


class Clientfilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr="icontains")
    company_name = filters.CharFilter(lookup_expr="icontains")
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")
    sales_admin = filters.CharFilter(lookup_expr="iexact")
    phone = filters.CharFilter(lookup_expr="icontains")
    mobile = filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Client
        fields = {
            'date_created': ["exact","year__gt"],
            "date_updated": ["exact","year__gt"],
            "Convert": ["exact"]
        }


class Contratfilter(filters.FilterSet):
    amont = filters.CharFilter(lookup_expr="icontains")
    status = filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Contrat
        fields = {
            "status": ["exact"],
            "amont" : ["lt",'gt'],
            "payment_due":["lt",'gt'],
            "date_created":["exact","year__gt"],
            "date_updated":["exact","year__gt"],
            "date_signature":["exact","year__gt"],
            "client_id":["exact"],
        }


class Eventfilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            "contrat": ["exact"],
            "note" : ["lt",'gt'],
            "attendees":["lt",'gt'],
            "date_created":["exact","year__gt"],
            "date_updated":["exact","year__gt"],
            "event":["exact","year__gt"],
            "support_contact":["exact"],
        }

