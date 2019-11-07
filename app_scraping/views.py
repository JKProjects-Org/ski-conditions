from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    greeting = HttpResponse("This is where Keystone conditions will be posted. Stay tuned.")
    return greeting
