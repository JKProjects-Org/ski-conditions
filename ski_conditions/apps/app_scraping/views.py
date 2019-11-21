from django.core import management
from django.http import HttpResponse
from django.template import loader

from .models import SkiResort


# Create your views here.
def index(request):
    # run management command to do scraping from here for now
    # TODO: put in cronjob
    # management.call_command('do_scraping')
    try:
        output = SkiResort.objects.all()
        template = loader.get_template('app_scraping/index.html')
        context = {
            'resort_list': output,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        greeting = HttpResponse("This is where Keystone conditions will be posted. Stay tuned.")
        return greeting
