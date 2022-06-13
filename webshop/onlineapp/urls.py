from django.urls import path,include
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
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart-detail/',views.cart_detail,name='cart_detail'),
    path('checkout/',views.checkout,name='checkout'),
    path('user_orders/',views.user_orders,name='user_orders'),   
    path('user_order_detail/<int:id>',views.user_order_detail, name='user_order_detail'), 
    path('paypal/', include('paypal.standard.ipn.urls')),
    # path('payment_process/', views.payment_process, name='payment_process' ),
    path('payment_done/<int:id>/', views.payment_done, name='payment_done'),
    path('payment_cancelled/<int:id>/', views.payment_cancelled, name='payment_cancelled'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
