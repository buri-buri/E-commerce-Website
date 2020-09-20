from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpRequest

def store(request):
    d={}
    return render(request,'store.html',d)

def cart(request):
    d={}
    return render(request,'cart.html',d)

def checkout(request):
    d={}
    return render(request,'checkout.html',d)