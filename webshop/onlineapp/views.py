from onlineapp.models import Product,ProductSize
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from onlineshopping.settings import MEDIA_ROOT,MEDIA_URL
from django.urls import reverse
from django.shortcuts import get_object_or_404
from itertools import product
from unicodedata import name
from .forms import UserForm
from django.contrib import messages
from collections import UserString
from onlineapp import forms
from django.contrib import messages
from onlineapp import models
from onlineapp.forms import UserForm
from onlineapp.forms import LoginForm
from django.contrib.auth.models import User
from cart.cart import Cart	
from onlineapp.models import Order,OrderDetail	
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm		
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum	
from django.db.models import F
# Create your views here.

def home(request):
  products =Product.objects.all()
  return render(request,'onlineapp/home.html',{'products':products})
  
#########################  Product Detail ###############################################################################################

"""
function to fetch product details to be viewed on product view page when user wants
more information regading a particular product
"""

def product_view(request, pid):
  product =Product.objects.filter(id=pid).first()
  sizes = ProductSize.objects.filter(product=product)
  return render(request, "onlineapp/product_view.html", {'product':product,'sizes':sizes , 'media_url': MEDIA_URL})
  
#######################################################################################################################################
  
#########################  User Account #############################################
def user_signup(request):
      
  registered = False
  
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    
    if user_form.is_valid():
      user = user_form.save(commit=False)
      user.set_password(user.password)
      user.save()
      registered = True

    else:
      print(user_form.errors)
  
  else:
    user_form = UserForm()

  return render(request, 'onlineapp/signup.html',
                {'user_form':user_form,
                 'registered':registered
                })

def user_login(request):
  '''
  Display the login page for the user to login
  If user logged in check if valid user and display the blog
  else display appropriate error message
  '''
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse('home'))  
        
  form = LoginForm(request.POST or None)
  if request.POST and form.is_valid():
      user = form.login(request)
      if user:
          login(request,user)
          userObj=User.objects.get(username=user.username)
          if userObj:
            return HttpResponseRedirect(reverse('home'))
          
  return render(request,'onlineapp/login.html',{'form':form})
  

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))      
############################################################################

######################### Search #############################################

def search(request):
     text= request.GET['prosearch']
     data=Product.objects.filter(name__icontains = text).order_by('-id')
     return render(request, 'onlineapp/search.html' , {'data':data})


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("/")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    try:
      cart.decrement(product=product)
    finally:      
      return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'onlineapp/cart.html')  

def checkout(request):
  data = Cart(request)
  customer=request.user
  address='11'
  order=Order.objects.create(customer=customer,
                      address=address)
  order.order_reference="ORD0000"+str(order.id)
  order.save()
  
  total_value=0

  for key,value in data.cart.items():
    product = Product.objects.get(id=value['product_id'])
    # size=value['product_id']
    qty=int(value['quantity'])
    price=float(value['price'])
   
    total_value=total_value+(qty*price)
    items=OrderDetail.objects.create(order=order,
                                        product=product,
                                        qty=qty,
                                        price=price)
    items.save()
  # Process Payment
  host = request.get_host()
  paypal_dict = {
      'business': settings.PAYPAL_RECEIVER_EMAIL,
      'amount': total_value,
      'item_name': order.order_reference,
      'invoice': order.order_reference,
      'currency_code': 'SEK',
      'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
      'return_url': 'http://{}{}'.format(host,reverse('payment_done',args=(str(order.id),))),
      'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled',args=(str(order.id),))),
  }
  form = PayPalPaymentsForm(initial=paypal_dict)
  return render(request, 'onlineapp/payment_process.html',{'form':form})
  

@login_required
def user_orders(request):
	orders=Order.objects.filter(customer=request.user).order_by('-id')
	return render(request, 'onlineapp/myorders.html',{'orders':orders})

@login_required
def user_order_detail(request,id):
  order=Order.objects.get(pk=id)
  orderdetail=OrderDetail.objects.filter(order=order).order_by('-id')
  total_value =OrderDetail.objects.filter(order=order).aggregate(total_value=Sum(F('qty') * F('price')))['total_value']
  context={'orderdetail':orderdetail,
            'media_url':MEDIA_URL,
            'total_value':total_value}
  return render(request, 'onlineapp/orderdetail.html',context)

@csrf_exempt
def payment_done(request,id):  
  del request.session['cart']
  payment_reference=request.GET['PayerID']
  Order.objects.filter(pk=id).update(payment_provider=payment_reference)  
  order=Order.objects.get(pk=id)
  context={'payment_reference':payment_reference,
            'id':id,
            'order_reference':order.order_reference,
            'order_date':order.order_date}
  return render(request, 'onlineapp/payment-success.html',context)


@csrf_exempt
def payment_cancelled(request,id):
  return render(request, 'onlineapp/payment-fail.html')
