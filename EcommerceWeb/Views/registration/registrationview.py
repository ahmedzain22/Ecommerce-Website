from EcommerceWeb.models import *
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal 
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        
        if password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'registration/register.html')


        
        user = User.objects.create_user(username=username, password=password1)
        auth_login(request, user)
        return redirect('home')  

    return render(request, 'registration/register.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'registration/login.html')



class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect('home')