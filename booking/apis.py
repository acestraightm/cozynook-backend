from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from booking.models import House, HousePhoto, Booking
from booking.serializers import HouseSerializer, BookingSerializer
from cozynook.pagination import MainPagination


class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    pagination_class = MainPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(title_image=request.FILES['title_image'])
        return Response('Success')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if ('title_image' in request.FILES) and request.FILES['title_image']:
            serializer.save(title_image=request.FILES['title_image'])
        else:
            serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='photos', parser_classes=(MultiPartParser, ))
    def update_photos(self, request, *args, **kwargs):
        house = self.get_object()

        old_photos = request.POST
        new_photos = request.FILES
        num_fields = len(old_photos) + len(new_photos)

        old_ids = [int(house_id) for _, house_id in old_photos.items()]
        for photo in house.photos.all():
            if photo.id not in old_ids:
                photo.delete()

        for i in range(num_fields):
            key = str(i)
            if key in old_photos:
                try:
                    photo = house.photos.get(id=old_photos[key])
                except HousePhoto:
                    continue
                photo.index = i
                photo.save()
            elif key in new_photos:
                photo = HousePhoto()
                photo.image = new_photos[key]
                photo.index = i
                photo.house_id = house.id
                photo.save()

        return Response('Success')

    @action(methods=['get'], detail=False, url_path='fetch', permission_classes=[])
    def fetch(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    pagination_class = MainPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Success')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='fetch', permission_classes=[])
    def fetch(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
