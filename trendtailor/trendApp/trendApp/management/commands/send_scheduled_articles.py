from django.core.management.base import BaseCommand
from trendApp.utils import send_scheduled_articles

class Command(BaseCommand):
    help = 'Send scheduled articles to users based on daily, weekly, monthly schedules'

    def handle(self, *args, **kwargs):
        logs = send_scheduled_articles()

        for log in logs:
            self.stdout.write(self.style.SUCCESS(log))