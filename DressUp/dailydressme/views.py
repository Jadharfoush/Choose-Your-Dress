from django.shortcuts import render
import os
import random
import requests
from django.conf import settings
from .serializers import ImageUrlSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

OPENWEATHERMAP_API_KEY = 'd2a2b4ae87b93c165c5421cee9970939'  # Replace with your actual API key

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print("Received data:", data)
    return data['main']['temp']

def get_outfit_image(temperature):
    if temperature < 10:
        folder = 'cold'
    elif 10 <= temperature < 20:
        folder = 'mild'
    else:
        folder = 'warm'
    
    dir_path = os.path.join(settings.MEDIA_ROOT, folder)
    images = os.listdir(dir_path)
    image_file = random.choice(images)
    image_url = settings.MEDIA_URL + os.path.join(folder, image_file)
    return image_url
    
def home(request):
    return render(request, 'home.html')

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city', 'Beirut')
        try:
            temperature = get_weather_data(city)
            image_url = get_outfit_image(temperature)
            context = {
                'city': city,
                'temperature': temperature,
                'image_url': image_url,
            }
            return render(request, 'index.html', context)
        except requests.RequestException as e:
            context = {'error': str(e)}
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

class OutfitRecommendationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        city = request.data.get('city', 'Beirut')
        try:
            temperature = get_weather_data(city)
            image_url = get_outfit_image(temperature)
            serializer = ImageUrlSerializer(data={'image_url': image_url})
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TemperatureAPIView(APIView):
    def post(self, request, *args, **kwargs):
        city = request.data.get('city', 'oslo')  # Default to Beirut if no city is provided
        try:
            temperature = get_weather_data(city)
            print(f"Temperature in {city}: {temperature}")
            return Response({'temperature': temperature})
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)