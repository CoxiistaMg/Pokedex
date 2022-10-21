from django.urls import path
from .views import api_request_search, api_request_found

urlpatterns = [
    path("", api_request_search, name="search"),
    path("/found/", api_request_found, name='found')
]