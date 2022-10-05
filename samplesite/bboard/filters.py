import django_filters
from django_filters import DateFilter, CharFilter, RangeFilter
from .models import Bb, Rubric


class BbFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='published', lookup_expr='gte')
    end_date = DateFilter(field_name='published', lookup_expr='lte')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    price = RangeFilter()
    class Meta:
        model = Bb
        # fields = '__all__'
        fields = ['rubric', 'kind']
        # exclude = [ 'title', 'price', 'kind']


'''
class F(django_filters.FilterSet):
    """Filter for Books by Price"""
    price = RangeFilter()

    class Meta:
        model = Book
        fields = ['price']

qs = Book.objects.all().order_by('title')

# Range: Books between 5€ and 15€
f = F({'price_min': '5', 'price_max': '15'}, queryset=qs)

# Min-Only: Books costing more the 11€
f = F({'price_min': '11'}, queryset=qs)

# Max-Only: Books costing less than 19€
f = F({'price_max': '19'}, queryset=qs)
'''