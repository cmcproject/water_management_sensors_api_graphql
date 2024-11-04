from apps.measurements.models.measurement_point.model import MeasurementPoint
from django.db import models


class WaterFlowMeasurement(models.Model):
    measurement_point = models.ForeignKey(
        MeasurementPoint,
        on_delete=models.PROTECT,
        related_name="water_flow_measurements",
    )

    timestamp = models.DateTimeField()
    duration_ms = models.IntegerField()
    volume_ml = models.PositiveBigIntegerField()

    temperature_min_celsius = models.IntegerField()
    temperature_avg_celsius = models.IntegerField()
    temperature_max_celsius = models.IntegerField()
