from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
import datetime
from django.contrib.auth.models import User

from .filter import Clientfilter, Contratfilter, Eventfilter
from .models import Client, Contrat, Event
from .serializers import ClientSerializer, ContratSerializer, EventSerializer, ClientSerializerupdate, ContratupdateSerializer, EventSerializerupdate
from .serializers import CreateUserSerializer
from .permission import allowed_users


class Signup(APIView):
    """
    requete pour la création de compte.
    """
    @staticmethod
    def post(request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)


class ClientGeneral(generics.ListAPIView):
    """
    request get and post for client
    """
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_class = Clientfilter

    @staticmethod
    def post(request):
        if allowed_users(request.user,["ventes","gestion"]):
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(request.data, request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("forbidden access",status=status.HTTP_403_FORBIDDEN)


class ContratGeneral(generics.ListAPIView):
    """
     request get and post for Contrat
    """
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer
    filterset_class = Contratfilter
    @staticmethod
    def post(request):
        if allowed_users(request.user, ["ventes","gestion"]):
            serializer = ContratSerializer(data = request.data)
            if serializer.is_valid():
                client = Client.get_client_by_id(request.data["client_id"])
                contrat = Contrat.objects.create(
                status=request.data['status'],
                amont=request.data['amont'],
                payment_due=request.data['payment_due'],
                client_id=client
                )
                contrat.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response("forbidden access", status=status.HTTP_403_FORBIDDEN)


class EventGeneral(generics.ListAPIView):
    """
    request get and post for Events
    """
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = Eventfilter
    @staticmethod
    def post(request):
        if allowed_users(request.user, ["ventes","gestion"]):
            serializer = EventSerializer(data = request.data)
            if serializer.is_valid():
                contrat = Contrat.get_contrat_by_id(request.data["contrat"])
                user = User.objects.get(id__in=request.data["support_contact"])
                event = Event.objects.create(
                contrat=contrat,
                support_contact=user,
                event=request.data['event'],
                note=request.data['note'],
                attendees = request.data['attendees'],
                )
                event.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        return Response("forbidden access", status=status.HTTP_403_FORBIDDEN)


class ClientUnique(APIView):
    """
    crud method for a client
    """
    permission_classes = (IsAuthenticated,)
    @staticmethod
    def get_object(request,pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        client = self.get_object(request,pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(request, pk)
        if request.user == client.sales_admin:
            serializer = ClientSerializerupdate(client, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    def delete(self, request, pk):
        client = self.get_object(request, pk)
        if request.user == client.sales_admin:
            client.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            raise PermissionDenied


class ContratUnique(APIView):

    permission_classes = (IsAuthenticated,)
    @staticmethod
    def get_object(pk):
        try:
            return Contrat.objects.get(pk=pk)
        except Contrat.DoesNotExist:
            raise Http404

    def get(self, pk):
        contrat = self.get_object(pk)
        serializer = ContratSerializer(contrat)
        return Response(serializer.data)

    def put (self, request, pk):
        contrat = self.get_object(pk)
        if request.user == contrat.client_id:
            serializer = ContratupdateSerializer(contrat, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    def delete (self, request, pk):
        contrat = self.get_object(pk)
        if request.user == contrat.client_id:
            contrat.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventUnique(APIView):
    permission_classes = (IsAuthenticated,)
    @staticmethod
    def get_object(pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self,pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put (self, request, pk):
        event = self.get_object(pk)
        if request.user == event.support_contact:
            if event.event < datetime.datetime.now():

                serializer = EventSerializerupdate(event, request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete (self,request, pk):
        event = self.get_object(pk)
        if request.user == event.support_contact:
            event.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)