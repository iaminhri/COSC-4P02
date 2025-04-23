from django.core.mail import send_mail
from .models import SubscribedUsers
from UserPreferenceApp.models import Article

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


