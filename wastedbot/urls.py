from django.urls import path
from . import views

app_name = 'wastedbot'

urlpatterns = [
    path('', views.index, name='index'),
]
