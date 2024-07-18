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
    
    def retrieve(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Recipe.DoesNotExist:
            return Response({"error": "Recipe id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.title = request.data.get('title', recipe.title)
            recipe.description = request.data.get('description', recipe.description)
            recipe.instructions = request.data.get('instructions', recipe.instructions)
            recipe.ingredients = request.data.get('ingredients', recipe.ingredients)
            recipe.time = request.data.get('time', recipe.time)
            

            category_ids = request.data.get('categories', [])
            if category_ids:
                recipe.categories.set(category_ids)

            recipe.save()

            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        
    def destroy(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe id does not exist"}, status=status.HTTP_404_NOT_FOUND)