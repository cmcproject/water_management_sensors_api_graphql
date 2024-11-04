import pytest

from .factory import LocationFactory
from .model import Location

pytestmark = pytest.mark.django_db


def test_basic_location_factory():
    """Test location factory works correctly"""
    location = LocationFactory.create()

    location_from_db = Location.objects.get(pk=location.pk)

    assert location == location_from_db
