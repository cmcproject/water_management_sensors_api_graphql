import pytz
import factory

from faker import Faker

from apps.measurements.models.measurement_point.factory import MeasurementPointFactory
from .model import WaterFlowMeasurement

fake = Faker()


class WaterFlowMeasurementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WaterFlowMeasurement

    measurement_point = factory.SubFactory(MeasurementPointFactory)

    timestamp = factory.LazyFunction(
        lambda: pytz.utc.localize(
            fake.date_time_between(start_date="-1y", end_date="-1d")
        )
    )
    duration_ms = factory.Faker("pyint", min_value=1, max_value=9999999)
    volume_ml = factory.Faker("pyint", min_value=1, max_value=9999999)

    temperature_min_celsius = factory.Faker("pyint", min_value=0, max_value=99)
    temperature_avg_celsius = factory.Faker("pyint", min_value=0, max_value=99)
    temperature_max_celsius = factory.Faker("pyint", min_value=0, max_value=99)
