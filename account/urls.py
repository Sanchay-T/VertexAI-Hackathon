from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path("", views.base_dashboard , name="dashboard"),
    path("home/", views.home , name="home"),
    path("about/", views.about , name="about"),
    path("services/", views.services , name="services"),
    path("contact/", views.contact , name="contact"),
    path("login/", views.login_user , name="login"),
]
