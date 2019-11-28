from django.http import HttpResponse
from django.template import loader

from .models import SkiResort


def index(request):
    output = SkiResort.objects.all()
    template = loader.get_template('app_scraping/index.html')
    context = {
        'resort_list': output,
        }
    return HttpResponse(template.render(context, request))
