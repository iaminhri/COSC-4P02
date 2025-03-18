from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm, ProfileImageForm
from .models import Profile, ProfileImage
from UserPreferenceApp.models import UserPreference
from UserPreferenceApp.forms import UserPreferenceForm
from trendApp.views import check_articles
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article 

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
        return render(request, 'dashboard.html', {'preferences': dashboard_pref, 'articles': articlePageObj})

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