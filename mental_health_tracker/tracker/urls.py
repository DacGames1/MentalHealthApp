from . import views
from django.urls import path
from .views import MoodEntryCreateView, MoodEntryListView, register,manage_users, edit_user


urlpatterns = [
    path('moods/new/', MoodEntryCreateView.as_view(), name='mood_create'),
    path('moods/', MoodEntryListView.as_view(), name='mood_list'),
    path('register/', register, name='register'),  # URL pattern for registration
     path('manage-users/', manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
