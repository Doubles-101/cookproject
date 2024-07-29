from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from cookprojectapi.models import Review, RecipeImage
import uuid
import base64
from django.core.files.base import ContentFile

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = '__all__'

class PictureViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        pass

    def retrieve(self, request, pk=None):
        try:
            picture = RecipeImage.objects.get(recipe_id=pk)
            serializer = PictureSerializer(picture, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except RecipeImage.DoesNotExist:
            return Response({"error": "Recipe Image id does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            recipe_picture = RecipeImage()
            recipe_id = request.data.get("recipe_id")
            recipe_image = request.data.get("recipe_image")

            format, imgstr = recipe_image.split(';base64,')
            imgstr += "=="
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'{recipe_id}-{uuid.uuid4()}.{ext}')

            recipe_picture.recipe_pic = image_data
            recipe_picture.recipe_id = request.data.get("recipe_id")


            recipe_picture.save()

            serializer = PictureSerializer(recipe_picture)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
 