from django.urls import path
from .views import file_upload

app_name = 'shiftscheduler'

urlpatterns = [
    path('', file_upload, name='shiftscheduler'),
]
