import datetime
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.db.models import Q
from django.dispatch import receiver

from base.models import ImageWithThumbnail


def title_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'house_%d.%s' % (datetime.datetime.now().timestamp(), ext)
    return os.path.join('images', filename)


THUMB_SIZE = (256, 256)


class House(models.Model):
    name = models.CharField(max_length=255)
    persons = models.PositiveSmallIntegerField()
    base_price = models.DecimalField(decimal_places=2, max_digits=8)
    title_image = models.ImageField(upload_to=title_image_path)
    thumbnail = models.ImageField()

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name', )

    @property
    def reservations(self):
        today = datetime.date.today()
        return self.bookings.filter(Q(date_from__gte=today))

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')
        super(House, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.title_image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        thumb_name = 'house_thumbnail_%d' % (datetime.datetime.now().timestamp(), )
        thumb_extension = os.path.splitext(self.title_image.name)[1].lower()

        thumb_filename = thumb_name + thumb_extension

        if thumb_extension in ('.jpg', '.jpeg'):
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(os.path.join('images', thumb_filename), ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


@receiver(models.signals.post_delete, sender=House, dispatch_uid='house_delete_signal')
def house_post_delete(sender, instance, using, **kwargs):
    if instance.title_image:
        try:
            os.remove(instance.title_image.path)
        except:
            pass

    if instance.thumbnail:
        try:
            os.remove(instance.thumbnail.path)
        except:
            pass


class HousePhoto(ImageWithThumbnail):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='photos')
    index = models.PositiveIntegerField()

    class Meta:
        # unique_together = (('house', 'index'), )
        ordering = ('index', )


class HouseReview(models.Model):
    rating = models.FloatField()
    person_name = models.CharField(max_length=128)
    content = models.TextField(max_length=1024)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )


class Booking(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='bookings')
    date_from = models.DateField()
    date_to = models.DateField()
    approved_by_manager = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_from', )

