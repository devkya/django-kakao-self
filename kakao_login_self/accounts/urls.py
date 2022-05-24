from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('kakao/login/', kakao_login, name='kakao_login'),
    # path('kakao/logout/', kakao_logout, name='kakao_logout'),
    path('kakao/login/callback/', get_user_info),
]
