from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from cookprojectapi.views import RecipeViewSet, CategoryViewSet, FavoriteViewSet, ReviewViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', RecipeViewSet, 'recipe')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'favorites', FavoriteViewSet, 'favorite')
router.register(r'reviews', ReviewViewSet, 'review')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

