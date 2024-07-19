from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from cookprojectapi.models import *
from cookprojectapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', RecipeViewSet, 'recipe')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'favorites', FavoriteViewSet, 'favorite')
router.register(r'reviews', ReviewViewSet, 'review')
router.register(r'users', Users, 'user')
router.register(r'pictures', PictureViewSet, 'picture')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

