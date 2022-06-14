from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.apps import AppConfig
from django.contrib import admin
from onlineapp import views

app_name= 'onlineapp'
urlpatterns = [
    path('signup/', views.user_signup, name="user_signup"),
    path('login/', views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path('about/', views.contactus, name="about"),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('changepass/', views.changepass, name='changepass'),
    path('product_list/<int:id>/', views.product_list,name='product_list'),
]        
    

