from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("core.urls")),
    path("api/", include("picow_api.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("appauth.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
