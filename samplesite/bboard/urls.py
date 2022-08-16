from django.urls import path

from .views import (index,
                   by_rubric, BbByRubricView, BbByRubricViewListView,
                   BbCreateView, BbAddFormView,
                   BbDetailView, BbUpdateView, BbDeleteView)

# app_name = 'bboard'

urlpatterns = [
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', BbUpdateView.as_view(), name='edit'),
    path('add/', BbAddFormView.as_view(), name='add'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricViewListView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('', index, name='index'),
]
