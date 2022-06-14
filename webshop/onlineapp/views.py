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
from onlineapp.forms import UserForm
from onlineapp.forms import LoginForm
from django.contrib.auth.models import User


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


def cart_add(request, id):
  return HttpResponse('done')