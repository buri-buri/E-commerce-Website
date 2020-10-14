#from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import *
from django.conf import settings
from django.http import JsonResponse
from store import models
import datetime
import json

def store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    products=models.Product.objects.all()
    d={'products':products,'cartItems':cartItems}
    return render(request,'store.html',d)

def cart(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    d={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',d)

def checkout(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    d={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',d)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:',action)
    print('ProductId:',productId)
    customer=request.user.customer
    product=models.Product.objects.get(id=productId)
    order,created=models.Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=models.OrderItem.objects.get_or_create(order=order,product=product)
    if(action=='add'):
        orderItem.quantity+=1
    elif(action=='remove'):
        orderItem.quantity-=1
    orderItem.save()
    if(orderItem.quantity<1):
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

#@csrf_exempt
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if(request.user.is_authenticated):
        customer=request.user.customer
        order,created=models.Order.objects.get_or_create(customer=customer,complete=False)
    else:
        customer,order=guestOrder(request,data)
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    if(total==order.get_cart_total):
        order.complete=True
    order.save()
    if(order.shipping==True):
        models.ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment Done',safe=False)