from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from UserPreferenceApp.utils import fetch_articles_from_api_1, fetch_articles_from_api_3
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article 
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import ScheduledContent  
from django.utils import timezone  
from datetime import datetime

print("Loading views.py...")

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

    articles = fetch_all_articles()
    paginator = Paginator(articles, 52)
    pageNumber = request.GET.get('p', 1)
    articlePageObj = paginator.get_page(pageNumber)

    return render(request, 'home.html', {"articles": articlePageObj})

def fetch_all_articles():
    return Article.objects.all()

def check_articles(user, topics, keywords):
    query = Q()
    for term in topics + keywords:
        query |= Q(title__icontains=term) | Q(description__icontains=term)

    existingArticles = Article.objects.filter(query)
    return list(existingArticles) if existingArticles.exists() else []

# Dashboard View (With Scheduling Feature)
@login_required
def dashboard(request):
    articles = Article.objects.all()
    scheduled_contents = ScheduledContent.objects.filter(user=request.user).order_by("schedule_date")
    return render(request, "dashboard.html", {"articles": articles, "scheduled_contents": scheduled_contents})

# Schedule Content View 
@login_required
def schedule_content(request):
    if request.method == "POST":
        print("RAW POST Data:", request.POST)

        content_id = request.POST.get("content_id")
        print(f"Received content_id before processing: {repr(content_id)}")

        schedule_date = request.POST.get("schedule_date")
        repeat_option = request.POST.get("repeat_option", "none")

        if not content_id or not schedule_date:
            return JsonResponse({"error": "Missing content ID or schedule date"}, status=400)

        try:
            content_id = content_id.strip().replace("'", "").replace('"', '')  
            if not content_id.isdigit():
                return JsonResponse({"error": f"Invalid article ID format: '{content_id}'"}, status=400)

            article_id = int(content_id)
            print(f"✅ Successfully converted to article_id: {article_id}")
            article = get_object_or_404(Article, id=article_id)
            print(f"✅ Fetched article: {article} (Type: {type(article)})")

            if not isinstance(article, Article):
                raise TypeError(f"❌ Mismatch: Retrieved object is not a valid `Article` instance. Got {type(article)}")

            # Convert schedule_date to timezone-aware datetime
            schedule_date = timezone.make_aware(datetime.strptime(schedule_date, "%Y-%m-%dT%H:%M"))

            # Create the scheduled content
            scheduled_content = ScheduledContent.objects.create(
                user=request.user,
                article=article,  
                schedule_date=schedule_date,
                repeat_option=repeat_option
            )

            return JsonResponse({
                "success": True,
                "article_title": article.title,
                "schedule_date": schedule_date,
                "repeat_option": scheduled_content.get_repeat_option_display(),
                "schedule_id": scheduled_content.id
            })

        except TypeError as te:
            print(f"❌ TypeError: {str(te)}")
            return JsonResponse({"error": str(te)}, status=500)
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# Delete Scheduled Content
@login_required
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(ScheduledContent, id=schedule_id, user=request.user)
    schedule.delete()
    return redirect("dashboard")

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

# Send Email (Ensures only logged-in users can send emails)
@csrf_exempt
@login_required
def send_email(request):
    if request.method == "POST":
        try:
            user_email = request.user.email  
            if not user_email:
                return JsonResponse({"error": "Your profile does not have an email set."}, status=400)

            data = json.loads(request.body)
            recipient_email = data.get("email")
            article_title = data.get("title")
            article_url = data.get("url")

            if not recipient_email:
                return JsonResponse({"error": "Recipient email is required."}, status=400)

            send_mail(
                subject=f"Check out this article: {article_title}",
                message=f"Hey! I found this interesting article: {article_url}",
                from_email=user_email,
                recipient_list=[recipient_email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Email sent successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def edit_schedule(request):
    if request.method == "POST":
        try:
            schedule_id = request.POST.get("schedule_id")
            new_date = request.POST.get("schedule_date")
            repeat_option = request.POST.get("repeat_option").capitalize()  

            print(f"Editing Schedule ID: {schedule_id}, New Date: {new_date}, Repeat: {repeat_option}")

            if new_date:
                new_date = timezone.make_aware(datetime.strptime(new_date, "%Y-%m-%dT%H:%M"))

            scheduled_content = get_object_or_404(ScheduledContent, id=schedule_id, user=request.user)
            scheduled_content.schedule_date = new_date
            scheduled_content.repeat_option = repeat_option.lower()  
            scheduled_content.save()

            formatted_date = scheduled_content.schedule_date.strftime("%B %d, %Y at %I:%M %p")

            return JsonResponse({
                "success": True,
                "message": "Schedule updated!",
                "new_date": formatted_date,
                "repeat": repeat_option  
            })
        
        except Exception as e:
            print(f"Error updating schedule: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
