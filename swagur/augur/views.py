from django import forms
from django.http import HttpResponse
from django.shortcuts import render


class BasicForm(forms.Form):
    user_id = forms.CharField(label="user_id")
    market_id = forms.CharField(label="market_id")

def index(request):
    return render(request, "augur/index.html")

def user(request):
    if request.method == "GET":
        return HttpResponse("App is running")
    elif request.method == "POST":
        form = BasicForm(request.POST)
        if form.is_valid():
            return HttpResponse(form.cleaned_data["user_id"])

def market(request):
    if request.method == "GET":
        return HttpResponse("App is running")
