from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from UserPreferenceApp.models import Article, UserPreference
from trendApp.models import ArchivedContent
from django.core.files.uploadedfile import SimpleUploadedFile
import json
import os

class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        for i in range(55):
            Article.objects.create(
                title=f"Tech News {i}",
                description=f"Tech article {i} description",
                url=f"https://example.com/news{i}",
            )

    def test_homepage_access(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_pagination(self):
        response = self.client.get(reverse("home") + "?p=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech News 0")

        response_page_2 = self.client.get(reverse("home") + "?p=2")
        self.assertEqual(response_page_2.status_code, 200)
        self.assertContains(response_page_2, "Tech News 52")  # Adjusted from 50 to 52

    def test_homepage_shows_articles(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Tech News 0")


class PreferenceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_update_preferences(self):
        response = self.client.post(reverse("preferences"), {
            "sources": "TechCrunch",
            "topics": "AI, Blockchain",
            "keywords": "Machine Learning, Quantum"
        })
        self.assertEqual(response.status_code, 200)


class ArticleStorageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")

        self.article1 = Article.objects.create(
            title="AI Breakthrough",
            description="A major AI breakthrough was announced.",
            url="https://example.com/ai"
        )
        self.article2 = Article.objects.create(
            title="Quantum Computing Update",
            description="Quantum computing is advancing fast.",
            url="https://example.com/quantum"
        )

    def test_articles_saved_in_database(self):
        articles = Article.objects.all()
        self.assertEqual(articles.count(), 2)

    def test_articles_show_on_homepage(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "AI Breakthrough")


class PaginationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")

        for i in range(55):
            Article.objects.create(
                title=f"Tech News {i}",
                description=f"Tech article {i} description",
                url=f"https://example.com/news{i}"
            )

    def test_pagination(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("home") + "?p=1")
        self.assertEqual(response.status_code, 200)

        response_page_2 = self.client.get(reverse("home") + "?p=2")
        self.assertEqual(response_page_2.status_code, 200)
        self.assertContains(response_page_2, "Tech News 52")


class EmailTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.client.login(username="testuser", password="password123")

        self.article = Article.objects.create(
            title="Email Test Article",
            description="This is a test description for email template.",
            url="https://example.com/test-article",
        )

    def test_email_template_views(self):
        for i in range(1, 6):
            response = self.client.get(reverse(f"email_T{i}"))
            self.assertEqual(response.status_code, 200)

    def test_share_email_view(self):
        response = self.client.get(reverse("share_email", args=[self.article.id, 1]))
        self.assertEqual(response.status_code, 200)

    def test_get_template_content_ajax(self):
        response = self.client.get(reverse("get_template_content", args=[self.article.id, 1]))
        data = response.json()
        self.assertIn("html_content", data)


class SNSPreviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="snsuser", password="testpass")
        self.client.login(username="snsuser", password="testpass")

    def test_preview_page_get(self):
        response = self.client.get(reverse("preview_content"))
        self.assertEqual(response.status_code, 200)

    def test_preview_invalid_platform(self):
        response = self.client.post(reverse("preview_content"), {
            "platform": "myspace",
            "title": "Should Fail"
        })
        self.assertEqual(response.status_code, 400)


class ContentSchedulingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        self.archived_content = ArchivedContent.objects.create(
            user=self.user,
            title="Test Archived Title",
            content="Sample archived content",
            platform="newsletter",
            image_url="https://example.com/testimage.jpg",
            url="https://example.com/article"
        )

    def test_successful_archive_content(self):
        response = self.client.post(reverse("archive_content"), {
            "title": "New Archived Title",
            "content": "Archived content body",
            "platform": "newsletter",
            "image_url": "https://example.com/newimage.jpg",
            "url": "https://example.com/newarticle"
        })
        self.assertEqual(response.status_code, 200)

    def test_archive_content_missing_fields(self):
        response = self.client.post(reverse("archive_content"), {
            "title": "",
            "content": "",
        })
        self.assertNotEqual(response.status_code, 500)

    def test_successful_unarchive_content(self):
        response = self.client.post(reverse("unarchive_content", args=[self.archived_content.id]))
        self.assertEqual(response.status_code, 200)

    def test_unarchive_invalid_content_id(self):
        response = self.client.post(reverse("unarchive_content", args=[9999]))
        self.assertIn(response.status_code, [200, 400])

    def test_view_archived_contents(self):
        response = self.client.get(reverse("archived_contents"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Archived Title")

    def test_export_archived_contents_pdf(self):
        response = self.client.get(reverse("export_archived_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), "application/pdf")