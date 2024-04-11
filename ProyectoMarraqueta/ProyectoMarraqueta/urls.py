from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api", include("picow_api.urls"), name="picow_api"),
    path("", include("core.urls"), name="core"),
    path("auth", include("django.contrib.auth.urls")),
]
