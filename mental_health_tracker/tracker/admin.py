from django.contrib import admin
from .models import UserProfile, MoodEntry, Activity

admin.site.register(UserProfile)
admin.site.register(MoodEntry)
admin.site.register(Activity)
