from itertools import product
from unicodedata import name
# Create your views here.
from django.shortcuts import  render, redirect
from .forms import UserForm
from django.contrib.auth import login
from django.contrib import messages
from collections import UserString
from django.shortcuts import render
from onlineapp import forms
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from onlineapp import models
from django.shortcuts import render
from onlineapp.forms import UserForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from onlineapp.forms import LoginForm
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from onlineapp.models import Product

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

  

#######################sending email #############################
from django.core.mail import send_mail
from django.conf import settings
import smtplib


def send_welcome_email(request, sended_email):
    subject = 'Welcome Message from G3-Store'
    message = "Your registeration is complete, you can browse more items and shop"
    from_email=settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email,[sended_email],auth_user= settings.EMAIL_HOST_USER, fail_silently=False,
    html_message="html><body><table style='font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 100%;'><tr><td style ='border: 1px solid #ddd;padding: 8px;'>Welcome "+ sended_email +" you can browse more items using " +settings.HOME_LINK +"</td></tr><tr><td style ='border: 1px solid #ddd;padding: 8px;'>to login " +settings.LOGIN_LINK +" </td></tr><tr><td style ='border: 1px solid #ddd;padding: 8px;'> To show products "+settings.PRODUCT_LINK +"</td></tr></table></body></html>")
  
  
