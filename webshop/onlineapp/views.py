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
from onlineapp.forms import UserForm, LoginForm, EditUserProfileForm
from onlineapp.forms import LoginForm
from django.contrib.auth.models import User

#------ imran imports ----
from django.contrib.auth.forms import PasswordChangeForm

#-------------------------


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


def cart_add(request, id):
  return HttpResponse('done')


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
   print
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




