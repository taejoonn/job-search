from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def home(request):
    
    return render(request, 'home.html')