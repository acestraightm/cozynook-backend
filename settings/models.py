import datetime
import os

from django.db import models
from django.dispatch import receiver


def carousel_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'carousel_%d.%s' % (datetime.datetime.now().timestamp(), ext)
    return os.path.join('images', filename)


class CarouselImage(models.Model):
    index = models.PositiveSmallIntegerField(unique=True)
    image = models.ImageField(upload_to=carousel_picture_path)

    class Meta:
        ordering = ('index', )


@receiver(models.signals.post_delete, sender=CarouselImage, dispatch_uid='carousel_image_delete_signal')
def carousel_image_post_delete(sender, instance, using, **kwargs):
    if instance.image:
        try:
            os.remove(instance.image.path)
        except:
            pass

    index = 0
    for item in CarouselImage.objects.all():
        item.index = index
        item.save()

        index += 1
