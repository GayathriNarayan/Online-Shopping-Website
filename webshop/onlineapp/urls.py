from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.apps import AppConfig
from django.contrib import admin
from onlineapp import views

app_name='onlineapp'

urlpatterns = [

    path('signup/', views.user_signup, name="user_signup"),
    path('login/', views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path('add/<int:id>/', views.cart_add, name='cart_add'),
    path('product_view/<int:pid>/', views.product_view,name='product_view'),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name="about"), 
    
   ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)