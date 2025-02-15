from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# ✅ Registration View
def register(request):  
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = RegisterForm()

        return render(request, 'registration/register.html', {'form': form})

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

        return render(request, 'registration/login.html', {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'dashboard.html')

def user_profile(request):
    return render(request, 'registration/profile.html')

def auth_logout(request):
    logout(request)
    return redirect('login')