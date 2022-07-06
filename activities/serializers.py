from rest_framework import serializers

from activities.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'base_price', 'image', 'description')
