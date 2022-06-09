from django.shortcuts import render
from onlineapp.models import Product
from onlineshopping.settings import MEDIA_URL
# Create your views here.

def home(request):
  return render(request,'onlineapp/home.html')

def login(request):
  return render(request, 'onlineapp/login.html')

def home(request):
  # category = Category.objects.all()
  product = Product.objects.all()
  data_category = {
    # 'category' : category,
    'product' : product,
    'media_url': MEDIA_URL
  }
  return render(request,'onlineapp/home.html', data_category)