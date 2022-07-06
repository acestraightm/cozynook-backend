from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from settings.models import CarouselImage
from settings.serializers import CarouselImageSerializer


class CarouselViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CarouselImageSerializer
    queryset = CarouselImage.objects.all()
    # parser_classes = (MultiPartParser, )

    def create(self, request, *args, **kwargs):
        carousel_item = CarouselImage()
        carousel_item.image = request.FILES['image']
        carousel_item.index = CarouselImage.objects.count()
        carousel_item.save()
        return Response('Success')

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

    # def destroy(self, request, *args, **kwargs):
    #     carousel_item = self.get_object()
    #     carousel_item.delete()
    #
    #     return Response('Success')

    @action(methods=['post'], detail=True, url_path='up')
    def index_up(self, request, *args, **kwargs):
        item = self.get_object()
        if item.index > 0:
            item1 = get_object_or_404(CarouselImage, index=item.index - 1)
            item1.index = CarouselImage.objects.count()
            item1.save()

            item.index = item.index - 1
            item.save()
            item1.index = item.index + 1
            item1.save()

        return Response('Success')

    @action(methods=['post'], detail=True, url_path='down')
    def index_down(self, request, *args, **kwargs):
        item = self.get_object()
        if item.index < CarouselImage.objects.count() - 1:
            item1 = get_object_or_404(CarouselImage, index=item.index + 1)
            item1.index = CarouselImage.objects.count()
            item1.save()

            item.index = item.index + 1
            item.save()
            item1.index = item.index - 1
            item1.save()

        return Response('Success')
