from django.urls import path
from .views import MoodEntryListView
from .views import MoodEntryCreateView, MoodEntryListView

urlpatterns = [
    path('moods/new/', MoodEntryCreateView.as_view(), name='mood_create'),  # Ruta za kreiranje
    path('moods/', MoodEntryListView.as_view(), name='mood_list'),
]
