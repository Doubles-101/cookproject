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
    
    def retrieve(self, request, pk=None):
        customers = Customer.objects.get(id=pk)

        serializer = CustomerSerializer(customers, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        
        try:
            customer = Customer.objects.get(pk=pk, user=request.auth.user)
            customer.user.last_name = request.data["last_name"]
            customer.user.email = request.data["email"]
            customer.address = request.data["address"]
            customer.phone_number = request.data["phone_number"]
            customer.user.save()
            customer.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Customer.DoesNotExist:
            return Response({"error": "Customer may not exists. Check if you have permission, or correct id"}, status=status.HTTP_400_BAD_REQUEST)