from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from store import models
import datetime
import json

def store(request):
    if(request.user.is_authenticated):
        customer=request.user.customer
        order,created=models.Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    products=models.Product.objects.all()
    d={'products':products,'cartItems':cartItems,'shipping':False}
    return render(request,'store.html',d)

def cart(request):
    if(request.user.is_authenticated):
        customer=request.user.customer
        order,created=models.Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        cartItems=order['get_Cart_items']
    d={'items':items,'order':order,'cartItems':cartItems,'shipping':False}
    return render(request,'cart.html',d)

def checkout(request):
    if(request.user.is_authenticated):
        customer=request.user.customer
        order,created=models.Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    d={'items':items,'order':order,'cartItems':cartItems,'shipping':False}
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

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if(request.user.is_authenticated):
        customer=request.user.customer
        order,created=models.Order.objects.get_or_create(customer=customer,complete=False)
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
    else:
        print('user is not logged in ...')
    return JsonResponse('Payment Done',safe=False)