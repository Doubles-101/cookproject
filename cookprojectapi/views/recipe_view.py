from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db.models import Q
from cookprojectapi.models import Recipe
from .category_view import CategorySerializer
from cookprojectapi.models import Customer


class RecipeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'ingredients', 'time', 'customer', 'categories']



class RecipeViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        try:
            search_text = self.request.query_params.get('q', None)
            sorting_text = self.request.query_params.get('orderby', None)
            #probably add a way to sort by specific categories in the future

            if search_text is None and sorting_text is None:
                recipes = Recipe.objects.all()
                serializer = RecipeSerializer(recipes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif search_text is not None:
                recipes = Recipe.objects.filter(
                    Q(title__contains=search_text) |
                    Q(description__contains=search_text) |
                    Q(time__contains=search_text) 
                )
                serializer = RecipeSerializer(recipes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif sorting_text == "time":
                recipes = Recipe.objects.all().order_by('time')
                serializer = RecipeSerializer(recipes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
    
            elif sorting_text == "title":
                recipes = Recipe.objects.all().order_by('title')
                serializer = RecipeSerializer(recipes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": "invalid sorting parameter"}, status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

            if recipe.customer.user != request.user:
                return Response({"error": "You do not have permission to delete this recipe."}, status=status.HTTP_403_FORBIDDEN)

            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        # Grabs the data from client request
        title = request.data.get('title')
        description = request.data.get('description')
        instructions = request.data.get('instructions')
        ingredients = request.data.get('ingredients')
        time = request.data.get('time')

        # Make sure the user is authenticated// Optional here
        if not request.user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the customer associated with the authenticated user
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Actually saves information to database
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            instructions=instructions,
            ingredients=ingredients,
            time=time,
            customer=customer
            )

        # Establish the many-to-many relationships, and set the information if available
        category_ids = request.data.get('categories', [])
        if category_ids:
            recipe.categories.set(category_ids)

        # Serialize then return a response
        serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)