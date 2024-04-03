# dailydressme/views.py

from django.http import JsonResponse
import os
import random
from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUrlSerializer
from django.shortcuts import render


# Assuming your existing functions are defined in this file
# If not, import them from their respective module

OPENWEATHERMAP_API_KEY = 'd2a2b4ae87b93c165c5421cee9970939'

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
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

class OutfitRecommendationView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'Beirut')
        try:
            temperature = get_weather_data(city)
            image_url = get_outfit_image(temperature)
            serializer = ImageUrlSerializer(data={'image_url': image_url})
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

