from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import MoodEntry
from django.urls import reverse_lazy

class MoodEntryListView(ListView):
    model = MoodEntry
    template_name = 'tracker/moodentry_list.html'
def home(request):
    return HttpResponse("<h1>Dobrodošli u aplikaciju za praćenje mentalnog zdravlja!</h1>")

class MoodEntryCreateView(CreateView):
    model = MoodEntry
    fields = ['mood', 'note']  # Polja koja će se prikazati u formi
    template_name = 'tracker/moodentry_form.html'  # Lokacija šablona
    success_url = reverse_lazy('mood_list')  # URL na koji se preusmerava nakon uspešnog unosa