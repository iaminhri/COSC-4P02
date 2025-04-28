from django.core.management.base import BaseCommand
from trendApp.utils import email_top_article

class Command(BaseCommand):
    help = 'Send top article to all subscribed users via email'

    def handle(self, *args, **kwargs):
        result = email_top_article()
        self.stdout.write(self.style.SUCCESS(result))
