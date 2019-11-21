import environ
import psycopg2
from django.core import management
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from .models import SkiResort


# Create your views here.
def index(request):
    # run management command to do scraping from here for now
    # TODO: put in cronjob
    management.call_command('do_scraping')

    '''
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
    cur.execute(
            f'INSERT INTO app_scraping_skiresort (resort_name, trails_open, lifts_open, acres_open, 
                terrain_percent, total_trails, total_lifts) 
                VALUES ('{resort_name}', {trails_open}, {lifts_open}, {acres_open}, {terrain_percent}, 
                {total_trails},{total_lifts})
                ON CONFLICT (resort_name) DO UPDATE
                    SET trails_open = {trails_open},
                        lifts_open = {lifts_open},
                        acres_open = {acres_open},
                        terrain_percent = {terrain_percent}
                    ')

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
            f'INSERT INTO app_scraping_skiresort (resort_name, trails_open, lifts_open, acres_open, 
                terrain_percent, total_trails, total_lifts) 
                VALUES ('{resort_name}', {trails_open}, {lifts_open}, {acres_open}, {terrain_percent}, 
                {total_trails},{total_lifts})
                ON CONFLICT (resort_name) DO UPDATE
                    SET trails_open = {trails_open},
                        lifts_open = {lifts_open},
                        acres_open = {acres_open},
                        terrain_percent = {terrain_percent}
                    ')

    db.commit()
    db.close()
    
    '''
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
