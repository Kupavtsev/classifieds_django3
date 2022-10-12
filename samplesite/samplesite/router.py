from bboard.api.viewsets import BbViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bboard', BbViewSet, basename='bb')

# for url in router.urls:
#     print(url, '\n')