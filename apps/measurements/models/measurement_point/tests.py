import pytest

from .factory import MeasurementPointFactory
from .model import MeasurementPoint

pytestmark = pytest.mark.django_db


def test_basic_measurement_point_factory():
    """Test MeasurementPoint factory works correctly"""
    measurement_point = MeasurementPointFactory.create()

    measurement_point_from_db = MeasurementPoint.objects.get(pk=measurement_point.pk)

    assert measurement_point == measurement_point_from_db
