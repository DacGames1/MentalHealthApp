from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import MoodEntry, User
from .forms import MoodForm, UserRegistrationForm, UserProfileForm

# Home view
def home(request):
    return render(request, 'home.html')

# ListView for Mood Entries - Restricted to user-specific entries or all for staff
from django.shortcuts import render
from django.views.generic import ListView
from .models import MoodEntry
from django.db.models import Q

class MoodEntryListView(ListView):
    model = MoodEntry
    template_name = 'tracker/mood_list.html'  # Update this path if necessary
    context_object_name = 'object_list'

    def get_queryset(self):
        # Start with the moods of the logged-in user
        queryset = MoodEntry.objects.filter(user=self.request.user)

        # Filter by mood (if provided)
        mood = self.request.GET.get('mood')
        if mood:
            queryset = queryset.filter(mood__icontains=mood)

        # Filter by note (if provided)
        note = self.request.GET.get('note')
        if note:
            queryset = queryset.filter(note__icontains=note)

        # Sorting by date (if provided)
        sort_by_date = self.request.GET.get('sort_by_date')
        if sort_by_date == 'desc':
            queryset = queryset.order_by('-date')
        else:
            queryset = queryset.order_by('date')

        return queryset




# CreateView for Mood Entries
class MoodEntryCreateView(LoginRequiredMixin, CreateView):
    model = MoodEntry
    fields = ['mood', 'note']
    template_name = 'tracker/moodentry_form.html'
    success_url = reverse_lazy('mood_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# User Registration
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "There was an error in your form. Please check the details.")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'tracker/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# User Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'registration/login.html')

# Manage Users - Staff Only
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)  # Ensure only staff can access this view
def manage_users(request):
    # Start by getting all users
    users = User.objects.all()

    # Search by username if provided
    username = request.GET.get('username')
    if username:
        users = users.filter(username__icontains=username)

    # Sorting based on filter
    filter_option = request.GET.get('filter')
    if filter_option == 'date_created':
        users = users.order_by('-date_joined')  # Most recent
    elif filter_option == 'date_created_least':
        users = users.order_by('date_joined')  # Least recent

    return render(request, 'tracker/manage_users.html', {'users': users})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CustomUserChangeForm
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.is_staff)  # ✅ Samo staff može editovati
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)  # ✅ Koristi CustomUserChangeForm
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully!")  # ✅ Dodana poruka
            return redirect('manage_users')  # ✅ Sada će te vratiti nazad
        else:
            messages.error(request, "Error updating user. Please check the form.")  # ✅ Ako ima grešaka
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'tracker/edit_user.html', {'form': form, 'user': user})




# Delete User - Staff Only
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to perform this action.")

    # Get the user object to be deleted
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Delete the user and redirect to manage users page
        user.delete()
        return redirect('manage_users')

    # GET request: Render confirmation page
    return render(request, 'tracker/confirm_delete_user.html', {'user': user})




# Create User - Staff Only
@user_passes_test(lambda u: u.is_staff)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserCreationForm()

    return render(request, 'tracker/create_user.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import MoodEntry
from .forms import MoodForm

def edit_mood_entry(request, mood_id):
    # Get the mood entry by its ID
    mood_entry = get_object_or_404(MoodEntry, id=mood_id)

    # Check if the logged-in user is the one who created the mood entry or if the user is an admin
    if mood_entry.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to edit this mood entry.")

    if request.method == "POST":
        form = MoodForm(request.POST, instance=mood_entry)
        if form.is_valid():
            form.save()

            # Redirect based on user type
            if request.user.is_staff:
                return redirect('user_mood_entries', user_id=mood_entry.user.id)  # Admin redirection
            else:
                return redirect('mood_list')  # Regular user redirection to their own mood list

    else:
        form = MoodForm(instance=mood_entry)

    return render(request, 'tracker/edit_mood.html', {'form': form, 'mood_entry': mood_entry})





# Delete Mood Entry - Staff Only
from django.shortcuts import get_object_or_404, redirect, render
from .models import MoodEntry
from django.http import HttpResponseForbidden

def delete_mood(request, mood_id):
    entry = get_object_or_404(MoodEntry, id=mood_id)

    # Check if the logged-in user is the one who created the mood entry
    if entry.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this mood entry.")

    if request.method == 'POST':
        user_id = entry.user.id
        entry.delete()

        # If admin, redirect to the user's mood entries
        if request.user.is_staff:
            return redirect('user_mood_entries', user_id=user_id)
        else:
            # Regular user, redirect to the general mood list
            return redirect('mood_list')

    return render(request, 'tracker/confirm_delete.html', {'entry': entry, 'type': 'mood'})




# Admin Mood Entry List - Staff Only
def admin_mood_entry_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    mood_entries = MoodEntry.objects.all()
    return render(request, 'tracker/admin_mood_entry_list.html', {'mood_entries': mood_entries})

# User Mood Entries
def user_mood_entries(request, user_id):
    user = get_object_or_404(User, id=user_id)
    mood_entries = MoodEntry.objects.filter(user=user)
    return render(request, 'tracker/user_mood_entries.html', {'user': user, 'mood_entries': mood_entries})
