import datetime
import os

from django.db import models


def activity_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'activity_%d.%s' % (datetime.datetime.now().timestamp(), ext)
    return os.path.join('images', filename)


class Activity(models.Model):
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(decimal_places=2, max_digits=8)
    image = models.ImageField(upload_to=activity_image_path)
    description = models.TextField(max_length=1500)

    class Meta:
        ordering = ('id', )
