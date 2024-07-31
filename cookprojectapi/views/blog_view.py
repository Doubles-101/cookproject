from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from cookprojectapi.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        blog = Blog.objects.all()
        serializer = BlogSerializer(blog, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            blog = Blog.objects.get(id=pk)
            serializer = BlogSerializer(blog, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Blog.DoesNotExist:
            return Response({"error": "Blog id does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        pass
 