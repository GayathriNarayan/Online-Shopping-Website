from django.urls import path
from onlineapp import views

urlpatterns = [
    path('', views.home),
   
]