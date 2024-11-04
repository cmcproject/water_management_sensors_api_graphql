from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=1000)

    class Meta:
        ordering = ["name"]
