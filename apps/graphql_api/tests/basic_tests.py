import pytz

from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_relay import to_global_id
from datetime import datetime, timedelta

from apps.measurements.models.measurement_point.factory import MeasurementPointFactory
from apps.measurements.models.location.factory import LocationFactory
from .results import all_locations_result, location_result
from apps.measurements.models import measurement_point
from apps.measurements.models.water_flow_measurement.factory import (
    WaterFlowMeasurementFactory,
)


class GraphQLApiBasicTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="test")

        # SETUP DATA FOR THE TESTS
        self.start = pytz.utc.localize(datetime(2022, 1, 2))
        self.end = pytz.utc.localize(datetime(2022, 1, 3))

        self.locations = []
        value = 0
        for i in range(10):
            location = LocationFactory.create(
                name=f"Location {i}", address=f"Address {i}"
            )
            self.locations.append(location)

            for j in range(10):
                number = i * 100 + j
                mp = MeasurementPointFactory.create(
                    location=location, name=f"Point {number}"
                )

                current = self.start
                while current < self.end:
                    value += 1
                    if value > 80:
                        value = 1
                    WaterFlowMeasurementFactory.create(
                        measurement_point=mp,
                        timestamp=current,
                        duration_ms=value * 10,
                        volume_ml=value * 20,
                        temperature_min_celsius=value - 1,
                        temperature_avg_celsius=value,
                        temperature_max_celsius=value + 1,
                    )

                    current += timedelta(hours=1)

        self.client.authenticate(self.user)

    def test_query_locations(self):
        query = """
            query AllLocations {
                allLocations {
                    edges {
                        node {
                            name
                            address
                        }
                    }
                }
            }
        """

        variables = {}
        result = self.client.execute(query, variables)

        assert result.data == all_locations_result

    def test_query_specific_location(self):
        query = """
        query Location ($locationId: ID!, $start: DateTime!, $end: DateTime!) {
            location (id: $locationId){
                name
                address
                points {
                    edges {
                        node {
                            name
                            waterFlowMeasurements (start: $start, end: $end) {
                                totalDurationMs
                                totalVolumeMl
                                weightedAvgTemperatureMinCelsius
                                weightedAvgTemperatureAvgCelsius
                                weightedAvgTemperatureMaxCelsius
                                edges {
                                    node {
                                        timestamp
                                        durationMs
                                        volumeMl
                                        temperatureMinCelsius
                                        temperatureAvgCelsius
                                        temperatureMaxCelsius
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """

        dt1 = pytz.utc.localize(datetime(2022, 1, 2, 12))
        dt2 = pytz.utc.localize(datetime(2022, 1, 2, 18))
        location = self.locations[-1]
        variables = {
            "locationId": to_global_id("LocationType", location.pk),
            "start": dt1,
            "end": dt2,
        }
        result = self.client.execute(query, variables)

        assert result.data == location_result
