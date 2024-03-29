"""
URL configuration for wastedproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # assuming 'api' is the name of your app
    path('', views.homepage, name='homepage'),  # root URL maps to your new homepage view
    path('streetseeker/', include('streetseeker2.urls')),
    path('shiftscheduler/', include('shiftscheduler.urls')),
    path('dabbamaker/', include('dabbamaker.urls')),
    path('analytics/', include('analytics.urls')),
    path('wastedbot/', include('wastedbot.urls')),
    path('complaintorganizer/', include('complaintorganizer.urls')),
    path('complaintpreparator/', include('complaintpreparator.urls')),
    path('routenotfinished/', include('routenotfinished.urls')),
    path('vehicleseeker2/', include('vehicleseeker2.urls')),


]
