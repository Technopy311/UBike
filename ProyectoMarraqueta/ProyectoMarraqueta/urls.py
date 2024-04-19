from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("core.urls"), name="core"),
    path("api/", include("picow_api.urls"), name="picow_api"),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
