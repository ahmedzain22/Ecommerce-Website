
from django.urls import path,include
from . import views
from .views import *
from django.contrib.auth.views import LogoutView
from EcommerceWeb.Views.dashboard import  dashboardview

from EcommerceWeb.Views.registration import  registrationview

from EcommerceWeb.Views.ecommerce import  ecommerceview


urlpatterns = [
    # Add urls
    
    path('hometest/', ecommerceview.hometest, name='hometest'),
    
    
    
    # about template
    path('about/', ecommerceview.about, name='about'),
    
    # contact template
    path('contact/', ecommerceview.contact, name='contact'),
    
    # base template 
    path('base/', ecommerceview.base, name='base'),
    
    # home template
    path('home/', ecommerceview.home, name='home'),
    
    # shop template
    path('shop/', ecommerceview.shop, name='shop'),
    
    
    # Single Product detail 
    path('product/<int:product_id>/', ecommerceview.product_detail, name='product_detail'),
    
    
    # cartpage
    
    
    # path('cart2/', views.cart2, name='shopping-cart2'),
    
    
    
    path('cart2/', ecommerceview.cart, name='shopping-cart2'),
    path('add_to_cart/<int:product_id>/', ecommerceview.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', ecommerceview.remove_from_cart, name='remove_from_cart'),
    # path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    
    
    
    # checkout page
    path('checkout/', ecommerceview.checkout, name='checkout'),
    
    
    
    path('thankyou/<int:order_id>/', ecommerceview.thankyou, name='thankyou'),
    
    
    
    
    # dashboard urls 
    
    path('dashboardbase/', dashboardview.dashboardbase, name='dashboardbase'),
    
    path('dashboardproductlist/', dashboardview.dashboardproductlist, name='dashboardproductlist'),
    
    path('delete_product/<int:product_id>/', dashboardview.delete_product, name='delete_product'),
    
    path('dashboardproductupdate/<int:product_id>/', dashboardview.dashboardproductupdate, name='dashboardproductupdate'),
    
    
    
    path('dashboardproductcreate/', dashboardview.dashboardproductcreate, name='dashboardproductcreate'),
    
    path('dashboardorderlist/', dashboardview.dashboardorderlist, name='dashboardorderlist'),
    
    path('dashboardorderdetail/<int:order_id>/', dashboardview.dashboardorderdetail, name='dashboardorderdetail'),
    
    # dashboard login 
    
    path('dashboardlogin/', dashboardview.dashboardlogin, name='dashboardlogin'),
    
    
    
    
    
    # user registration
    path('register/', registrationview.register, name='register'),
    
    # user login
    
    path('login/', registrationview.user_login, name='user_login'),
    
    # logout 
    path('logout/', registrationview.CustomLogoutView.as_view(), name='logout'),
    
    
    
]
