# dailydressme/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get-outfit/', views.outfit_recommendation_view, name='outfit_recommendation'),
    path('', views.index, name='index'),
    path('api/outfit-recommendation/', views.OutfitRecommendationView.as_view(), name='outfit-recommendation'),
]

