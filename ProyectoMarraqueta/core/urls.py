from django.urls import path
from . import views as core_views

urlpatterns = [
    path("emergency_view", core_views.emergency_view, name="emergency_view"),
    path("user_view", core_views.user_view, name="user_view"),
    path("guard_view", core_views.guard_view, name="guard_view"),
    path("", core_views.welcome_view, name="welcome_view")
]