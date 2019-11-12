import environ
import psycopg2
from django.http import HttpResponse
from django.template import loader

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

    if 'heavenly' in url:
        # assign text to variables
        total_trails = trail_totals[3].get_text()[2:]
        total_lifts = trail_totals[1].get_text()[2:]

        # assign ints to variables
        acres_open = int(trails_summary_items[0].get_text())
        terrain_percent = int(trails_summary_items[2].get_text())
        trails_open = int(trails_summary_items[3].get_text())
        lifts_open = int(trails_summary_items[1].get_text())

    elif 'keystone' in url:
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
    # get database name from environment
    env = environ.Env(DEBUG=(bool, False), )
    
    # create connection to database 
    db = psycopg2.connect(database = env.db()['NAME'])

    # create cursor to go through database
    cur = db.cursor()
    
    ######## KEYSTONE
    # run scraper to get latest keystone data
    url = 'https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'

    resort_name = 'Keystone'

    total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open = \
            ski_scraper(url)


    # insert data into table if resort doesn't exist
    # otherwise, update existing resort data

    ski_resort, created = SkiResort.objects.update_or_create(
        resort_name=resort_name,
        defaults={
            'trails_open': trails_open,
            'lifts_open': lifts_open,
            'acres_open': acres_open,
            'terrain_percent': terrain_percent,
            'total_trails': total_trails,
            'total_lifts': total_lifts,
        }
    )

    # cur.execute(
    #         f'''INSERT INTO app_scraping_skiresort (resort_name, trails_open, lifts_open, acres_open,
    #             terrain_percent, total_trails, total_lifts)
    #             VALUES ('{resort_name}', {trails_open}, {lifts_open}, {acres_open}, {terrain_percent},
    #             {total_trails},{total_lifts})
    #             ON CONFLICT (resort_name) DO UPDATE
    #                 SET trails_open = {trails_open},
    #                     lifts_open = {lifts_open},
    #                     acres_open = {acres_open},
    #                     terrain_percent = {terrain_percent}
    #                 ''')

    db.commit()
        
    ######### HEAVENLY
    # run scraper to get latest Heavenly data
    url = 'https://www.skiheavenly.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
    resort_name = 'Heavenly'
    total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open = \
            ski_scraper(url)

    # insert data into table if resort doesn't exist
    # otherwise, update existing resort data
    cur.execute(
            f'''INSERT INTO app_scraping_skiresort (resort_name, trails_open, lifts_open, acres_open, 
                terrain_percent, total_trails, total_lifts) 
                VALUES ('{resort_name}', {trails_open}, {lifts_open}, {acres_open}, {terrain_percent}, 
                {total_trails},{total_lifts})
                ON CONFLICT (resort_name) DO UPDATE
                    SET trails_open = {trails_open},
                        lifts_open = {lifts_open},
                        acres_open = {acres_open},
                        terrain_percent = {terrain_percent}
                    ''')

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
