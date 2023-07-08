from django.shortcuts import render , redirect 
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def base_dashboard(request):
    # if request.user.is_authenticated:

    return render(request , "account/emp_dashboard.html")
    # return render(request , "account/hr_dashboard.html")

def home(request):
    return render(request , "account/home.html")

def about(request):
    return render(request , "account/about.html")

def services(request):
    return render(request , "account/services.html")

def contact(request):
    return render(request , "account/contact.html")

# create login view 
def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate user 
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            return redirect(reverse("dashboard"))
        else:
            return HttpResponse("Invalid Login")

    return render(request , "account/login.html")
