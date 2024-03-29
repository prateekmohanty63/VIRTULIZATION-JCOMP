from unicodedata import name
from .import views
from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns=[
    path('',views.index,name='index'),
    path('signout/',views.signout,name='signout'),
    path('signin/',views.signIn,name='signin'),
    path('signup/',views.signUp,name='signup'),
    path('userReg/',views.userRegistration,name='userReg'),
    path('doctorReg/',views.doctorRegistration,name='doctorReg'),
    path('hospitalReg/',views.hospitalRegistration,name='hospitalReg'),


     # search views
    path('DocsearchResult/',views.DocsearchResult,name='DocsearchResult'),


    # appointment crud
    
    path('appointment/',AppointmentViewSet.as_view({
        'post':'create'
    }))
    

  
]