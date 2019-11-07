from django.shortcuts import render
from django.http import HttpResponse
from .models import SkiResort

# Create your views here.
def index(request):
    try:
        resort_name = SkiResort.resort_name
        output = resort_name
        return HttpResponse(output)
    except:

        greeting = HttpResponse("This is where Keystone conditions will be posted. Stay tuned.")
        return greeting
