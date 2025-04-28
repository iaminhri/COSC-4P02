from django.core.mail import send_mail
from .models import SubscribedUsers
from UserPreferenceApp.models import Article
from django.conf import settings
from django.utils import timezone
from UserPreferenceApp.models import ScheduledContent

def email_top_article():
    top_article = Article.objects.order_by('-timestamp').first()
    
    if not top_article:
        return "No articles available."

    # Compose email content
    subject = f"Today's Top Article: {top_article.title}"
    message = f"""
    {top_article.title}

    {top_article.description or ''}

    Read more: {top_article.url}
    """

    # Get all subscribed user emails
    recipient_list = list(SubscribedUsers.objects.values_list('email', flat=True))

    # Send email
    send_mail(
        subject,
        message,
        'iamin.hri@email.com',
        recipient_list,
        fail_silently=False,
    )
    return f"Sent to {len(recipient_list)} users."


def should_send_today(schedule_date, today, repeat_option):
    """Check if today matches the scheduled date based on repeat_option."""
    schedule_date = schedule_date.date()
    today = today.date()

    if repeat_option == "none":
        return schedule_date == today

    elif repeat_option == "daily":
        return today >= schedule_date

    elif repeat_option == "weekly":
        delta_days = (today - schedule_date).days
        return delta_days % 7 == 0 and today >= schedule_date

    elif repeat_option == "monthly":
        return schedule_date.day == today.day and today >= schedule_date

    return False

def send_scheduled_articles():
    """Send scheduled articles to users based on their schedule settings."""
    now = timezone.now()
    scheduled_contents = ScheduledContent.objects.select_related('user', 'article')

    results = []  # Collect logs to return

    for schedule in scheduled_contents:
        user = schedule.user
        article = schedule.article
        schedule_date = schedule.schedule_date
        repeat_option = schedule.repeat_option

        if should_send_today(schedule_date, now, repeat_option):
            if user.email:
                subject = f"🔥 Your Scheduled Article: {article.title}"
                message = f"""
                Hello {user.first_name or user.username},

                Here’s the article you scheduled:

                Title: {article.title}
                {article.description or ''}

                Read it here: {article.url}

                Regards,
                Your Website Team
                """.strip()

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                results.append(f"✅ Email sent to {user.email} for '{article.title}'")
            else:
                results.append(f"⚠️ User {user.username} has no email, skipped.")
        else:
            results.append(f"⏩ Not time yet for {user.username} - {repeat_option}")

    return results
