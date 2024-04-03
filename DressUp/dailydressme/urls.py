# dailydressme/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/outfit-recommendation/', views.OutfitRecommendationView.as_view(), name='outfit-recommendation'),
]

