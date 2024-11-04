from django.db.models import F, Sum, query

def calculate_sum(
        queryset: query.QuerySet,
        value_field: str,
    ):
    """
    Calculate sum
    """
    result = queryset.aggregate(sum=Sum(value_field))

    return result["sum"]


def calculate_weighted_average(
        queryset: query.QuerySet,
        value_field: str,
        weight_field: str
    ) -> int:
    """
    Calculate weighted average
    """
    weighted_sum = Sum(F(value_field) * F(weight_field))
    total_weight = Sum(F(weight_field))

    result = queryset.aggregate(weighted_avg=weighted_sum / total_weight)
    return int(result["weighted_avg"])

