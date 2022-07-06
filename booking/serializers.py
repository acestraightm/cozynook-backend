import datetime

from django.db.models import Avg, Q
from rest_framework import serializers

from booking.models import House, HousePhoto, Booking


class BookingSerializer(serializers.ModelSerializer):
    house_name = serializers.CharField(read_only=True, source='house.name')

    class Meta:
        model = Booking
        fields = ('id', 'house', 'date_from', 'date_to', 'approved_by_manager', 'house_name')
        extra_kwargs = {
            'date_from': {
                'input_formats': ['%Y-%m-%d'],
            },
            'date_to': {
                'input_formats': ['%Y-%m-%d'],
            }
        }


class HousePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousePhoto
        fields = ('id', 'image', 'thumbnail', 'index', )
        extra_kwargs = {
            'thumbnail': {'required': False},
        }


class HouseSerializer(serializers.ModelSerializer):
    photos = HousePhotoSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ('id', 'name', 'persons', 'base_price', 'title_image', 'thumbnail', 'photos', 'rating', 'reservations')
        extra_kwargs = {
            'thumbnail': {'required': False},
        }

    def get_rating(self, instance):
        avg_rating = instance.reviews.all().aggregate(Avg('rating'))
        return {
            'score': avg_rating['rating__avg'] if avg_rating else 0,
            'reviews': instance.reviews.count()
        }

    def get_reservations(self, instance):
        return BookingSerializer(instance.reservations.all(), many=True).data
