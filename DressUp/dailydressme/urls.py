# dailydressme/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/outfit-recommendation/', views.OutfitRecommendationView.as_view(), name='outfit-recommendation'),
]

