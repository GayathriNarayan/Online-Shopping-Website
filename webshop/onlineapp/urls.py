from onlineapp import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.apps import AppConfig


app_name='onlineapp'

urlpatterns = [
    
path('product_view/<int:pid>/', views.product_view,name='product_view'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
