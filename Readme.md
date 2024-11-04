# Scenario

In this Django App we want to create an API to model water measurement sensors. The sensors can be installed in different locations, for example "House 1", "Factory on the hill", "School 3".

On each location, we may have multiple measuring points, for example "House 1" may have a "Kitchen sink water tube" measuring point, "Laundry room washing machine tube" measuring point, ...

On each of these points our sensors will take measurements when the water is flowing, those measurements will include:

- Time of the measurement (timestamp)
- Duration of the water flow (duration_ms)
- Volume of the water flow (volume_ml)
- Temperature of the water (temperature_*)

On this scenario, we assume that those measurements are already stored in the database, and we only have to display the results on a GraphQL API.


# Code provided

The code provided includes the basic Django project, with the models and tests to pass.


# Objective

Please create a GraphQL API using graphene-django with graphene.relay.Node interfaces to pass the tests that exist under `apps/graphql_api/tests/basic_tests.py`. You can see which Graphene types and fields to implement from the queries executed in that file.

The general structure should be:
- Create `DjangoObjectType` types for each of the 3 models with interface `graphene.relay.Node` (LocationType, MeasurementPointType, WaterFlowMeasurementType).
- Create the query for `allLocations` using `DjangoFilterConnectionField`
- Create the query for `location` using `graphene.relay.Node.Field`
- Create a field on the type `MeasurementPointType` with parameters `start` and `end` that allows us to query the `WaterFlowMeasurements` under this MeasurementPoint in the time period between `start` and `end`.
  - Add a `graphene.Connection` type to calculate aggregated values over those  `WaterFlowMeasurements` records:
    - `total_duration_ms`: Sum of the field `duration_ms` for all records queried
    - `total_volume_ml`: Sum of the field `volume_ml` for all records queried
    - `weighted_avg_temperature_min_celsius`: Average of the field `temperature_min_celsius` weighted by `volume_ml` (https://en.wikipedia.org/wiki/Weighted_arithmetic_mean)
    - `weighted_avg_temperature_avg_celsius`: Average of the field `temperature_avg_celsius` weighted by `volume_ml` (https://en.wikipedia.org/wiki/Weighted_arithmetic_mean)
    - `weighted_avg_temperature_max_celsius`: Average of the field `temperature_max_celsius` weighted by `volume_ml` (https://en.wikipedia.org/wiki/Weighted_arithmetic_mean)


# How to setup and run the tests

- Create Python virtual environment

$ pip install -r requirements/dev.txt

$ pytest --create-db
