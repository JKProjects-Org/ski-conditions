import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from app_scraping.models import SkiResort


class Command(BaseCommand):
    help = "Scrapes ski resort website and updates database"

    def handle(self, *args, **options):
        # list of urls
        url_keystone = \
                'https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
        url_heavenly = \
                'https://www.skiheavenly.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
        
        # place urls in list, loop over them
        url_list = [url_keystone, url_heavenly]
        
        for url in url_list:
            page = requests.get(url)

            # create a BeautifulSoup object
            soup = BeautifulSoup(page.text, 'html.parser')

            # search for class c118__number1--v1
            trails_summary = soup.find(class_ = 'terrain_summary row')

            # look for stuff in <span> tags
            trails_summary_items = trails_summary.find_all(class_= 'c118__number1--v1')

            # look for trail and lift totals
            trail_totals = trails_summary.find_all(class_='c118__number2--v1')

            if url == url_heavenly:
                # assign text to variables
                total_trails = int(trail_totals[3].get_text()[2:])
                total_lifts = int(trail_totals[1].get_text()[2:])
                # assign ints to variables
                acres_open = int(trails_summary_items[0].get_text())
                terrain_percent = int(trails_summary_items[2].get_text())
                trails_open = int(trails_summary_items[3].get_text())
                lifts_open = int(trails_summary_items[1].get_text())

                name = "Heavenly"

            
            elif url == url_keystone:

                total_trails = int(trail_totals[2].get_text()[2:])
                total_lifts = int(trail_totals[3].get_text()[2:])

                acres_open = int(trails_summary_items[0].get_text())
                terrain_percent = int(trails_summary_items[1].get_text())
                trails_open = int(trails_summary_items[2].get_text())
                lifts_open = int(trails_summary_items[3].get_text())

                name = "Keystone"

            k = SkiResort.objects.get(resort_name = name)
            k.trails_open = trails_open
            k.lifts_open = lifts_open
            k.acres_open = acres_open
            k.terrain_percent = terrain_percent
            k.save()

        self.stdout.write('SkiResort model updated')
