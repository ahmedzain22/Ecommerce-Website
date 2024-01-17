
from EcommerceWeb.models import *
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal 
from django.http import JsonResponse,HttpResponse


import stripe
from django.conf import settings
from django.db import transaction
from django.urls import reverse

from django.contrib.auth.views import LogoutView





# dashboard view functions 

def dashboardbase (request):
    return render(request, 'dashboard/dashboardbase.html')


# dashboad product list
def dashboardproductlist(request):
    products = Product.objects.all()
    context = {'product_list': products}
    return render(request, 'dashboard/dashboardproductlist.html', context)




# deleteing product from product list

def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()

        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



# creating new product in dashboard 

def dashboardproductcreate (request):

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_discription')

        print(product_description)
        print(product_price)
        print(product_name)
        new_product = Product.objects.create(
            name=product_name,
            price=product_price,
            description=product_description,
            image=request.FILES.get('image')
        )
        
        # print("product created sucessfully")

        return redirect('dashboard/dashboardproductlist')

    return render(request, 'dashboard/dashboardproductcreate.html')




# updating the exexting product





def dashboardproductupdate(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        
        product.name = request.POST.get('product_name')
        product.price = request.POST.get('product_price')
        product.description = request.POST.get('product_description')
        new_image = request.FILES.get('image')
        
        
        if new_image:
            product.image = new_image

        product.save()

        return redirect('dashboard/dashboardproductlist')  

    return render(request, 'dashboard/dashboardproductupdate.html', {'product': product})





# order list list of all the orders 


def dashboardorderlist(request):
    orders = Order.objects.all()
    return render(request, 'dashboard/dashboardorderlist.html', {'orders': orders})



#  detal of order 
def dashboardorderdetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'dashboard/dashboardorderdetail.html', {'order': order})



from django.contrib.auth import authenticate,login

# login to dashboard 

def dashboardlogin(request):
    
    


    if request.method == 'POST':
    
            username = request.POST.get('Username')
            password = request.POST.get('password')
                
            print(username, password)
                
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard/dashboardproductlist')  
            else:
                return HttpResponse('Invalid UserName  or password')
                
    else:
        
        return render(request, 'dashboard/dashboardlogin.html')
