from django.db import models


class Image(models.Model):
    """Image's model class"""
    title = models.CharField(max_length=255, blank=False, null=False)
    width = models.PositiveIntegerField(blank=True)
    height = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to="images/", blank=False, null=False)
