from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "augur/index.html")

def user(request):
    if request.method == "GET":
        return HttpResponse("App is running")

def market(request):
    if request.method == "GET":
        return HttpResponse("App is running")
