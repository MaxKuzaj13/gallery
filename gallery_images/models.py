from django.db import models


class GalleryImage(models.Model):
    index = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='gallery_images/')
