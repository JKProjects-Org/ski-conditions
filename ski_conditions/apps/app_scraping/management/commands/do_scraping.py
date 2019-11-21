import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from ski_conditions.apps.app_scraping.models import SkiResort


# TODO Use the abc library
class AbstractScraper:
    def scrape(self):
        pass


class AbstractVailScraper(AbstractScraper):
    def _common_scrape(self):
        page = requests.get(self.url)

        # create a BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')

        # search for class c118__number1--v1
        trails_summary = soup.find(class_='terrain_summary row')

        # look for stuff in <span> tags
        trails_summary_items = trails_summary.find_all(class_='c118__number1--v1')

        # look for trail and lift totals
        trail_totals = trails_summary.find_all(class_='c118__number2--v1')

        return (trail_totals, trails_summary_items)


class KeystoneScraper(AbstractVailScraper):
    name = 'Keystone'
    url = 'https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'

    def scrape(self):
        trail_totals, trails_summary_items = self._common_scrape()

        new_total_trails = int(trail_totals[2].get_text()[2:])
        new_total_lifts = int(trail_totals[3].get_text()[2:])

        new_acres_open = int(trails_summary_items[0].get_text())
        new_terrain_percent = int(trails_summary_items[1].get_text())
        new_trails_open = int(trails_summary_items[2].get_text())
        new_lifts_open = int(trails_summary_items[3].get_text())

        # TODO Use a struct or other data structure
        return {
            'total_trails': new_total_trails,
            'total_lifts': new_total_lifts,
            'acres_open': new_acres_open,
            'terrain_percent': new_terrain_percent,
            'trails_open': new_trails_open,
            'lifts_open': new_lifts_open,
        }


class HeavenlyScraper(AbstractVailScraper):
    name = 'Heavenly'
    url = 'https://www.skiheavenly.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'

    def scrape(self):
        trail_totals, trails_summary_items = self._common_scrape()

        # assign text to variables
        new_total_trails = int(trail_totals[3].get_text()[2:])
        new_total_lifts = int(trail_totals[1].get_text()[2:])

        # assign ints to variables
        new_acres_open = int(trails_summary_items[0].get_text())
        new_terrain_percent = int(trails_summary_items[2].get_text())
        new_trails_open = int(trails_summary_items[3].get_text())
        new_lifts_open = int(trails_summary_items[1].get_text())

        return {
            'total_trails': new_total_trails,
            'total_lifts': new_total_lifts,
            'acres_open': new_acres_open,
            'terrain_percent': new_terrain_percent,
            'trails_open': new_trails_open,
            'lifts_open': new_lifts_open,
        }


class Command(BaseCommand):
    help = "Scrapes ski resort website and updates database"

    def handle(self, *args, **options):
        scrapers = [
            KeystoneScraper(),
            # HeavenlyScraper(),
        ]

        for scraper in scrapers:
            name = scraper.name
            scraped = scraper.scrape()

            SkiResort.objects.update_or_create(
                resort_name=name,
                defaults={
                    'total_trails': scraped['total_trails'],
                    'acres_open': scraped['acres_open'],
                    'terrain_percent': scraped['terrain_percent'],
                    'trails_open': scraped['trails_open'],
                    'lifts_open': scraped['lifts_open'],
                    'total_lifts': scraped['total_lifts'],
                }
            )

        self.stdout.write('SkiResort model updated')
