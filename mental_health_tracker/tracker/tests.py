from django.test import TestCase, Client
from django.contrib.auth.models import User
from tracker.models import MoodEntry, UserProfile, Activity
from tracker.forms import MoodForm
from django.urls import reverse

class MoodEntryTests(TestCase):

    def setUp(self):
        """ Kreiranje testnog korisnika i unosa raspoloženja """
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.mood_entry = MoodEntry.objects.create(
            user=self.user,
            mood="Happy",
            note="Feeling great today!"
        )

    def test_mood_entry_creation(self):
        """ Testira je li unos raspoloženja ispravno kreiran """
        self.assertEqual(self.mood_entry.mood, "Happy")
        self.assertEqual(self.mood_entry.user.username, "testuser")

    def test_mood_list_view(self):
        """ Testira prikaz liste raspoloženja za prijavljenog korisnika """
        response = self.client.get(reverse("mood_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Happy")  # Da li prikazuje raspoloženje?

    def test_mood_form_valid(self):
        """ Testira je li forma za unos raspoloženja validna """
        form_data = {
            "user": self.user.id,  # Obavezno polje
            "mood": "Sad",
            "note": "Not a great day"
        }
        form = MoodForm(data=form_data)
        print("Form errors:", form.errors)  # Debugging
        self.assertTrue(form.is_valid())




    def test_mood_entry_edit(self):
        """ Testira može li korisnik urediti svoj unos """
        response = self.client.post(reverse("edit_mood", args=[self.mood_entry.id]), {
            "mood": "Neutral",
            "note": "Feeling okay."
        }, follow=True)

        self.mood_entry.refresh_from_db()
        print("Mood after edit:", self.mood_entry.mood)  # Debugging
        print("Response status:", response.status_code)
        print("Response content:", response.content)

    def test_mood_entry_delete(self):
        """ Testira može li korisnik obrisati svoj unos """
        response = self.client.post(reverse("delete_mood", args=[self.mood_entry.id]))
        self.assertEqual(response.status_code, 302)  # Redirect nakon brisanja
        self.assertFalse(MoodEntry.objects.filter(id=self.mood_entry.id).exists())

class UserAuthTests(TestCase):

    def setUp(self):
        """ Kreiranje testnog korisnika """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login(self):
        """ Testira može li se korisnik prijaviti """
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 302)  # Redirect nakon prijave

    """def test_register(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "age": 25,
            "gender": "Male",
            "bio": "Testing user registration."
        }, follow=True)

        self.assertTrue(User.objects.filter(username="newuser").exists())"""


class AdminTests(TestCase):

    def setUp(self):
        """ Kreira admin korisnika i običnog korisnika """
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="admin", password="adminpass")

    def test_admin_can_delete_user(self):
        """ Testira može li admin obrisati korisnika """
        response = self.client.post(reverse("delete_user", args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_non_admin_cannot_delete_user(self):
        """ Testira da običan korisnik ne može obrisati druge korisnike """
        self.client.logout()
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("delete_user", args=[self.admin.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

