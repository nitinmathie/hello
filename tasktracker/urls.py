#from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import path
from .views import (userregistration_view, organizationregistration_view, projectregistration_view, gensend_otp, verify_otp, userlogin_view,
                    updateorganization_view, deleteorganization_view, updateproject_view, deleteproject_view, adduser_view, updateuser_view,
                    deleteuser_view,useradmitreq_view, approveuser_view)

app_name= ""
urlpatterns = [
path('registration', userregistration_view, name= "register"),
path('createorganization/<str:userid>', organizationregistration_view, name= "createorganization"),
path('createproject/<str:userid>/<str:organizationid>', projectregistration_view, name= "createproject"),
path('sendotp',gensend_otp,name='sendotp'),
path('verifyotp',verify_otp,name='verifyotp'),
path('login',userlogin_view,name='login'),
path('updateorganization/<str:userid>/<str:organizationid>',updateorganization_view,name='updateorganization'),
path('deleteorganization/<str:userid>/<str:organizationid>',deleteorganization_view,name='deleteorganization'),
path('updateproject/<str:userid>/<str:projectid>',updateproject_view,name='updateproject'),
path('deleteproject/<str:userid>/<str:projectid>',deleteproject_view,name='deleteproject'),
path('adduser/<str:userid>/<str:projectid>/<str:organizationid>/<str:role>',adduser_view,name='adduser'),
path('updateuser/<str:userid>', updateuser_view, name= "updateuser"),
path('deleteuser/<str:userid>', deleteuser_view, name= "deleteuser"),
path('useradmitreq', useradmitreq_view, name= "useradmitreq"),
path('approveuser/<str:approverid>', approveuser_view, name= "approveuser"),
]



