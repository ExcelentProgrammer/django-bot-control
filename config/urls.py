from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("control.urls")),
    path("sponsors/",include("sponsors.urls")),
    path("accounts/",include("django.contrib.auth.urls")),

    re_path(r"media/(.*)", serve, {"document_root": settings.MEDIA_ROOT}),
]
