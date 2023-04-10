from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index),
    path("summarize",views.summarize),
    path("textSummarize",views.textSummarize),
    path("text",views.text),
    path("video",views.video),
    path("aboutUs",views.aboutUs),
    path("register",views.register),
    path("login",views.login),
    path("copyrights",views.copyrights),
    
    
    
]
