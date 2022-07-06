from django.urls import include, path
from rest_framework import routers

from . import apis

router = routers.DefaultRouter()
router.register('api/activities', apis.ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
