import requests

def get_weather_data():
    # API key
    api_key = "00c79b3186249ab2cdc9a9fde3aa21f5"
    city = "Ghent"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    # Convert temperature from Kelvin to Celsius
    temperature_celsius = round(data['main']['temp'] - 273.15, 2)
    temperature_celsius_feel = round(data['main']['feels_like'] - 273.15, 2)

    weather_data = {
        "city": city,
        "temperature": temperature_celsius,
        "description": data['weather'][0]['description'],
        "icon": data['weather'][0]['icon'],
        "wind": data['wind']['speed'],
        "humidity": data['main']['humidity'],
        "rain": data.get('rain', {}).get('1h', 'No rain'),
        "feels_like": temperature_celsius_feel
    }

    return weather_data




