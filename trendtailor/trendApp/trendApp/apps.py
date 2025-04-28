import os
import sys
import threading
import time
from django.apps import AppConfig
from django.core.management import call_command
from django.conf import settings

class TrendAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trendApp'

    def ready(self):
        if settings.RUN_SERVER_TASKS:
            # Make sure it's runserver command and the main process
            if self.is_runserver():
                threading.Thread(target=self.run_daily_email, daemon=True).start()
                threading.Thread(target=lambda: call_command('send_scheduled_articles'), daemon=True).start()

    def run_daily_email(self):
        """Runs send_daily_email every 24 hours."""
        while True:
            print("⏰ Sending Daily Email...")
            call_command('send_daily_email')
            time.sleep(86400)  # Sleep 24 hours

    def is_runserver(self):
        """Check if the server is running under runserver command."""
        return (
            os.environ.get('RUN_MAIN') == 'true'
            and len(sys.argv) > 1
            and sys.argv[1] == 'runserver'
        )
