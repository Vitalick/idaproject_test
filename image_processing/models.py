from io import BytesIO

from PIL import Image as PIL_Image
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse


class Image(models.Model):
    file = models.ImageField('файл изображения', upload_to='originals')
    thumbnail = models.ImageField('превью изображения', blank=True, upload_to='thumbnails')
    width = models.PositiveIntegerField('ширина', default=100)
    height = models.PositiveIntegerField('высота', default=100)

    def __str__(self):
        return self.file.name.split('/')[-1]

    def get_absolute_url(self):
        return reverse('image_detail', kwargs={'pk': self.id})

    def get_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        return self.file.url
