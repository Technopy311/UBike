from django.urls import path
from . import views as core_views

urlpatterns = [
    path("user_view", core_views.user_view, name="user_view"),
    path("user_register", core_views.user_register, name="user_register"),
    path("guard_view", core_views.guard_view, name="guard_view"),
    path("", core_views.welcome_view, name="welcome_view")
]