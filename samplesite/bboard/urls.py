from django.urls import path
from .models            import Bb

from .views import (index, BbIndexView,
                   by_rubric, BbByRubricView, BbByRubricViewListView,
                   BbCreateView, BbAddFormView,
                   BbDetailView, BbUpdateView, BbDeleteView,
                   BbMonthArchiveView, BbYearArchiveView, BbDayArchiveView, BbDayDetailView)

# app_name = 'bboard'

urlpatterns = [
    
    path('<int:year>/<int:month>/<int:day>', BbDayArchiveView.as_view(model=Bb, date_field='published', month_format='%m')),
    # path('<int:year>/', BbYearArchiveView.as_view()),
    path('<int:year>/<int:month>', BbMonthArchiveView.as_view()),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', BbUpdateView.as_view(), name='edit'),
    path('add/', BbAddFormView.as_view(), name='add'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDayDetailView.as_view(), name='detail'),

    # path('', BbIndexView.as_view(), name='index'),
    path('', index, name='index'),
]
