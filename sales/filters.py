import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):

    created_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    created_to = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    class Meta:
        model = Order
        fields = ["status", "dealer"]