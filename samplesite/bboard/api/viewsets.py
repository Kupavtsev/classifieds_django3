from bboard.models import Bb
from .serializers import BbSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# class BbViewSet(viewsets.ViewSet):

#     def list(self, request):
#         queryset = Bb.objects.all()
#         serializer = BbSerializer(queryset, many=True)
#         return Response(serializer.data)



class BbViewSet(viewsets.ModelViewSet):

    # list, create, retrieve, update, destroy

    queryset = Bb.objects.all()
    serializer_class = BbSerializer
    # auhtentication_classes = (TokenAuthentication,)               # it's doesnt work properly! Why ?
    # permission_classes = (IsAuthenticated, )

    @action(methods=['GET'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('published').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)