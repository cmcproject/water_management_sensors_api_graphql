from django.db import models

from apps.measurements.models import Location


class MeasurementPoint(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="points"
    )
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        unique_together = (
            "location",
            "name",
        )
