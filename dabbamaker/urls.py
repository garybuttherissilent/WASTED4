from django.urls import path
from .views import upload_file, display_map

app_name = 'dabbamaker'


urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('display_map/', display_map, name='display_map'),

]
