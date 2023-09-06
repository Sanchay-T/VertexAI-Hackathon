from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

user_type_data = ((1, "HR"), (2, "Employee"))
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, null=False)

    email = models.EmailField(max_length=250, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()
    user_type = models.IntegerField(choices=user_type_data, default=1)

    def __str__(self):
        return "{}".format(self.username)

class Employee_Info(models.Model):
    name = models.CharField(max_length=250, null=False)
    candidate_info = models.TextField(max_length=1000)
    skills = models.TextField(max_length=1000)
    experience = models.TextField(max_length=1000)


class Company(models.Model):
    company_name = models.CharField(max_length=250, null=False)

    def __str__(self):
        return "{}".format(self.company_name)


job_security_information_choices = (("Stable", "Stable"), ("Risky", "Risky"))


class JobPost(models.Model):
    job_title = models.CharField(max_length=250, null=False)
    job_description = models.TextField(max_length=250, null=False)
    job_location = models.CharField(max_length=250, null=False)
    job_experience = models.CharField(max_length=250, null=False)
    job_qualification = models.CharField(max_length=250, null=False)
    job_posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_salary_range = models.CharField(max_length=250, null=False)
    flexible_work_arrangements = models.BooleanField(default=False)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_information = models.TextField(max_length=250, null=False)
    job_posted_on = models.DateField(auto_now_add=True)
    job_type = models.CharField(max_length=250, null=False)
    job_security_information = models.CharField(
        max_length=250, choices=job_security_information_choices, null=False , default="Stable"
    )
    job_data = models.JSONField(null=True)

    def __str__(self):
        return "{}_{}".format(self.job_title, self.job_posted_by.email)


class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes")
    application_status = models.CharField(
        max_length=250,
        null=True,
        choices=(
            ("Applied", "Applied"),
            ("Rejected", "Rejected"),
            ("Interview Stage", "Interview Stage"),
            ("Job Offered", "Job Offered"),
        ),
        default="Applied",
    )
    communication_log = models.CharField(max_length=250, null=True)
    hiring_decision = models.CharField(
        max_length=250,
        null=True,
        choices=(("Hired", "Hired"), ("Rejected", "Rejected"), ("Pending", "Pending")),
        default="Pending"
    )
    application_date = models.DateField(auto_now_add=True)
    employee_info = models.OneToOneField(Employee_Info , on_delete=models.CASCADE)

    
    def __str__(self):
        return "{}_{}".format(self.job.job_title , self.applicant.email)


class JobInsightData(models.Model):
    job = models.OneToOneField(JobPost, on_delete=models.CASCADE)
    job_application_data = models.JSONField(null=True)
