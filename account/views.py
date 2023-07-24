from django.shortcuts import render , redirect 
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
import vertex_ai_process
import threading
import os
from agent.final_Agent import extract_resume_information



print("in the views")

# Create your views here.

@login_required(login_url='login')
def base_dashboard(request):
    if request.user.is_superuser:
        return render(request , "account/admin/admin_dashboard.html")
    
    if request.user.user_type == 1:
        return render(request , "account/hr/hr_dashboard.html")
    else:
        return render(request , "account/employee/emp_dashboard.html")

def home(request):
    return render(request , "account/home.html")

def about(request):
    return render(request , "account/about.html")

def services(request):
    return render(request , "account/services.html")

def contact(request):
    return render(request , "account/contact.html")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")


        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")
        else:
            user = CustomUser.objects.create_user(username=username , email=email , password=password , user_type=user_type)
            user.save()
            return redirect("login")
        
    return render(request , "account/signup.html")

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect("login")

def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email , password)

        # authenticate user 
        user = authenticate(request , email=email , password=password)

        if user is not None:
            login(request , user)
            return redirect("dashboard")
        else:
            return HttpResponse("Invalid Credentials")

    return render(request , "account/login.html")


@login_required(login_url='login')
def post_job(request):
    if request.method == "POST":
        print(request.POST)
        job_title = request.POST.get("job_title")
        job_description = request.POST.get("job_description")
        job_location = request.POST.get("job_location")
        job_experience = request.POST.get("job_experience")
        job_qualification = request.POST.get("job_qualification")
        job_company = request.POST.get("job_company")
        job_salary_range = request.POST.get("job_salary")
        job_company_info = request.POST.get("job_company_info")
        job_security = request.POST.get("job_security")
        flexible_work_arrangements = request.POST.get("flexible_work_arrangements")
        flexible_work_arrangements = True if flexible_work_arrangements else False
        print("********")
        print(flexible_work_arrangements)
        print("********")
        job_posted_by = request.user
        # job_status = request.POST.get("job_status")
        job_type = request.POST.get("job_type")

        company = Company.objects.get(id = job_company)

        job_post = JobPost.objects.create(job_title=job_title , job_description=job_description , job_location=job_location , job_salary_range=job_salary_range , job_experience=job_experience , job_qualification=job_qualification , flexible_work_arrangements = flexible_work_arrangements , company_information = job_company_info , job_posted_by=job_posted_by , job_type=job_type , job_security_information = job_security , company_id=company)
        job_post.save()
        return redirect("jobs_posted")
    return render(request , "account/hr/new_job_post.html" , context={'company_list' : Company.objects.all()})

import json

@login_required(login_url='login')
def job_list_hr(request):
    job_list = JobPost.objects.all()
    context = {
        "job_list" : job_list
    }
    return render(request , "account/hr/jobs_posted.html" , context)

@login_required(login_url='login')
def job_details(request , job_id):
    job = JobPost.objects.get(id=job_id)

    job_applicants = JobApplication.objects.filter(job = job).select_related('job' , 'applicant').all()
    print(job_applicants)

    mydict = {
        'Name' : [],
        'Email' : [],
        "Skills" : [],
        "Experience" : [],
        "Applicant Status" : []
    }

    for job_applicant in job_applicants:
        mydict['Name'].append(job_applicant.applicant.username)
        mydict['Email'].append(job_applicant.applicant.email)
        mydict['Skills'].append(job_applicant.employee_info.skills)
        mydict['Experience'].append(job_applicant.employee_info.experience)
        mydict['Experience'].append(job_applicant.employee_info.experience)


    # convert mydict to jsonstring 
    json_string = json.dumps(mydict)
    print(json_string)

    
    jobpost_data , create = JobInsightData.objects.get_or_create(job=job)
    jobpost_data.job_application_data = json_string


    context = {
        'job_applicants' : job_applicants,
        'job_id' : job.id,
    }


    return render(request , "account/job_details.html" , context=context)


@login_required(login_url='login')
def job_list_emp(request):
    job_list = JobPost.objects.all()
    context = {
        "job_list" : job_list
    }
    return render(request , "account/employee/jobs_list.html" , context = context)

@login_required(login_url='login')
def apply_for_job(request , job_id):
    job = JobPost.objects.get(id=job_id)   
    resume = request.FILES['resume']
    # if JobApplication.objects.filter(job=job , applicant=request.user).exists():
        # return HttpResponse("Job Already Applied.")
    employee = Employee_Info.objects.create(candidate_info = "Testing Info" , experience = "5 years" , skills = "Django")
    employee.save()
    job_application = JobApplication.objects.create(job=job , applicant=request.user , resume = resume , employee_info = employee)
    job_application.save()
    

    filename = os.path.basename(job_application.resume.name)

    print(filename)

    threading.Thread(target=extract_resume_information , args=[filename]).start()
    print("\n\n\n\This is the resume output")
    print(output)
    print("********\n\n\n")



    
    return HttpResponse("Applied Successfully.")


@login_required(login_url='login')
def jobs_applied(request):
    job_list = JobApplication.objects.select_related("job" , "applicant").filter(applicant=request.user)
    context = {
        "job_list" : job_list
    }
    return render(request , "account/employee/jobs_applied.html" , context = context)


def analyze_hr_query(request):
    print(request.POST)

    job_id = request.POST.get("job_id")
    print(JobInsightData.objects.filter(job_id=job_id).first().job_application_data)
    return HttpResponse("Success")


