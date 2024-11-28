from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import MoodEntry
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class MoodEntryListView(ListView):
    model = MoodEntry
    template_name = 'tracker/moodentry_list.html'
def home(request):
    return render(request, 'home.html')

class MoodEntryCreateView(LoginRequiredMixin, CreateView):
    model = MoodEntry
    fields = ['mood', 'note']
    template_name = 'tracker/moodentry_form.html'
    success_url = reverse_lazy('mood_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatski dodeljuje trenutnog korisnika
        return super().form_valid(form)