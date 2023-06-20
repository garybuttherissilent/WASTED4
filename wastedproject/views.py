from django.shortcuts import render
from weather.views import get_weather_data

def homepage(request):
    weather_data = get_weather_data()
    return render(request, 'homepage.html', weather_data)
