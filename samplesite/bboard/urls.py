from django.urls import path

from .views import (index, by_rubric,
                   BbCreateView, BbByRubricView,
                   BbDetailView, BbByRubricViewListView)

# app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricViewListView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('', index, name='index'),
]
