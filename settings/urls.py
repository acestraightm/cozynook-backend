from django.urls import include, path
from rest_framework import routers

from . import apis

router = routers.DefaultRouter()
router.register('api/settings/carousel-images', apis.CarouselViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
