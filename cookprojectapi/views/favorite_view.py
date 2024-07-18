from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from cookprojectapi.models import Favorite, Customer, Recipe

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'customer_id', 'recipe_id']

class FavoriteViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        favorites = Favorite.objects.all()

        customer_id = self.request.query_params.get('customer', None)
        recipe_id = self.request.query_params.get('recipe', None)

        if customer_id is not None:
            favorites = favorites.filter(customer__id=customer_id)
            serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if recipe_id is not None:
            favorites = favorites.filter(recipe__id=recipe_id)
            serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        # Extract data from request
        customer_id = request.data.get('customer')
        recipe_id = request.data.get('recipe')

        # Ensure customer and recipe IDs are provided
        if not customer_id or not recipe_id:
            return Response({"error": "Both customer and recipe must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the customer and recipe exist
        try:
            customer = Customer.objects.get(id=customer_id)
            recipe = Recipe.objects.get(id=recipe_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the favorite already exists
        if Favorite.objects.filter(customer=customer, recipe=recipe).exists():
            return Response({"error": "This favorite already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the Favorite instance
        favorite = Favorite.objects.create(
            customer=customer,
            recipe=recipe
        )

        # Serialize and return
        serializer = FavoriteSerializer(favorite, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(pk=pk)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Favorite.DoesNotExist:
            return Response({"error": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)