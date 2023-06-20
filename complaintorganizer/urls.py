from .views import download_complaints
from django.urls import path

app_name = 'complaintorganizer'

urlpatterns = [
    path('download-complaints/', download_complaints, name='download_complaints'),
]
