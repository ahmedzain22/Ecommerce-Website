from EcommerceWeb.models import *
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal 
from django.http import JsonResponse,HttpResponse


import stripe
from django.conf import settings
from django.db import transaction
from django.urls import reverse

from django.contrib.auth.views import LogoutView

from django.contrib.auth import login as auth_login


from django.contrib import messages





# Create your views here.



# base teamplate include header and footer 
def base(request):
    
    
    return render(request, 'base.html')



# home page
def home(request):
    products = Product.objects.all()
   
    

    context = {
        
        'products': products, 
        
    }
    return render(request, 'home.html', context)
    
    
# shop page 
def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html',   {'products': products} )
    
    




# remove it after testing its only for testing

def hometest(request):
    
    products = Product.objects.all()
    return render(request, 'hometest.html',   {'products': products} )



# index teamplate is for testing purpose (remove it if testing ended) 
def index(request):
    return render(request, 'index.html')

# about page

def about(request):
    return render(request, 'about.html')


# contact page
def contact(request):
    return render(request, 'contact.html')




# Single product view need product primary key 

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product-detail.html', {'product': product})


# def cart2(request):
#     return render(request, 'shopping-cart2.html')




# cart 


def cart(request):
    cart = request.session.get('cart', {})
    list = []
    for item_id, item in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        item['product'] = product
        item['total_price'] = item['quantity'] * product.price
        
        # Add item details to the list
        list.append({
            'product_name': item['product'],
            
            'total_price': item['total_price']
        })
    

    total_price = sum(item['total_price'] for item in cart.values())
    
    
    print(list)
    

    return render(request, 'shopping-cart2.html', {'cart': cart.values(), 'total_price': total_price})

 
# item adding n the cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    else:
        quantity = 1

    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product.id), {'quantity': 0})
    cart_item['quantity'] += quantity
    cart[str(product.id)] = cart_item
    request.session['cart'] = cart

    return redirect('shopping-cart2')



# item removing from cart


from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def calculate_total_price(cart):
    print("total price calculation is hit")
    total_price = Decimal('0')  

    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        quantity = Decimal(item_data['quantity'])  
        total_price += quantity * product.price

    return total_price

def remove_from_cart(request, product_id):
    print("remove fuction hit")
    print(product_id)
    try:
        cart = request.session.get('cart', {})
        
        if str(product_id) in cart:
            del cart[str(product_id)]
            print("the iteam is deleted")
            request.session['cart'] = cart
            
            total_price = calculate_total_price(cart) 
            print(total_price)

            return JsonResponse({'success': True, 'total_price': total_price})

    except Exception as e:
        # Log the exception for debugging
        print(e)

    return JsonResponse({'success': False, 'error': 'Internal Server Error'}, status=500)






# checkout and order place



stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    
    
    if request.method == 'POST':
        
        # retriving data from template 
        first_name_ship = request.POST.get('first_name')
        last_name_ship = request.POST.get('last_name')
        phone_ship = request.POST.get('phone')
        email_ship = request.POST.get('email')
        address_ship = request.POST.get('address')
        city_ship = request.POST.get('city')
        country_ship = request.POST.get('country')
        
        # creating shipping instance
        shipping_address = ShippingAddress.objects.create(
            
            
            first_name=first_name_ship,
            last_name=last_name_ship,
            phone = phone_ship,
            email = email_ship,
            address= address_ship,
            city= city_ship,
            country= country_ship
            
        )

    
        grandtotal_str = request.POST.get('Grandtotal')

        if grandtotal_str is not None:
            total_price = float(grandtotal_str)
            order = Order.objects.create(
                shipping_address=shipping_address,
                total_price=total_price
            )
        else:
            
            total_price = 0
            order = Order.objects.create(
                shipping_address=shipping_address,
                total_price=total_price
            )

        return_url = request.build_absolute_uri(reverse('home'))
        try:
            with transaction.atomic():
            
                    payment_intent = stripe.PaymentIntent.create(
                    amount=int(total_price * 100),
                    currency='usd',
                    payment_method=request.POST.get('payment_method'),
                    confirmation_method='manual',
                    confirm=True,
                    return_url=return_url,
                    )
                    
                    

                    

            
        
        
            a = request.POST.get('item_count')
        
            b=int(a)
            
            for i in range(b):
            
                print("i am in loop")
                product_name = request.POST.get(f'product_name_{i}')
                
                total_price = request.POST.get(f'total_price_{i}')
                
                quantity = request.POST.get(f'quantity_{i}')
                
                product_price = request.POST.get(f'product_price_{i}')
                

                product = Product.objects.get(name=product_name)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    total_price =total_price,
                    product_name =product_name,
                    product_price = product_price
                    
                )

            return redirect('thankyou', order_id=order.id)
        
        except stripe.error.CardError as e:
            messages.error(request, f"Payment failed: {e.error.message}")
            return render(request, 'checkout.html', {'error': str(e)})
        except stripe.error.StripeError as e:
            messages.error(request, f"Payment failed: {e.error.message}")
            return render(request, 'checkout.html', {'error': str(e)})
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return render(request, 'checkout.html', {'error': str(e)})
    

    
        
    
        # making list and Grand Total
    cart = request.session.get('cart', {})
    
       
    list = []
    for item_id, item in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        item['product'] = product
        item['price'] = product.price
        
        item['total_price'] = item['quantity'] * product.price
            
        list.append({
            'product_name': item['product'],
            'product_price': item['price'],
                
            'total_price': item['total_price'],
            'quantity': item['quantity'] 
            
        })
        
        listlength =len(list)
    

    Grandtotal = sum(item['total_price'] for item in cart.values())    
    
    return render(request, 'checkout.html', context={'product_list': list, 'Grandtotal': Grandtotal, 'listlength': listlength})







def thankyou(request,order_id):
    
     
    order = Order.objects.get(pk=order_id)
    
    context = {'order': order}
    

    return render(request, 'thankyou.html', context)






