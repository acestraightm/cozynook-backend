from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response

from users.serializers import LoginSerializer, UserSerializer


class AdminLoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if not user.is_staff:
            return Response('Non-staff are not allowed to access the admin.', status=403)

        token = AuthToken.objects.create(user)[1]

        return Response({
            'token': token,
            'user': UserSerializer(instance=user).data,
            'role': 'admin',
            'type': 'account',
            'status': 'ok',
        })


class AuthUserAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(instance=request.user).data,
            'role': 'admin',
            'type': 'account',
        })


class ContactAPI(generics.GenericAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return Response('')

