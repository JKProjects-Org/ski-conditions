from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import SkiResort


# Create your views here.
def index(request):
    # testing creating a SkiResort object
    # need to put this code somewhere else because it creates new entries
    # should be updating existing entries
    keystone = SkiResort(resort_name="Keystone")
    keystone.save()
    try:
        output = SkiResort.objects.all()
        template = loader.get_template('app_scraping/index.html')
        context= {
                'resort_list': output,
                }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        greeting = HttpResponse("This is where Keystone conditions will be posted. Stay tuned.")
        return greeting
