from onlineapp.models import Product,ProductSize
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from onlineshopping.settings import MEDIA_ROOT,MEDIA_URL
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
  products =Product.objects.all()
  print(products)
  return render(request,'onlineapp/home.html',{'products':products})

"""
function to fetch product details to be viewed on product view page when user wants
more information regading a particular product
"""
def product_view(request, pid):
  product =Product.objects.filter(id=pid).first()
  sizes = ProductSize.objects.filter(product=product)
  
  return render(request, "onlineapp/product_view.html", {'product':product,'sizes':sizes , 'media_url': MEDIA_URL})
