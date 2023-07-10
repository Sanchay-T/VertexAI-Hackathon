from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

user_type_data = ((1 , "HR") , (2 , "Employee"))
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, null=False)

    email = models.EmailField(max_length=250, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    user_type = models.CharField(default=1 , choices=user_type_data , max_length=10)


    def __str__(self):
        return "{}".format(self.username)



class JobPost(models.Model):
    job_title = models.CharField(max_length=250, null=False)
    job_description = models.TextField(max_length=250, null=False)
    job_location = models.CharField(max_length=250, null=False)
    job_salary = models.CharField(max_length=250, null=False)
    job_experience = models.CharField(max_length=250, null=False)
    job_qualification = models.CharField(max_length=250, null=False)
    job_posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_posted_on = models.DateField(auto_now_add=True)
    job_type = models.CharField(max_length=250, null=False)
    job_data = models.JSONField(null=True)

    def __str__(self):
        return "{}".format(self.job_title)
    
class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes")
    application_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.job.job_title)
    

class JobInsightData(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to="csv_files")

