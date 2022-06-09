from django.shortcuts import render

# Create your views here.

def home(request):
  return render(request,'onlineapp/home.html')


def clothing(request):
  context = {}
  return render(request,'onlineapp/clothing.html', context)


def shoes(request):
  context = {}
  return render(request,'onlineapp/shoes.html', context)

def accessories(request):
  context = {}
  return render(request,'onlineapp/accessories.html', context)
