from django.contrib import admin
from django.urls import path , include
from . import views
from google_vertex_ai import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.base_dashboard , name="dashboard"),
    path("home/", views.home , name="home"),
    path("about/", views.about , name="about"),
    path("services/", views.services , name="services"),
    path("contact/", views.contact , name="contact"),
    path("signup/", views.sign_up , name="signup"),
    path("login/", views.login_user , name="login"),
    path("logout/", views.logout_user , name="logout"),
    path("post_job/", views.post_job , name="post_job"),
    path("jobs_posted/", views.job_list_hr , name="jobs_posted"),
    path("job_list/", views.job_list_emp , name="emp_job_list"),
    # path("job_detail/<int:job_id>/", views.job_detail , name="job_detail"),
    path("apply_for_job/<int:job_id>/", views.apply_for_job , name="apply_for_job"),
    path("jobs_applied/", views.jobs_applied , name="jobs_applied"),
    path("job_insights/<int:job_id>", views.job_details , name="job_insights"),
    path("analyze_hr_query", views.analyze_hr_query , name="analyze_hr_query"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









