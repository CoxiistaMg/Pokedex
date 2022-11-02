
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('api_search', include('api.urls')),
    path("", include("pokedex.urls"), name="index")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
