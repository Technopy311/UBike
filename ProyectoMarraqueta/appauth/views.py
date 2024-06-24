from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from core import models as core_models
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.images import ImageFile
from django.conf import settings
from django.db import IntegrityError
from pathlib import Path
import re


def custom_login(request, next=None):
    if request.method == "POST":
        mail = request.POST.get("mail")
        password = request.POST.get("password")

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
            elif user.is_superuser or user.is_staff:
                return redirect('/admin')
            else:
                return redirect('user_view')
        else:
            return render(request, 'core/welcome.html', context={'errormsg': 'Datos inválidos.'})        

    else:
        return redirect('welcome_view')

def custom_register(request, next=None):
    context = {
        'errormsg': None
    }
    
    if request.method == "POST":
        try: 
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            rut = request.POST.get("rut")
            password = request.POST.get("password")
            email = request.POST.get("email")
            
            modelBici = request.POST.get("modelBici")
            marcaBici = request.POST.get("marcaBici")
            colorBici = request.POST.get("colorBici")
            fotoBici = request.FILES.get("fotoBici")
        except Exception:
            context['errormsg'] = 'Datos inválidos.'
            return render(request, 'core/welcome.html')    
        
        rut = re.sub('[^0-9]', '', rut)   # Sanitize field to remove non-digits

        try:
            validate_password(password)
        except ValidationError:
            context['errormsg']= "Contraseña insegura."
            return render(request, 'core/welcome.html', context)
        
        # Create new user
        try:
            usuario = core_models.User(
                username = nombre,
                first_name = nombre,
                last_name=apellido,
                run=rut,
                password=password,
                email=email,
            )
        except ValueError:
            context['errormsg'] = 'Datos inválidos.'
            return render(request, 'core/welcome.html', context=context)
        except IntegrityError:
            context['errormsg'] = 'Datos ya registrados.'
            return render(request, 'core/welcome.html', context=context)
        usuario.save()
    
        # Save image
        image_path = settings.MEDIA_ROOT + fotoBici.name
        
        destination = open(image_path, 'wb+')
        for chunk in fotoBici.chunks():
            destination.write(chunk)
        destination.close()
        
        path = Path(image_path)
        # Save bicycle
        bicicleta = core_models.Bicycle(
            model=(str(marcaBici)+'-'+str(modelBici)),
            colour=colorBici,
            bicy_user=core_models.User.objects.get(email=email),
            image=None,
        )
        
        with path.open(mode="rb") as f:
            bicicleta.image = ImageFile(f, name=path.name)
            bicicleta.save()
        
        # Login user
        login(request, usuario)        
        return redirect('user_view')

    else:
        return redirect('welcome_view')


def custom_logout(request, next=None):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return redirect('welcome_view')
    else:
        return redirect('welcome_view')