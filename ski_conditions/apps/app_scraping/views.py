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


def twitter(request):
    output = '''
        <a class="twitter-timeline" data-width="480" data-height="600"
        href="https://twitter.com/HVconditions?ref_src=twsrc%5Etfw">Tweets by HVconditions</a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

        <a class="twitter-timeline" data-width="480" data-height="600" data-theme="dark"
        href="https://twitter.com/northstarmtn?ref_src=twsrc%5Etfw">Tweets by northstarmtn</a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

        <a class="twitter-timeline" data-width="480" data-height="600"
        href="https://twitter.com/KWconditions?ref_src=twsrc%5Etfw">Tweets by KWconditions</a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    '''
    return HttpResponse(output)
