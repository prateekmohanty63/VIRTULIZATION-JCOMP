from unicodedata import name
from .import views
from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns=[
    path('',views.index,name='index'),
    path('signout/',views.signout,name='signout'),
    path('signup/',views.signUp,name='signup'),
]