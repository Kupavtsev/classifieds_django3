from bboard.models import Bb
from .serializers import BbSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


# class BbViewSet(viewsets.ViewSet):

#     def list(self, request):
#         queryset = Bb.objects.all()
#         serializer = BbSerializer(queryset, many=True)
#         return Response(serializer.data)

class BbFilter(filters.FilterSet):
    # title = filters.CharFilter(lookup_expr='icontains')       # one of variant

    class Meta:
        model = Bb
        # fields = ('title', 'price')                           # one of variant
        fields = {
            'title': ['icontains'],
            'published': ['iexact', 'lte', 'gte']
        }


class BbViewSet(viewsets.ModelViewSet):

    # list, create, retrieve, update, destroy

    queryset = Bb.objects.all()
    serializer_class = BbSerializer
    # filter_backends = [DjangoFilterBackend]                    # We can use it instead of global DEFAULT_FILTER_BACKENDS
    # filter_fields = ('title', 'price', 'rubric')               # Its doesnt work even with global DEFAULT_FILTER_BACKENDS
    
    filterset_class = BbFilter

    # auhtentication_classes = (TokenAuthentication,)               # it's doesnt work properly! Why ?
    # permission_classes = (IsAuthenticated, )

    @action(methods=['GET'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('published').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

    # When we use 'filter_fields' we dont need it
    # def get_queryset(self):
    #     # queryset = super(CLASS_NAME, self).get_queryset()
    #     queryset = Bb.objects.filter(title__icontains='иж')
    #     return queryset