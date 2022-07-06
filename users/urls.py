from django.urls import include, path
from rest_framework import routers
from . import apis
from knox import views as knox_views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/login/', apis.AdminLoginAPI.as_view()),
    path('api/auth/user/', apis.AuthUserAPI.as_view()),
    path('api/contact/', apis.ContactAPI.as_view()),
]
