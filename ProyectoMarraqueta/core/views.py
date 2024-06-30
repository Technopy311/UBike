from django.shortcuts import render, redirect
from . import models as core_models
from django.db.models import Q
from tickets import models as tickets_models
from django.contrib.auth.decorators import login_required

def welcome_view(request):
    context = {}
    if request.user.is_authenticated:
        context["user"] = True
    else:
        context["user"] = False
    return render(request, 'core/welcome.html')


@login_required
def user_view(request):
    if (request.user.is_guard is not None):
        return redirect('guard_view')
    elif request.user.is_superuser:
        return redirect('guard_view')
    
    user = request.user

    bicycle = user.bicycle_set.get()
        
    context = {
        "name": user.username,
        "model": bicycle.model,
        "colour": bicycle.colour,
        "status": False,
        "holder": 0,
        "nearby": None,
        "image_url": bicycle.image.url,
        "holder_x_coord": None,
        "holder_y_coord": None,
    }
    
    if (bicycle.holder_pk is not None) and (bicycle.is_saved) and (bicycle.holder_pk!=0):
        holder = core_models.BicycleHolder.objects.get(pk=bicycle.holder_pk)
        context["holder_x_coord"] = holder.coord_x
        context["holder_y_coord"] = holder.coord_y
        context["nearby"] = holder.location
        context["status"] = True
        context["holder"] = holder.pk
    print(context)
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
                search_result = core_models.User.objects.filter(
                    Q(run__icontains=search_query) | Q(username__icontains=search_query) | Q(email__icontains=search_query) | Q(last_name__icontains=search_query)
                ).exclude()
                context["search_results"] = search_result
            except core_models.User.DoesNotExist:
                context["search_results"] = None
                print("No data found")

        try:
            latest_bicycles = core_models.Bicycle.objects.all()[:5]
            context["latest_bicycles"] = latest_bicycles
                
        except core_models.Bicycle.DoesNotExist:
            print("No latest bicycles to show")
    else:
        return redirect('welcome_view')
        

    return render(request, 'core/security_dashboard.html', context=context)


@login_required
def user_detail(request, user_pk):
    if(request.user.is_guard) or (request.user.is_superuser):
        try:
            user = core_models.User.objects.get(pk=user_pk)
        except core_models.User.DoesNotExist:
            return redirect('guard_view')
        
        bicycle = core_models.Bicycle.objects.get(bicy_user=user)
        context = {
            "run": user.run,
            "email": user.email, 
            "first_name": user.first_name,
            "model": bicycle.model,
            "colour": bicycle.colour,
            "image_url": bicycle.image.url,
            "status": bicycle.is_saved,
        }
        try:
            holder = core_models.BicycleHolder.objects.get(pk=bicycle.holder_pk)
            context["holder"] = True
            context["holder_location"] = holder.nearest_building
            context["holder_x"]= holder.coord_
            context["holder_y"]= holder.coord_y                       
        except core_models.BicycleHolder.DoesNotExist:
            context['holder'] = False
        
        return render(request, 'core/user_details.html', context)
            
@login_required
def emergency_view(request):
    if request.method == "POST":
        message = request.POST["message"]
       
        try:
            new_emergency_ticket = tickets_models.EmergencyTicket(
                user=request.user,
                message=message
            )
        except Exception:
           return render(request, 'core/welcome.html', context={'errormsg': 'Límite de carácteres excedido o Petición Inválida.'})
        
        new_emergency_ticket.save()
        return render(request, 'core/ayuda.html', context={"msg":"Tu asunto fue enviado exitosamente! Nos comunicaremos contigo a la brevedad."})
       
        
    elif request.method == "GET":
        return render(request, 'core/ayuda.html')
