from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']  # Only username and email are collected

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return password_confirmation

    def save(self, commit=True):
        # Save the User object first
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)  # Hash the password before saving
        if commit:
            user.save()  # Save the user to the database
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'bio']
