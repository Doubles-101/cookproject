from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from cookprojectapi.models import Review, Customer, Recipe
from django.utils import timezone

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'customer_id', 'recipe_id', 'comment', 'create_date']

class ReviewViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        reviews = Review.objects.all()

        customer_id = self.request.query_params.get('customer', None)
        recipe_id = self.request.query_params.get('recipe', None)

        if customer_id is not None:
            reviews = reviews.filter(customer__id=customer_id)
            serializer = ReviewSerializer(reviews, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if recipe_id is not None:
            reviews = reviews.filter(recipe__id=recipe_id)
            serializer = ReviewSerializer(reviews, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):

        customer_id = request.data.get('customer')
        recipe_id = request.data.get('recipe')
        comment = request.data.get('comment')
        create_date = timezone.now().date()

        
        if not customer_id or not recipe_id or not comment:
            return Response({"error": "Customer, recipe, and comment must be provided."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            customer = Customer.objects.get(id=customer_id)
            recipe = Recipe.objects.get(id=recipe_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe does not exist."}, status=status.HTTP_404_NOT_FOUND)


        review = Review.objects.create(
            customer=customer,
            recipe=recipe,
            comment=comment,
            create_date=create_date
        )

        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Review.DoesNotExist:
            return Response({"error": "Review is not found."}, status=status.HTTP_404_NOT_FOUND)