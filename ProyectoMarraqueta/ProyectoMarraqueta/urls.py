from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("core.urls")),
    path("api/", include("picow_api.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("appauth.urls"))
]
