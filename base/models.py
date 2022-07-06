import datetime
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models

# Create your models here.
from django.dispatch import receiver

from cozynook.settings import THUMB_SIZE


def image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'image_%d.%s' % (datetime.datetime.now().timestamp(), ext)
    return os.path.join('images', filename)


class ImageWithThumbnail(models.Model):
    image = models.ImageField(upload_to=image_path)
    thumbnail = models.ImageField()

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')
        super(ImageWithThumbnail, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        thumb_name = 'thumbnail_%d' % (datetime.datetime.now().timestamp(), )
        thumb_extension = os.path.splitext(self.image.name)[1].lower()

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


@receiver(models.signals.post_delete, sender=ImageWithThumbnail, dispatch_uid='image_with_thumbnail_delete_signal')
def image_with_thumbnail_post_delete(sender, instance, using, **kwargs):
    if instance.image:
        try:
            os.remove(instance.image.path)
        except:
            pass

    if instance.thumbnail:
        try:
            os.remove(instance.thumbnail.path)
        except:
            pass