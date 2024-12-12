from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import MoodEntry
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib import messages
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


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # This now handles password hashing
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)  # Log in the user after registration
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "There was an error in your form. Please check the details and try again.")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'tracker/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password, or account is inactive.")
            return redirect('login')  # Optionally, redirect back to login page

    return render(request, 'registration/login.html')

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, get_object_or_404, redirect

@user_passes_test(lambda u: u.is_staff)  # Ensure only staff can access this view
def manage_users(request):
    users = User.objects.all()
    return render(request, 'tracker/manage_users.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)  # Ensure only staff can access this view
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'tracker/edit_user.html', {'form': form, 'user': user})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def delete_user(request, user_id):
    # Check if the logged-in user is an admin
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to perform this action.")

    user = get_object_or_404(User, id=user_id)

    # Delete the user
    user.delete()

    # Redirect to manage users page after deletion
    return redirect('manage_users')

from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)  # Only staff (admins) can access this page
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')  # Redirect back to manage users after creating the user
    else:
        form = UserCreationForm()

    return render(request, 'tracker/create_user.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .forms import MoodForm
from .models import MoodEntry

def edit_mood(request, mood_id):
    mood = get_object_or_404(MoodEntry, id=mood_id)

    # Check if user is admin
    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            # Debugging: print form.errors if any
            print(form.errors)  # This will print to the console if the form isn't valid
            return redirect('mood_list')  # Redirect to the mood list page after saving
        else:
            print("Form is invalid!")
            print(form.errors)
    else:
        form = MoodForm(instance=mood)

    return render(request, 'tracker/edit_mood.html', {'form': form, 'mood': mood})




# Delete mood
def delete_mood(request, mood_id):
    mood = get_object_or_404(MoodEntry, pk=mood_id)

    # Check if user is admin
    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == 'POST':
        mood.delete()
        return redirect('mood_list')  # Redirect to the mood list page

    return render(request, 'confirm_delete_mood.html', {'mood': mood})
