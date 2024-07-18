from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db.models import Q
from cookprojectapi.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'ingredients', 'time', 'customer']



class RecipeViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)