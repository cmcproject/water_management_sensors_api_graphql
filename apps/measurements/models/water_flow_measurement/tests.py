import pytest

from .factory import WaterFlowMeasurementFactory
from .model import WaterFlowMeasurement

pytestmark = pytest.mark.django_db


def test_basic_WaterFlowMeasurement_factory():
    """Test WaterFlowMeasurement factory works correctly"""
    water_flow_measurement = WaterFlowMeasurementFactory.create()

    water_flow_measurement_from_db = WaterFlowMeasurement.objects.get(
        pk=water_flow_measurement.pk
    )

    assert water_flow_measurement == water_flow_measurement_from_db
