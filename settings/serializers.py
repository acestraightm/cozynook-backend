from rest_framework import serializers

from settings.models import CarouselImage


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ['id', 'index', 'image']
        read_only_fields = ['index']

