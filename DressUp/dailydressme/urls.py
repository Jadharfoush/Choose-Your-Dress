# dailydressme/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
        path('', views.home, name='home'),

    
    path('api/outfit-recommendation/', views.OutfitRecommendationAPIView.as_view(), name='outfit-recommendation'),
    path('api/temperature', views.TemperatureAPIView.as_view(), name='api-temperature'),
]

