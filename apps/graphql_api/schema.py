import graphene
from django.db.models import F, FloatField, Sum
from graphene import Connection, Float, relay
from graphene_django import DjangoObjectType, filter

from apps.graphql_api.helpers import calculate_sum, calculate_weighted_average
from apps.measurements.models.location.model import Location
from apps.measurements.models.measurement_point.model import MeasurementPoint
from apps.measurements.models.water_flow_measurement.model import WaterFlowMeasurement


class WaterFlowMeasurementType(DjangoObjectType):
    class Meta:
        model = WaterFlowMeasurement
        fields = (
            "id",
            "measurement_point",
            "timestamp",
            "duration_ms",
            "volume_ml",
            "temperature_min_celsius",
            "temperature_avg_celsius",
            "temperature_max_celsius",
        )
        interfaces = (relay.Node,)


class WaterFlowMeasurementConnection(Connection):
    total_duration_ms = Float()
    total_volume_ml = Float()
    weighted_avg_temperature_min_celsius = Float()
    weighted_avg_temperature_avg_celsius = Float()
    weighted_avg_temperature_max_celsius = Float()

    class Meta:
        node = WaterFlowMeasurementType

    def resolve_total_duration_ms(root, info):
        return calculate_sum(root.iterable, "duration_ms")

    def resolve_total_volume_ml(root, info):
        return calculate_sum(root.iterable, "volume_ml")

    def resolve_weighted_avg_temperature_min_celsius(root, info):
        return calculate_weighted_average(
            root.iterable, "temperature_min_celsius", "volume_ml"
        )

    def resolve_weighted_avg_temperature_avg_celsius(root, info):
        return calculate_weighted_average(
            root.iterable, "temperature_avg_celsius", "volume_ml"
        )

    def resolve_weighted_avg_temperature_max_celsius(root, info):
        return calculate_weighted_average(
            root.iterable, "temperature_max_celsius", "volume_ml"
        )


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = ("id", "name", "address", "points")
        filter_fields = ["id", "name", "address", "points"]
        interfaces = (relay.Node,)


class LocationConnection(graphene.relay.Connection):
    class Meta:
        node = LocationType


class MeasurementPointType(DjangoObjectType):
    class Meta:
        model = MeasurementPoint
        fields = ("id", "location", "name", "water_flow_measurements")
        interfaces = (relay.Node,)

    water_flow_measurements = graphene.ConnectionField(
        WaterFlowMeasurementConnection,
        start=graphene.DateTime(required=True),
        end=graphene.DateTime(required=True),
    )

    def resolve_water_flow_measurements(self, info, start, end):
        return self.water_flow_measurements.filter(
            timestamp__gte=start, timestamp__lte=end
        )


class Query(graphene.ObjectType):
    location = graphene.relay.Node.Field(LocationType)
    all_locations = filter.DjangoFilterConnectionField(LocationType)


schema = graphene.Schema(query=Query)
