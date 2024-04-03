# dailydressme/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/outfit-recommendation/', views.OutfitRecommendationAPIView.as_view(), name='outfit-recommendation'),
]

