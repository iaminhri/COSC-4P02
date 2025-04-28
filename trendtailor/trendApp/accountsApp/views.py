from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm, ProfileImageForm
from .models import Profile, ProfileImage
from UserPreferenceApp.models import UserPreference
from UserPreferenceApp.forms import UserPreferenceForm
from trendApp.views import check_articles
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article 
from UserPreferenceApp.models import ScheduledContent  
from django.utils import timezone  
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from .summarization import summarize_article
# ✅ Registration View
def register(request):  
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                Profile.objects.create(user=user)
                ProfileImage.objects.create(user=user)
                # messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = RegisterForm()

        return render(request, 'accounts/register.html', {'form': form})

# ✅ Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = LoginForm(request = request, data = request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
        else:
            form = LoginForm()

        return render(request, 'accounts/login.html', {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        try:
            dashboard_pref, pre_created = UserPreference.objects.get_or_create(user=request.user)
        except:
            dashboard_pref = None
            messages.info(request, "No Preferences Set")

        try:
            preferences, create = UserPreference.objects.get_or_create(user=request.user)
            
            topics = preferences.topics.split(',') if preferences.topics else []
            keywords = preferences.keywords.split(',') if preferences.keywords else []
            
            contents = check_articles(request.user, topics, keywords)

            paginator = Paginator(contents, 3)
            pageNumber = request.GET.get('p', 1)
            articlePageObj = paginator.get_page(pageNumber)

        except:
            articlePageObj = None
            messages.error(request, "Something is wrong !!!")

        scheduled_contents = ["Not Available"]
        articles = Article.objects.all()
        try:
            scheduled_contents = ScheduledContent.objects.filter(user=request.user).order_by("schedule_date")
        except Exception as e:
            print("Scheduling Error: ", e)
            
        return render(request, 'dashboard.html', {'preferences': dashboard_pref, 'articles': articlePageObj, "scheduled_contents": scheduled_contents})

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        try:
            profile = Profile.objects.get(user=request.user)
            profileimage = ProfileImage.objects.get(user=request.user)
        except:
            profile = None
            profileimage = None
            if profile == None:
                messages.info(request, "No profile data found. Please create your profile")
            elif profileimage == None:
                messages.info(request, "No image data found, please upload an image.")
            else:
                messages.info(request, "No profile and image data found, please create your profile.")
            return redirect('profile_form')
        
        return render(request, 'users/profile.html', {'profile': profile, 'profileimage': profileimage})

def profile_form(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        
        profile, created = Profile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!!!")
            else:
                messages.error(request, "Error updating your profile. Please check the form data")
        else:
            form = ProfileForm(instance=profile)

        return render(request, 'users/edit_profile.html', {'form': form})

def user_settings(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'users/account_settings.html')

def edit_profile_image(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        profileImage, created = ProfileImage.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            form = ProfileImageForm(request.POST, request.FILES, instance=profileImage)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile picture updated successfully!!!")
            else:
                messages.error(request, "Error uploading your profile picture. Please try again.")
        else:
            form = ProfileImageForm(instance=profileImage)

        return redirect('profile')
    
def auth_logout(request):
    logout(request)
    return redirect('login')

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

def summarization(request):
    summary = None
    error = None

    if request.method == 'POST':
        article_text = ''

        uploadedFile = request.FILES.get('contentFile')
        if uploadedFile and isinstance(uploadedFile, UploadedFile):
            try:
                article_text = uploadedFile.read().decode('utf-8')
            except Exception as e:
                error = f"Error reading file: {str(e)}"

        if not article_text:
            article_text = request.POST.get('textInput', '').strip()

        if article_text:
            try:
                summary = summarize_article(article_text)
            except Exception as e:
                error = f"Error Summarize Text: {str(e)}"
        elif not error:
            error = "Please upload a file or enter text."

    return render(request, 'summarization.html', {'summary': summary, 'error': error})