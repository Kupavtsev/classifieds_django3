from django.urls import path
from .models            import Bb

from .views import (index, BbIndexView,
                   by_rubric, BbByRubricView, BbByRubricViewListView,
                   BbCreateView, BbAddFormView,
                   BbDetailView, BbUpdateView, edit, BbDeleteView,
                   BbMonthArchiveView, BbYearArchiveView, BbDayArchiveView, BbDayDetailView,
                   rubrics, bbs)

app_name = 'bboard'

urlpatterns = [

    # 7 Edit/Validation in forms
    path('bbs/<int:rubric_id>', bbs, name='bbs'),
    path('rubrics/', rubrics, name='rubrics'),
    
    # 6 DATES
    path('<int:year>/<int:month>/<int:day>', BbDayArchiveView.as_view(model=Bb, date_field='published', month_format='%m')),
    # path('<int:year>/', BbYearArchiveView.as_view()),
    path('<int:year>/<int:month>', BbMonthArchiveView.as_view()),

    
    # 5 EDIT AD FORM - CLASS
    path('edit/<int:pk>/', BbUpdateView.as_view(), name='edit'),
    # path('edit/<int:pk>/', BbUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    # 4 Add new Advertisment
    path('add/', BbAddFormView.as_view(), name='add'),

    # 3 DETAIL VIEW OF EACH PRODUCT
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDayDetailView.as_view(), name='detail'),

    # 2 BY RUBRIC - FUNC
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),

    # 1 MAIN PAGE
    # path('', BbIndexView.as_view(), name='index'),
    path('', index, name='index'),
]
