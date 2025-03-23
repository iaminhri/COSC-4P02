from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from UserPreferenceApp.utils import fetch_articles_from_api_1, fetch_articles_from_api_2, fetch_articles_from_api_3
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article 
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from UserPreferenceApp.models import UserPreference, Article
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def home(request):
    topics_and_keywords = {
        "Artificial": ["Artificial", "Intelligence", "AI", "Research", "University", "Medical", "Stock", "Market"],
        "technology": ["web", "development", "softwares", "Blockchain", "Cyber Security", "Internet of Things", "Machine Learning"],
        "Science": ["Experiment", "Theory"],
        "Technology": ["Innovation", "Gadgets"],
        "Health": ["Wellness", "Medicine"],
        "Education": ["Learning", "Schools"],
        "Environment": ["Conservation", "Climate"],
        "Arts": ["Painting", "Sculpture", "Photography"],
        "Business": ["Entrepreneurship", "Startups", "Mergers", "Acquisitions"],
        "Politics": ["Elections", "Legislation", "Diplomacy", "Policies"],
        "Sports": ["Football", "Basketball", "Olympics", "Tennis"],
        "Culture": ["Literature", "Cinema", "Traditions", "Festivals"],
        "Economics": ["Markets", "Stocks", "Trade", "Economic Growth"],
        "Psychology": ["Cognitive", "Behavioral", "Therapy", "Mental Health"],
        "Technology": ["Robotics", "Machine Learning", "Blockchain", "Cybersecurity"],
        "Environment": ["Renewable Energy", "Wildlife Conservation", "Climate Change"],
        "Food": ["Cuisine", "Recipes", "Nutrition", "Veganism"],
        "Travel": ["Destinations", "Adventure", "Cultural Experiences", "Travel Tips"],
        "Fashion": ["Trends", "Designers", "Runways", "Sustainable Fashion"]
    }

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetch_articles_from_api_1([topics], keywords)

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetch_articles_from_api_2([topics], keywords)

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetch_articles_from_api_3([topics], keywords)  

    articles = fetch_all_articles()
    paginator = Paginator(articles, 52)
    pageNumber = request.GET.get('p', 1)
    articlePageObj = paginator.get_page(pageNumber)

    # Fetch user preferences if authenticated
    if request.user.is_authenticated:
        try:
            user_pref = UserPreference.objects.get(user=request.user)
            preferences = user_pref.topics.split(",")  #  Extract topics list
        except UserPreference.DoesNotExist:
            preferences = []
    else:
        preferences = []

    #  Ensure preferences are passed correctly
    return render(request, "home.html", {"articles": articlePageObj, "preferences": preferences})

def fetch_all_articles():
    return Article.objects.all().order_by("id")  

def check_articles(user, topics, keywords):
    query = Q()
    for term in topics + keywords:
        query |= Q(title__icontains=term) | Q(description__icontains=term)

    existingArticles = Article.objects.filter(query)
    return list(existingArticles) if existingArticles.exists() else []

# Email Template Views
def email_template_1(request):
    return render(request, 'email_template_1.html')

def email_template_2(request):
    return render(request, 'email_template_2.html')

def email_template_3(request):
    return render(request, 'email_template_3.html')

def email_template_4(request):
    return render(request, 'email_template_4.html')

def email_template_5(request):
    return render(request, 'email_template_5.html')

# Share article with email templates
@xframe_options_exempt
def share_email(request, article_id, template_id):
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return HttpResponse("Article not found", status=404)

    template_map = {
        1: "share_email1.html",
        2: "share_email2.html",
        3: "share_email3.html",
        4: "share_email4.html",
        5: "share_email5.html",
        6: "share_email6.html",
    }
    
    return render(request, template_map.get(template_id, "share_email1.html"), {"article": article})

def get_template_content(request, article_id, template_id):
    """Fetches the full HTML content of an email template."""
    article = get_object_or_404(Article, id=article_id)

    # Map template IDs to template filenames
    template_map = {
        "1": "share_email1.html",
        "2": "share_email2.html",
        "3": "share_email3.html",
        "4": "share_email4.html",
        "5": "share_email5.html",
        "6": "share_email6.html",
    }
    
    template_name = template_map.get(str(template_id), "share_email1.html") 

    try:
        email_html_content = render_to_string(template_name, {"article": article})
    except:
        email_html_content = "<p>Error loading template</p>"

    return JsonResponse({
        "title": article.title,
        "url": article.url,
        "html_content": email_html_content
    })

@csrf_exempt
@login_required
def send_email(request):
    """Handles sending the email with the generated HTML template."""
    if request.method == "POST":
        try:
            user_email = request.user.email  
            if not user_email:
                return JsonResponse({"error": "Your profile does not have an email set."}, status=400)

            data = json.loads(request.body)
            recipient_email = data.get("email")
            article_title = data.get("title")
            article_url = data.get("url")
            email_body = data.get("email_body", None)  # Generated HTML email content

            if not recipient_email:
                return JsonResponse({"error": "Recipient email is required."}, status=400)

            if email_body:
                # Send email with HTML content
                email = EmailMultiAlternatives(
                    subject=f"Check out this article: {article_title}",
                    body="This email contains an HTML template. Please enable HTML viewing.",  # Fallback text
                    from_email=user_email,
                    to=[recipient_email]
                )
                email.attach_alternative(email_body, "text/html")
                email.send()

            else:
                # Send plain email if no template is selected
                send_mail(
                    subject=f"Check out this article: {article_title}",
                    message=f"Hey! I found this interesting article: {article_url}",
                    from_email=user_email,
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )

            return JsonResponse({"message": "✅ Email with template sent successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# SCRUM 11 - Define 2 SNS content classes (52), html snippet
class InstagramContent:
    def __init__(self, title, caption, image_url, link, hashtags):
        self.title = title
        self.caption = caption
        self.image_url = image_url
        self.link = link
        self.hashtags = hashtags

    def render(self):
        return f"""
        <div style="max-width:600px;margin:auto;background-color:#333;color:white;padding:20px;border-radius:10px;">
            <div style="width:100%;border-radius:10px;">
                <img src="{self.image_url}" alt="Instagram Post Image" style="width:100%;border-radius:10px;">
            </div>
            <h2 style="font-size:32px;margin-top:10px;">{self.title}</h2>
            <p style="font-size:16px;margin-top:10px;">
                {self.caption}<br>
                🔗 <a href="{self.link}" style="color:#8a3ab9;text-decoration:none;">Link in Bio</a>
            </p>
            <p style="color:#8a3ab9;">{self.hashtags}</p>
            <a href="#" style="display:inline-block;padding:10px 20px;background-color:#8a3ab9;color:white;text-decoration:none;border-radius:5px;margin-top:20px;">Share</a>
        </div>
        """

class RedditContent:
    def __init__(self, title, caption, image_url):
        self.title = title
        self.caption = caption
        self.image_url = image_url

    def render(self):
        return f"""
        <div style="max-width:800px;margin:auto;background-color:#272729;color:#d7dadc;padding:20px;border-radius:10px;">
            <p style="font-weight:bold;font-size:28px;margin-bottom:15px;text-align:center;word-wrap:break-word;">
                {self.title}
            </p>
            <div style="text-align:center;margin-bottom:20px;">
                <img src="{self.image_url}" alt="Reddit Post Image" style="width:100%;border-radius:10px;">
            </div>
            <p style="font-size:18px;line-height:1.6;">{self.caption}</p>
            <div style="text-align:center;margin-top:20px;">
                <button onclick="alert('Post link copied to clipboard!')" style="padding:10px 20px;">Share</button>
            </div>
        </div>
        """
    
# SCRUM 11 - Preview SNS content classes (53)
@csrf_exempt
def preview_content(request):
    if request.method == "POST":
        platform = request.POST.get("platform", "")
        title = request.POST.get("title", "")
        caption = request.POST.get("caption", "")
        link = request.POST.get("link", "")
        hashtags = request.POST.get("hashtags", "")

        sns_storage = FileSystemStorage(
            location=os.path.join(settings.MEDIA_ROOT, 'SNS_content'),
            base_url=settings.MEDIA_URL + 'SNS_content/'
        )

        image_file = request.FILES.get("image_file", None)
        if image_file:
            saved_filename = sns_storage.save(image_file.name, image_file)
            image_url = sns_storage.url(saved_filename) 
        else:
            image_url = ""

        if platform == "instagram":
            content_obj = InstagramContent(title, caption, image_url, link, hashtags)
        elif platform == "reddit":
            content_obj = RedditContent(title, caption, image_url)
        else:
            return HttpResponse("Unknown platform", status=400)

        preview_html = content_obj.render()

        return render(request, "preview_SNScontent.html", {
            "preview_html": preview_html,
            "form_data": {
                "platform": platform,
                "title": title,
                "caption": caption,
                "link": link,
                "hashtags": hashtags,
            }
        })
    else:
        return render(request, "preview_SNScontent.html", {
            "preview_html": None,
            "form_data": {}
        })
