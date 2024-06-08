from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from core import models as core_models
from django.core.exceptions import PermissionDenied

def custom_login(request, next=None):
    if request.method == "POST":
        mail = request.POST["mail"]
        password = request.POST["password"]

        try:
            username = core_models.User.objects.get(email=mail).username
        except core_models.User.DoesNotExist:
            return redirect('welcome_view') #TODO: add error message functionality for welcome_view
        
        try:
            user = authenticate(request, username=username, password=password)
        except PermissionDenied:
            return redirect('welcome_view') #TODO: add error message functionality for welcome_view

        if user is not None:
            login(request, user)
            return redirect('user_view')
        else:
            return redirect('welcome_view')

    else:
        return redirect('welcome_view')

def register(request):
    pass

def changepass(request):
    pass

def logout(request, next):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return redirect('welcome_view')
    else:
        return redirect('welcome_view')