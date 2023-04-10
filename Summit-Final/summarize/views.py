from django.shortcuts import render
import SummIt
import summit_text
from .models import users
import datetime

# Create your views here.
def register(request):
    return render(request , "summarize/register.html")

def login(request):
    return render(request , "summarize/login.html")

def copyrights(request):
    return render(request, "summarize/copyrights.html")

def index(request):
    if request.method=="POST":
        temp=users()
        data=request.POST
        temp.username=data["username"]
        temp.phone=data["phone"]
        temp.email=data["email"]
        if data["password"]!=data["password2"]:
            return render(request, 'summarize/error.html',{"message":"Passwords don't match"})
        temp.password=data["password"]
        temp.save()
    return render(request , "summarize/index.html")


def text(request):
    if request.method=="POST" and "email" in request.POST:
        email=request.POST["email"]
        password=request.POST["password"]
        temp=users.objects.all()
        for i in temp:
            if i.email==email and i.password == password:
                    return render(request, "summarize/text.html")
            if i.email==email:
                return render(request , "summarize/error.html", {"message" : "Wrong Password"})
        return render(request , "summarize/error.html", {"message" : "Not registered Email"})
    return render(request, "summarize/text.html")

def video(request):
    return render(request, "summarize/video.html")


def summarize(request):
    data=request.POST
    language=data["language"]
    url=data["url"]
    percentage = data["percentage"]
    start=datetime.datetime.now()
    output = SummIt.summarizeDataComplete(url,language,percentage)
    if output=="captions":
        return render(request , "summarize/video.html" ,{"message" : "No Captions available"})
    if output == "ratio":
        return render(request , "summarize/video.html" ,{"message" : "The percentage extraction for video is too low"})
    end=datetime.datetime.now()
    diff=(end-start).seconds + (end-start).microseconds/1000000
    ind=url.index("=")
    urlcode=url[ind+1:ind+12]
    recommed=SummIt.recommendVideo(urlcode)
    if recommed=="":
        recommed="Comments are turned off for this video."
    url = "http://i3.ytimg.com/vi/" + urlcode +"/0.jpg"
    return render(request, "summarize/result.html" , {"output" : output, "url":url,"display":"block","delay":"Data was summerized in "+str(diff)+" seconds","recommend":recommed})


def textSummarize(request):
    data=request.POST
    language=data["language"]
    textdata=data["textdata"]
    percentage = data["percentage"]
    start=datetime.datetime.now()
    output = summit_text.summarizeText(language,textdata,float(percentage))
    if output==None:
        return render(request , "summarize/text.html" ,{"message" : "The percentage extraction for text is too low"})

    end=datetime.datetime.now()
    diff=(end-start).seconds + (end-start).microseconds/1000000
    
    return render(request, "summarize/result.html", {"output" : output,"url":None,"display" : "none","delay":"Data was summerized in "+str(diff)+" seconds"})


def aboutUs(request):
    return render(request , "summarize/aboutus.html")