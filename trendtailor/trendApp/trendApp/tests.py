from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from UserPreferenceApp.models import Article, UserPreference
from UserPreferenceApp.forms import UserPreferenceForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import json


class HomePageTests(TestCase):
    """Test cases for the homepage functionality."""

    def setUp(self):
        """Set up a test user, preferences, and sample articles."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create user preferences
        self.user_pref = UserPreference.objects.create(
            user=self.user,
            sources="CNN,BBC",
            topics="Technology,Science",
            keywords="AI,Quantum Computing"
        )

        # Create test articles
        for i in range(55):  # Ensuring pagination works correctly
            Article.objects.create(
                title=f"Tech News {i}",
                description=f"Tech article {i} description",
                url=f"https://example.com/news{i}",
                urlToImage="https://example.com/image.jpg"
            )

    def test_homepage_access(self):
        """Ensure the homepage loads correctly."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Featured Articles")

    def test_homepage_shows_preferences(self):
        """Verify that user preferences appear on the homepage."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Technology")
        self.assertContains(response, "Science")
        self.assertContains(response, "AI")

    def test_homepage_pagination(self):
        """Ensure pagination works and displays the correct articles per page."""
        response = self.client.get(reverse("home") + "?p=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech News 0")
        self.assertContains(response, "Tech News 49")  # Should show first 50 articles

        response_page_2 = self.client.get(reverse("home") + "?p=2")
        self.assertContains(response_page_2, "Tech News 50")  # Next page should contain remaining articles


class PreferenceTests(TestCase):
    """Tests related to updating and saving user preferences."""

    def setUp(self):
        """Set up a test user."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_update_preferences(self):
        """Ensure users can update their news preferences."""
        response = self.client.post(reverse("preferences"), {
            "sources": "TechCrunch",
            "topics": "AI, Blockchain",
            "keywords": "Machine Learning, Quantum"
        })
        self.assertEqual(response.status_code, 200)

        # Verify the database is updated
        updated_pref = UserPreference.objects.get(user=self.user)
        self.assertEqual(updated_pref.sources, "TechCrunch")
        self.assertEqual(updated_pref.topics, "AI, Blockchain")


class ArticleStorageTests(TestCase):
    """Tests for verifying stored content in the database."""

    def setUp(self):
        """Set up test user and stored articles."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")

        self.article1 = Article.objects.create(
            title="AI Breakthrough",
            description="A major AI breakthrough was announced.",
            url="https://example.com/ai",
            urlToImage="https://example.com/image.jpg"
        )
        self.article2 = Article.objects.create(
            title="Quantum Computing Update",
            description="Quantum computing is advancing fast.",
            url="https://example.com/quantum",
            urlToImage=None
        )

    def test_articles_saved_in_database(self):
        """Ensure articles are correctly stored and retrieved."""
        articles = Article.objects.all()
        self.assertEqual(articles.count(), 2)

    def test_articles_show_on_homepage(self):
        """Ensure stored articles appear on the homepage."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "AI Breakthrough")
        self.assertContains(response, "Quantum Computing Update")


class PaginationTests(TestCase):
    """Test cases to ensure pagination works properly."""

    def setUp(self):
        """Create a test user and multiple articles."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")

        for i in range(55):  # Creating 55 articles
            Article.objects.create(
                title=f"Tech News {i}",
                description=f"Tech article {i} description",
                url=f"https://example.com/news{i}",
                urlToImage=None
            )

    def test_pagination(self):
        """Ensure the pagination displays correct number of articles per page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("home") + "?p=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech News 0")
        self.assertContains(response, "Tech News 49")  # Should show first 50 articles

        response_page_2 = self.client.get(reverse("home") + "?p=2")
        self.assertContains(response_page_2, "Tech News 50")  # Next page should contain remaining articles


class EmailTemplateTests(TestCase):
    """Tests for Sprint 3: Email templates and article sharing"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.client.login(username="testuser", password="password123")

        self.article = Article.objects.create(
            title="Email Test Article",
            description="This is a test description for email template.",
            url="https://example.com/test-article",
            #urlToImage="https://example.com/image.jpg"
        )

    def test_email_template_views(self):
        """Check if all email template views return 200"""
        for i in range(1, 6):  # email-T1 to email-T5
            response = self.client.get(reverse(f"email_T{i}"))
            self.assertEqual(response.status_code, 200, f"Failed at email_T{i}")

    def test_share_email_view(self):
        """Ensure share_email view renders correctly with article and template"""
        response = self.client.get(reverse("share_email", args=[self.article.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome to TrendTailor", response.content.decode())

    def test_get_template_content_ajax(self):
        """Check if AJAX call for getting email template content works"""
        response = self.client.get(reverse("get_template_content", args=[self.article.id, 1]))
        data = response.json()
        self.assertIn("html_content", data)
        self.assertIn(self.article.title, data["html_content"])

    def test_send_email_post(self):
        """Simulate sending an email with article and template content"""
        response = self.client.post(
            reverse("send_email"),
            data=json.dumps({
                "email": "recipient@example.com",
                "title": self.article.title,
                "url": self.article.url,
                "email_body": "<p>This is a test email</p>"
            }),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

class SNSPreviewTests(TestCase):
    """Test SNS content generation and preview page functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="snsuser", password="testpass")
        self.client.login(username="snsuser", password="testpass")

    def test_preview_page_get(self):
        """Ensure the preview page loads with a GET request."""
        response = self.client.get(reverse("preview_content"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preview Content")

    def test_instagram_preview_post(self):
        """Test SNS preview for Instagram with form data."""
        with open(os.path.join(os.path.dirname(__file__), 'test_image.jpg'), 'rb') as img:
            image = SimpleUploadedFile("test.jpg", img.read(), content_type="image/jpeg")
            response = self.client.post(reverse("preview_content"), {
                "platform": "instagram",
                "title": "Insta Title",
                "caption": "Cool caption",
                "link": "https://example.com",
                "hashtags": "#AI #Tech",
                "image_file": image
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insta Title")
        self.assertContains(response, "#AI #Tech")
        self.assertContains(response, "Link in Bio")

    def test_reddit_preview_post(self):
        """Test SNS preview for Reddit with form data."""
        with open(os.path.join(os.path.dirname(__file__), 'test_image.jpg'), 'rb') as img:
            image = SimpleUploadedFile("test.jpg", img.read(), content_type="image/jpeg")
            response = self.client.post(reverse("preview_content"), {
                "platform": "reddit",
                "title": "Reddit Title",
                "caption": "Reddit description here",
                "image_file": image
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reddit Title")
        self.assertContains(response, "Reddit description here")

    def test_preview_invalid_platform(self):
        """Test that invalid platform returns 400."""
        response = self.client.post(reverse("preview_content"), {
        "platform": "myspace",  # Invalid platform
        "title": "Should Fail"
             })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unknown platform", response.content.decode())