from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from UserPreferenceApp.utils import fetch_articles_from_api_1, fetch_articles_from_api_3
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt


def home(request):
    articles = fetch_all_articles()
    paginator = Paginator(articles, 52)
    page_number = request.GET.get('p', 1)
    article_page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {"articles": article_page_obj})

def fetch_all_articles():
    return Article.objects.all()

def check_articles(user, topics, keywords):
    query = Q()
    for term in topics + keywords:
        query |= Q(title__icontains=term) | Q(description__icontains=term)
    
    existingArticles = Article.objects.filter(query)

    if existingArticles.exists():
        articles_list = list(existingArticles)
        return articles_list
    else:
        return []

# Scrum 3 task1: Generate email template with newsletter
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
    
    template_name = template_map.get(template_id, "share_email1.html") 
    return render(request, template_name, {"article": article})


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
