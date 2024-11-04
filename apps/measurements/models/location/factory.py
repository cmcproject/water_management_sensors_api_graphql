import factory

from faker import Faker

from .model import Location

fake = Faker()


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f"{fake.company()} - {n}")  # Avoid duplicates
    address = factory.Faker("address")
