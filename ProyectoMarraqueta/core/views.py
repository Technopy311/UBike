from django.shortcuts import render, redirect
from . import models as core_models
from django.db.models import Q

from django.contrib.auth.decorators import login_required

def welcome_view(request):
    return render(request, 'core/welcome.html')

@login_required
def user_view(request):
    if (request.user.is_guard is not None):
        return redirect('guard_view')
    else:
        pass
    user = request.user

    bicycle = user.bicycle_set.get()
    holder = core_models.BicycleHolder.objects.get(pk=bicycle.holder_pk)

    context = {
        "name": user.username,
        "model": bicycle.model,
        "colour": bicycle.colour,
        "status": False,
        "holder": 0,
        "nearby": holder.nearest_building,
        "image_url": bicycle.image.url,
        "holder_x_coord": holder.coord_x,
        "holder_y_coord": holder.coord_y,
    }

    if bicycle.is_saved:
        context["status"] = True
        context["holder"] = bicycle.holder_pk
    return render(request, 'core/vista_usuario.html', context=context)


@login_required
def guard_view(request): # View of security dashboard
    if (request.user.is_guard is not None) or (request.user.is_superuser):
        
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
    else:
        return redirect('welcome_view')
        

    return render(request, 'core/security_dashboard.html', context=context)