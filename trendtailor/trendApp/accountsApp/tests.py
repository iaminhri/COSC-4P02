from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, ProfileImage

class UserAuthenticationTests(TestCase):
    def setUp(self):
        """Set up a test user"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="StrongPass123")
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to login page
        self.assertTrue(User.objects.filter(username='newuser').exists())  # User should exist

    def test_login_user(self):
        """Test user login"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to dashboard
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)  # Check if logged in

    def test_dashboard_access_without_login(self):
        """Test if unauthenticated users are redirected"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to home

    def test_dashboard_access_with_login(self):
        """Test dashboard access for authenticated users"""
        self.client.login(username="testuser", password="StrongPass123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Should load successfully

    def test_logout_user(self):
        """Test user logout"""
        self.client.login(username="testuser", password="StrongPass123")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Expecting redirect to login
        self.assertNotIn('_auth_user_id', self.client.session)  # Ensure user is logged out

class ProfileTests(TestCase):
    def setUp(self):
        """Create test user and profile"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="StrongPass123")
        self.client.login(username="testuser", password="StrongPass123")
    
    # def test_profile_creation_on_registration(self):
        """Test if a profile is created when a user registers"""
       # self.assertTrue(Profile.objects.filter(user=self.user).exists())
       # self.assertTrue(ProfileImage.objects.filter(user=self.user).exists())

    def test_profile_update(self):
        """Test profile update form submission"""
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
        self.assertEqual(response.status_code, 200)  # Expecting success
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.city, 'Toronto')  # Profile should be updated

    def test_profile_image_upload(self):
        """Test profile image upload"""
        with open('test_image.jpg', 'wb') as f:  # Create a dummy image file
            f.write(b'\x00\x01')  

        with open('test_image.jpg', 'rb') as img:
            response = self.client.post(reverse('edit_image'), {'image': img})
        
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertTrue(ProfileImage.objects.filter(user=self.user).exists())  # Image should exist
