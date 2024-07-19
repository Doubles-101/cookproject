from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from cookprojectapi.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers"""
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer', lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'phone_number', 'address')
        depth = 1


class Customers(ViewSet):

    def list(self, request):
        customers = Customer.objects.all()

        serializer = CustomerSerializer(customers, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass