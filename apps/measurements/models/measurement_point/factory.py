import factory

from faker import Faker

from .model import MeasurementPoint
from apps.measurements.models.location.factory import LocationFactory

fake = Faker()


class MeasurementPointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MeasurementPoint

    location = factory.SubFactory(LocationFactory)
    name = factory.Sequence(lambda n: f"{fake.job()} Room #{n}")  # Avoid duplicates
