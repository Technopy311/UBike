from django.urls import path
from . import views as picow_api_views

""" 

Endpoints:

Endopoint: recv.

Description: 

This endpoint is the one which receives the connection from the pico_w module.
There are two other packages underlying this endpoint, "controller" and "auth_user"
"""

urlpatterns = [
    path("recv", picow_api_views.recv, name="picow_recv")
]