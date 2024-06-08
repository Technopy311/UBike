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
            if user.is_guard:
                return redirect('guard_view')
            else:
                return redirect('user_view')
        else:
            return redirect('welcome_view')

    else:
        return redirect('welcome_view')

def custom_register(request, next=None):
    return redirect('welcome_view')
    if request.method == "POST":
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        rut = request.POST["rut"]
        password = request.POST["password"]
        email = request.POST["email"]
        
        modelBici = request.POST["modelBici"]
        marcaBici = request.POST["marcaBici"]
        colorBici = request.POST["colorBici"]
        #fotoBici = request.FILES["fotoBici"]
        print(request.FILES)

        try:
            usuario = core_models.User(
                username = nombre,
                last_name=apellido,
                run=rut,
                password=password,
                email=email,
            )
            usuario.save()
        except Exception:
            pass

        try:
            bicicleta = core_models.Bicycle(
                model=(str(marcaBici)+'-'+str(modelBici)),
                colour=colorBici,
                bicy_user=usuario,
                image=fotoBici,
            )
            bicicleta.save()
        except Exception:
            pass

    else:
        return redirect('welcome_view')

def changepass(request):
    pass

def logout(request, next):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return redirect('welcome_view')
    else:
        return redirect('welcome_view')