from unicodedata import name
from .import views
from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

from .views import AppointmentViewSet,DoctorViewSet


urlpatterns=[
    path('',views.index,name='index'),
    path('signout/',views.signout,name='signout'),
    path('signin/',views.signIn,name='signin'),
    path('signup/',views.signUp,name='signup'),
    path('userReg/',views.userRegistration,name='userReg'),
    path('doctorReg/',views.doctorRegistration,name='doctorReg'),
    path('hospitalReg/',views.hospitalRegistration,name='hospitalReg'),


    # appointment crud
    path('docAppointment/',views.DoctorAppointment,name='docAppointment'),

    # search urls  
  #  path('DocsearchResult/',views.DocsearchResult,name='DocsearchResult'),


    # rest crud

      path('registerDoctor/', DoctorViewSet.as_view({
        'post':'create'
    })),

     path('createAppointment/', AppointmentViewSet.as_view({
        'get':'list',
        'post':'create'
    }))

  
]