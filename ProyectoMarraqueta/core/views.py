from django.shortcuts import render, redirect
from . import models as core_models
from django.db.models import Q

def welcome_view(request):
    return render(request, 'core/welcome.html')

def user_view(request):
    return render(request, 'core/vista_usuario.html')

def user_register(request): # View which receives from / to register
    pass

def login_user(request): # View to login users
    pass

def guard_view(request): # View of security dashboard
    context = {
            "latest_bicycles": [],
            "search_results": None
        }

    if request.method == "POST" and request.POST != None:
        
        search_query = request.POST["search_bicycle_info"]
        try:
            search_result = core_models.User.objects.get(
                Q(run__icontains=search_query) | Q(username__icontains=search_query) | Q(email__icontains=search_query) | Q(last_name__icontains=search_query)
            )
            context["search_results"] = [search_result]
        except core_models.User.DoesNotExist:
            context["search_results"] = None

    try:
        latest_bicycles = core_models.Bicycle.objects.all()[:5]
        context["latest_bicycles"] = latest_bicycles
            
    except core_models.Bicycle.DoesNotExist:
        print("No latest bicycles to show")

    

    return render(request, 'core/security_dashboard.html', context=context)