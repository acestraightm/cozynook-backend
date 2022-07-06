from django.urls import include, path
from rest_framework import routers

from . import apis

router = routers.DefaultRouter()
router.register('api/booking/houses', apis.HouseViewSet)
router.register('api/booking/bookings', apis.BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
