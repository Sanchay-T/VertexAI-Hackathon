from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(JobInsightData)
admin.site.register(Company)
admin.site.register(Employee_Info)

