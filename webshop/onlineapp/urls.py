from django.urls import path,include
from . import views

urlpatterns = [
    path('onlineapp/add/<int:id>/', views.cart_add, name='cart_add'),
    path('onlineapp/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('onlineapp/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('onlineapp/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('onlineapp/cart_clear/', views.cart_clear, name='cart_clear'),
    path('onlineapp/cart-detail/',views.cart_detail,name='cart_detail'),
    path('onlineapp/checkout/',views.checkout,name='checkout'),
    path('onlineapp/user_orders/',views.user_orders,name='user_orders'),   
    path('onlineapp/user_order_detail/<int:id>',views.user_order_detail, name='user_order_detail'), 
    path('paypal/', include('paypal.standard.ipn.urls')),
    # path('payment_process/', views.payment_process, name='payment_process' ),
    path('payment_done/<int:id>/', views.payment_done, name='payment_done'),
    path('payment_cancelled/<int:id>/', views.payment_cancelled, name='payment_cancelled'),
]