import os
import random
import requests
from django.http import JsonResponse
from django.conf import settings

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


# You need to sign up for OpenWeatherMap to get an API key and add it here
OPENWEATHERMAP_API_KEY = 'd2a2b4ae87b93c165c5421cee9970939'

def get_weather_data(city):
    # Constructs the URL to fetch the weather data
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'  # units can be 'metric' or 'imperial'
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    data = response.json()
    return data['main']['temp']  # Returns the current temperature

def get_outfit_image(temperature):
    # Depending on the temperature, you will select a folder
    if temperature < 10:  # Celsius
        folder = 'cold'
    elif 10 <= temperature < 20:
        folder = 'mild'
    else:
        folder = 'warm'

    # Get the directory for the selected folder
    dir_path = os.path.join(settings.MEDIA_ROOT, folder)
    images = os.listdir(dir_path)
    # Choose a random image
    image_file = random.choice(images)
    image_url = settings.MEDIA_URL + os.path.join(folder, image_file)
    return image_url

def outfit_recommendation_view(request):
    city = request.GET.get('city', 'Beirut')  # Default to London if no city is provided in the request
    try:
        # Fetch the weather data
        temperature = get_weather_data(city)
        # Fetch a random image based on the temperature
        image_url = get_outfit_image(temperature)
        return JsonResponse({'image_url': image_url})
    except requests.RequestException as e:
        # If the weather API call fails, return an error message
        return JsonResponse({'error': str(e)}, status=500)


        
