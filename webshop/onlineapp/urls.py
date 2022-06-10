from django.contrib import admin
from django.urls import path
from onlineapp import  views

app_name= 'onlineapp'
urlpatterns = [
    path('signup/', views.user_signup, name="user_signup"),
    path('login/', views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path('profile/', views.profile, name="profile"),
     
    
]
