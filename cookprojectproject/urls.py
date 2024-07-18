from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from cookprojectapi.views import RecipeViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', RecipeViewSet, 'game')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

