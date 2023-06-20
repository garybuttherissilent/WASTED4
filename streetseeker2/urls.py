from django.urls import path
from . import views

app_name = 'streetseeker2'


urlpatterns = [
    path('', views.search_street, name='streetseeker'),


]

