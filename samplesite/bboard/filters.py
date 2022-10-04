from dataclasses import field
import django_filters
from django_filters import DateFilter, CharFilter

from .models import Bb, Rubric


class BbFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='published', lookup_expr='gte')
    end_date = DateFilter(field_name='published', lookup_expr='lte')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Bb
        # fields = '__all__'
        fields = ['rubric', 'price', 'kind']
        # exclude = [ 'title', 'price', 'kind']
