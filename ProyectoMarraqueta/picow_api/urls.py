from django.urls import path
from . import views as picow_api_views

urlpatterns = [
    path("recv", picow_api_views.recv, name="picow_recv"),
    path("auth_user", picow_api_views.auth_user, name="picow_auth"),
    path("controller", picow_api_views.controller, name="picow_controller")
]