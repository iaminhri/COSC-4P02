from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from UserPreferenceApp.models import Article, UserPreference
from UserPreferenceApp.forms import UserPreferenceForm

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
