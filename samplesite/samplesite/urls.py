"""samplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf        import settings
from django.conf.urls   import url
from django.urls        import path, include
from django.contrib     import admin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView, PasswordChangeView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from rest_framework.authtoken import views


from bboard.views import PassChg
from .router import router



urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),

    # 8 Password operations
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='bboard:index'), name='logout'),
    
    path('accounts/password_change/', PassChg.as_view(), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(
                        template_name='registration/password_changed.html'),
                        name='password_change_done'),
    
    # Use default parametrs
    path('accounts/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('accounts/password_reset/', PasswordResetView.as_view(
    #                         template_name='registration/reset_password.html',
    #                         subject_template_name='registration/reset_subject.txt',
    #                         email_template_name='registration/reset_email.txt'
    #                         ), name='password_reset'),

    path('accounts/password_reset/done', PasswordResetDoneView.as_view(
                              template_name='registration/email_sent.html'),
                              name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
                              template_name='registration/confirm_password.html'),
                              name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(
                              template_name='registration/password_confirmed.html'),
                              name='password_reset_complete'),

    path('captcha/', include('captcha.urls')),
    url('', include('social_django.urls', namespace='social')),

    
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth')
]



# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(
#             r'^__debug__/',
#             include(debug_toolbar.urls)
#             ),
#     ]