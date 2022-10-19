# from django.views.decorators.cache import cache_page
from django.urls import path
from .models            import Bb

from bboard.assets.emails_handler import mail_send
from . import views


app_name = 'bboard'

urlpatterns = [
    #10 API
    path('api/rubrics/<int:pk>', views.api_rubrics_detail),
    path('api/rubrics', views.api_rubrics),
    # 9 Cabinet
    path('cabinet/', views.PrivateCabinet.as_view(), name='cabinet'),
    # 8 Emails
    path('email_send/', mail_send, name='mail_send'),
    # 7 Edit/Validation in forms
    path('bbs/<int:rubric_id>', views.bbs, name='bbs'),
    path('rubrics/', views.rubrics, name='rubrics'),
    # 6 DATES
    path('<int:year>/<int:month>/<int:day>', views.BbDayArchiveView.as_view(model=Bb, date_field='published', month_format='%m')),
    # path('<int:year>/', views.BbYearArchiveView.as_view()),
    path('<int:year>/<int:month>', views.BbMonthArchiveView.as_view()),
    # 5 EDIT AD FORM - CLASS
    path('edit/<int:pk>/', views.BbUpdateView.as_view(), name='edit'),
    # path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.BbDeleteView.as_view(), name='delete'),
    # 4 Add new Advertisment
    path('add/', views.BbAddFormView.as_view(), name='add'),
    # 3 DETAIL VIEW OF EACH PRODUCT
    path('detail/<int:pk>/', views.BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', views.BbDayDetailView.as_view(), name='detail'),
    # 2 BY RUBRIC - FUNC
    # path('<int:rubric_id>/', views.by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', views.BbByRubricView.as_view(), name='by_rubric'),
    # 1 MAIN PAGE
    # path('', views.BbIndexView.as_view(), name='index'),
    path('', views.index, name='index'),
]
