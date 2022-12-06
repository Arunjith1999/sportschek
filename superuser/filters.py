import django_filters
from login.models import OrderTable
from django_filters import DateFilter


class orderFilter(django_filters.FilterSet):
    class Meta:
        model = OrderTable
        fields=['date_delivered']