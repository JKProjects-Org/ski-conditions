import psycopg2
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from .models import SkiResort


def ski_scraper(url):
    '''
    Inputs:
    url: string; URL of resort to scrape
    --------
    Returns:
    total_trails: string; total trails in resort
    total_lifts: string; total lifts in resort
    acres_open: int; current acres open in resort
    terrain_percent: int; current percent of terrain open
    trails_open: int; current number of trails open
    lifts_open: int; current number of lifts open

    '''
    from bs4 import BeautifulSoup
    import requests
    
    page = requests.get(url)

    # check if page retrieved. should output 200
    #print('page status code: ', page.status_code)

    # create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # search for class terrain_summary row
    trails_summary = soup.find(class_ = 'terrain_summary row')

    # look for open data in class c118__number1--v1
    trails_summary_items = trails_summary.find_all(class_= 'c118__number1--v1')

    # look for trail and lift totals in class c118__number2--v1
    trail_totals = trails_summary.find_all(class_='c118__number2--v1')

    # assign text to variables
    total_trails = trail_totals[2].get_text()[2:]
    total_lifts = trail_totals[3].get_text()[2:]

    # assign ints to variables
    acres_open = int(trails_summary_items[0].get_text())
    terrain_percent = int(trails_summary_items[1].get_text())
    trails_open = int(trails_summary_items[2].get_text())
    lifts_open = int(trails_summary_items[3].get_text())

    return total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open


# Create your views here.
def index(request):
    # create connection to database db_ski
    db = psycopg2.connect(database = 'db_ski')
    # create cursor to go through database
    cur = db.cursor()
    
    # run scraper to get latest keystone data
    url = 'https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'

    resort_name = 'Keystone'

    total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open = \
            ski_scraper(url)


    # testing creating a SkiResort object
    # should be updating existing entries
    try:
        # resort entry already exists
        cur.execute(
                f'''UPDATE app_scraping_skiresort
                SET trails_open = {trails_open},
                    lifts_open = {lifts_open},
                    acres_open = {acres_open},
                    terrain_percent = {terrain_percent}
                WHERE resort_name = '{resort_name}' and id=1;
                ''')

    except:
        # new resort entry

        cur.execute(
                f'''INSERT INTO app_scraping_skiresort (resort_name, trails_open, lifts_open, acres_open, 
                terrain_percent, total_trails, total_lifts) 
                VALUES ({resort_name}, {trails_open}, {lifts_open}, {acres_open}, {terrain_percent}, 
                {total_trails},{total_lifts});''')
        
    db.commit()
    db.close()
    

    # render views
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
