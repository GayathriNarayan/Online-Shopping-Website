from onlineapp.models import Product,ProductSize,Product_Review
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
from onlineapp.forms import UserForm, LoginForm, EditUserProfileForm
from onlineapp.forms import LoginForm
from django.contrib.auth.models import User
from cart.cart import Cart	
from onlineapp.models import Order,OrderDetail	
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm		
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum	
from django.db.models import F

#------ imran imports ----
from django.contrib.auth.forms import PasswordChangeForm
#-------------------------

# Create your views here.

def home(request):
  products =Product.objects.all()
  return render(request,'onlineapp/home.html',{'products':products})
  
#########################  Product Detail ###############################################

'''
Function to fetch product details to be viewed on product view page when user wants
more information regading a particular product and can add review for that product
to be saved in database.

'''

def product_view(request, pid):
  product =Product.objects.filter(id=pid).first()
  sizes = ProductSize.objects.filter(product=product)
  reviews = Product_Review.objects.filter(product=product).order_by('-datetime') [:5] 
  #customer = request.user

  if request.method=="POST" and request.user.is_authenticated:
    content = request.POST['content']
    review = Product_Review(user= request.user, content=content, product=product)
    review.save()

  return render(request, "onlineapp/product_view.html", {'product':product,
                                                         'sizes':sizes ,
                                                         'reviews':reviews,
                                                         'media_url': MEDIA_URL})

  
####################################################################################
  
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
      send_welcome_email(request,user_form.cleaned_data['email'])

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
     return render(request, 'onlineapp/search.html' , {'data':data, 'media_url': MEDIA_URL})

#-----product list  -----Imran-----
 
def home(request):
  #category = ProductClassification.objects.all()
  product = Product.objects.all()
  data_category = {
   # 'category' : category,
    'product' : product,
    'media_url': MEDIA_URL
  }
  return render(request,'onlineapp/home.html', data_category)

  #---------- Profile-----------#

def profile(request):
    return render(request, 'onlineapp/profile.html',{'media_url': MEDIA_URL})

#---------- Edit Profile-----------#

def edit_profile(request):

  if request.user.is_authenticated:
    if request.method == "POST":
      usr = EditUserProfileForm(request.POST, instance=request.user)
      if usr.is_valid():
        messages.success(request, 'profile updated !')
        usr.save()
    else:
     usr = EditUserProfileForm(instance=request.user)
    return render(request, 'onlineapp/edit_profile.html', {'name': request.user, 
                                                    'form':usr,
                                                    'media_url': MEDIA_URL})

  else:

    return HttpResponseRedirect('onlineapp/login')

#---- change password------ Imran ---- #

def changepass(request):
 if request.method == "POST":
   pwd = PasswordChangeForm(user=request.user, data=request.POST)
   if pwd.is_valid():
     pwd.save()
     messages.success(request, 'Password changed successfully!')
   else:
    messages.warning(request, 'Follow the instructions & Try again')
 else:
    pwd = PasswordChangeForm(user=request.user)
    
 return render(request, 'onlineapp/changepass.html', {'form':pwd})

def about(request):
    return render(request, 'onlineapp/about.html')

#---- Send Email ------
#######################sending email #############################

from django.core.mail import send_mail
from django.conf import settings
import smtplib


def send_welcome_email(request, sended_email):
    subject = 'Welcome Message from G3-Store'
    message = "Your registeration is complete, you can browse more items and shop"
    from_email=settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email,[sended_email],auth_user= settings.EMAIL_HOST_USER, fail_silently=False,
    html_message="html><body><table style='font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 100%;'><tr><td style ='border: 1px solid #ddd;padding: 8px;'>Welcome "+ sended_email +" you can browse more items using " +settings.HOME_LINK +"</td></tr><tr><td style ='border: 1px solid #ddd;padding: 8px;'>To login " +settings.LOGIN_LINK +" </td></tr><tr><td style ='border: 1px solid #ddd;padding: 8px;'> To change your password, link to  "+settings.CHANGE_PASS_LINK +"</td></tr></table></body></html>")

@login_required(login_url="/onlineapp/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("onlineapp:product_view",pid=id)


@login_required(login_url="/onlineapp/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("onlineapp:cart_detail")


@login_required(login_url="/onlineapp/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("onlineapp:cart_detail")


@login_required(login_url="/onlineapp/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    try:
      cart.decrement(product=product)
    finally:      
      return redirect("onlineapp:cart_detail")


@login_required(login_url="/onlineapp/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("onlineapp:cart_detail")


@login_required(login_url="/onlineapp/login")
def cart_detail(request):
    total=0
    data=request.session.values()
    d=list(data)[3]
    l=[*d.values()]
    for i in l:
      total=total+(float(i['quantity'])*float(i['price']))

    context={'total_cart_value':total}    
    return render(request, 'onlineapp/cart.html',context)  

@login_required(login_url="/onlineapp/login")
def checkout(request):
  '''
  Display PayPal Checkout
  pip install django-paypal 2.0 for this functionality
  '''
  data = Cart(request)
  customer=request.user
  address=request.POST.get('address')
  order=Order.objects.create(customer=customer,
                      address=address)
  id=order.id
  order.order_reference="ORD"+str(id).zfill(5)
  order.save()
  
  total_value=0

  for key,value in data.cart.items():
    product = Product.objects.get(id=value['product_id'])
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
      'notify_url': 'http://{}{}'.format(host,reverse('onlineapp:paypal-ipn')),
      'return_url': 'http://{}{}'.format(host,reverse('onlineapp:payment_done',args=(str(order.id),))),
      'cancel_return': 'http://{}{}'.format(host,reverse('onlineapp:payment_cancelled',args=(str(order.id),))),
  }
  form = PayPalPaymentsForm(initial=paypal_dict)
  return render(request, 'onlineapp/payment_process.html',{'form':form})
  

@login_required(login_url="/onlineapp/login")
def user_orders(request):
  '''
  Display orders for the logged in customer
  '''
  orders=Order.objects.filter(customer=request.user).order_by('-id')
  return render(request, 'onlineapp/myorders.html',{'orders':orders})

@login_required(login_url="/onlineapp/login")
def user_order_detail(request,id):
  '''
  Display order details
  '''
  order=Order.objects.get(pk=id)
  orderdetail=OrderDetail.objects.filter(order=order).order_by('-id')
  context={'orderdetail':orderdetail,
            'media_url':MEDIA_URL,
            'total_value':order.get_total_value}
  return render(request, 'onlineapp/orderdetail.html',context)

@csrf_exempt
def payment_done(request,id):  
  '''
  Display payment success page with a link to the order
  '''
  #Delete the cart when the order checkout is success
  del request.session['cart']

  #Update the PayerID
  payment_reference=request.GET['PayerID']
  Order.objects.filter(pk=id).update(payment_provider=payment_reference)  

  #Fetch order to be displayed
  order=Order.objects.get(pk=id)
  context={'payment_reference':payment_reference,
            'id':id,
            'order_reference':order.order_reference,
            'order_date':order.order_date}
  return render(request, 'onlineapp/payment-success.html',context)


@csrf_exempt
def payment_cancelled(request,id):
  '''
  Display payment cancelled page or failed
  for PayPal
  '''
  return render(request, 'onlineapp/payment-fail.html')
