from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, ProfileImage
from UserPreferenceApp.models import Article, ScheduledContent
import os
from datetime import datetime
from django.utils import timezone

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="StrongPass123")
    
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'bademail',
            'password1': '123',
            'password2': '456'
        })
        self.assertEqual(response.status_code, 200)  # Form invalid, stay on page

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_dashboard_access_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_access_with_login(self):
        self.client.login(username="testuser", password="StrongPass123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        self.client.login(username="testuser", password="StrongPass123")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="StrongPass123")
        self.client.login(username="testuser", password="StrongPass123")
    
    def test_profile_update(self):
        response = self.client.post(reverse('edit_profile'), {
            'role': 'Developer',
            'phone_number': '1234567890',
            'bio': 'Software Engineer',
            'street_address': '123 Main St',
            'city': 'Toronto',
            'province': 'ON',
            'postal_code': 'M1M1M1',
            'birth_date': '2000-01-01'
        })
        self.assertEqual(response.status_code, 200)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.city, 'Toronto')

    def test_edit_profile_image(self):
        with open('test_image.jpg', 'wb') as f:
            f.write(b'\x00\x01')

        with open('test_image.jpg', 'rb') as img:
            response = self.client.post(reverse('edit_image'), {'image': img})
        self.assertEqual(response.status_code, 302)

    def test_settings_page(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

class ScheduleContentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="StrongPass123")
        self.client.login(username="testuser", password="StrongPass123")
        self.article = Article.objects.create(title="Scheduled Article", url="https://example.com")

    def test_schedule_content_success(self):
        schedule_date = (timezone.now() + timezone.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(reverse('schedule_content'), {
            'content_id': str(self.article.id),
            'schedule_date': schedule_date,
            'repeat_option': 'daily'
        })
        self.assertEqual(response.status_code, 200)

    def test_edit_schedule(self):
        schedule = ScheduledContent.objects.create(
            user=self.user,
            article=self.article,
            schedule_date=timezone.now(),
            repeat_option='none'
        )
        new_date = (timezone.now() + timezone.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(reverse('edit_schedule'), {
            'schedule_id': schedule.id,
            'schedule_date': new_date,
            'repeat_option': 'weekly'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_schedule(self):
        schedule = ScheduledContent.objects.create(
            user=self.user,
            article=self.article,
            schedule_date=timezone.now(),
            repeat_option='none'
        )
        response = self.client.get(reverse('delete_schedule', args=[schedule.id]))
        self.assertEqual(response.status_code, 302)

class SummarizationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="StrongPass123")
        self.client.login(username="testuser", password="StrongPass123")

    def test_summarization_page_get(self):
        response = self.client.get(reverse('summarization'))
        self.assertEqual(response.status_code, 200)

    def test_summarization_submit_text(self):
        response = self.client.post(reverse('summarization'), {
            'textInput': 'This is a long article that needs to be summarized.'
        })
        self.assertEqual(response.status_code, 200)