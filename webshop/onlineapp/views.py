from itertools import product
from unicodedata import name
from onlineshopping.settings import MEDIA_ROOT,MEDIA_URL
# Create your views here.
from django.shortcuts import  render, redirect
from .forms import UserForm
from django.contrib.auth import login
from django.contrib import messages
from collections import UserString
from django.shortcuts import render
from onlineapp import forms ,models
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from onlineapp.forms import UserForm, LoginForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from onlineapp.models import Product, ProductClassification, Contactus
from django.contrib.auth.forms import PasswordChangeForm
from onlineapp.forms import UserForm,LoginForm,EditUserProfileForm

# Create your views here.

def home(request):
  return render(request,'onlineapp/home.html')

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

#---------- change password-----------#

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

#---------- Product List-----------#
 
def home(request):
  category = ProductClassification.objects.all()
  product = Product.objects.all()
  categoryID = request.GET.get('category')
  if categoryID:
    product = Product.objects.filter(productclassification=categoryID)
  else:
    product = Product.objects.all()
  data_category = {
    'category' : category,
    'product' : product,
    'media_url': MEDIA_URL
  }
  return render(request,'onlineapp/home.html', data_category)

  #---------- About-----------#

def contactus(request):
  if request.method == 'POST':
    contact = Contactus(
      name = request.POST.get('name'),
      email = request.POST.get('email'),
      subject = request.POST.get('subject'),
      message = request.POST.get('message'),
    )
    contact.save()
  return render(request, 'onlineapp/about.html')