from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return get_object_or_404(User, pk=user.id)
        raise serializers.ValidationError("Incorrect Credentials")


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'name')

    def get_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'
