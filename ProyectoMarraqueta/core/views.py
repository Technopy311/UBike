from django.shortcuts import render, redirect


def welcome_view(request):
    return render(request, 'core/welcome.html')

def user_view(request):
    return render(request, 'core/vista_usuario.html')

def user_register(request): # View which receives from / to register
    pass

def login_user(request): # View to login users
    pass

def guard_view(request): # View of security dashboard
    return render(request, 'core/security_dashboard.html')