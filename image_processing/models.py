from django.db import models

# Create your models here.
from django.urls import reverse


class Image(models.Model):
    file = models.ImageField('файл изображения')

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('image_detail', kwargs={'pk': self.id})
