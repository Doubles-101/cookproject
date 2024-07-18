from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from cookprojectapi.models import Review

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