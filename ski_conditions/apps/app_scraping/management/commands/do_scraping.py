import json
import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from ski_conditions.apps.app_scraping.models import SkiResort


# TODO Use the abc library
class AbstractScraper:
    def scrape(self):
        pass


class AbstractScriptScraper(AbstractScraper):
    def _common_scrape(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # search for javascript
        script_items = soup.find_all('script', type='text/javascript')

        return script_items


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


class NorthstarScraper(AbstractVailScraper):
    name = 'Northstar'
    url = 'https://www.northstarcalifornia.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'

    def scrape(self):
        trail_totals, trails_summary_items = self._common_scrape()

        new_total_trails = int(trail_totals[2].get_text()[2:])
        new_total_lifts = int(trail_totals[1].get_text()[2:])

        new_acres_open = int(trails_summary_items[2].get_text())
        new_terrain_percent = int(trails_summary_items[3].get_text())
        new_trails_open = int(trails_summary_items[1].get_text())
        new_lifts_open = int(trails_summary_items[0].get_text())

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


class KirkwoodSnowReport(AbstractScriptScraper):
    name = 'Kirkwood'
    url = 'https://www.kirkwood.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx'

    def scrape(self):
        script_items = self._common_scrape()

        # get script body that contains snow report numbers
        script_snow_report = script_items[1].text

        # create regex pattern to find snowReportData json
        # only grabs stuff in parens
        pattern = re.compile("snowReportData = ({.*})")
        # returns a list, grab first and only element
        snow_data = re.findall(pattern, script_snow_report)[0]

        # use json module to read json snow_data
        json_snow_data = json.loads(snow_data)

        return json_snow_data

    def unpack_json(self, json_data):

        return {
            'overnight': json_data['OvernightSnowfall']['Inches'],
            '24hr': json_data['TwentyFourHourSnowfall']['Inches'],
            '48hr': json_data['FortyEightHourSnowfall']['Inches'],
            '7day': json_data['SevenDaySnowfall']['Inches'],
            'base_depth': json_data['BaseDepth']['Inches'],
            'current_season': json_data['CurrentSeason']['Inches'],
        }


class HeavenlySnowReport(AbstractScriptScraper):
    name = 'Heavenly'
    url = 'https://www.skiheavenly.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx'

    def scrape(self):
        script_items = self._common_scrape()

        # get script body that contains snow report numbers
        script_snow_report = script_items[1].text

        # create regex pattern to find snowReportData json
        # only grabs stuff in parens
        pattern = re.compile("snowReportData = ({.*})")
        # returns a list, grab first and only element
        snow_data = re.findall(pattern, script_snow_report)[0]

        # use json module to read json snow_data
        json_snow_data = json.loads(snow_data)

        return json_snow_data

    def unpack_json(self, json_data):

        return {
            'overnight': json_data['OvernightSnowfall']['Inches'],
            '24hr': json_data['TwentyFourHourSnowfall']['Inches'],
            '48hr': json_data['FortyEightHourSnowfall']['Inches'],
            '7day': json_data['SevenDaySnowfall']['Inches'],
            'base_depth': json_data['BaseDepth']['Inches'],
            'current_season': json_data['CurrentSeason']['Inches'],
        }


class NorthstarSnowReport(AbstractScriptScraper):
    name = 'Northstar'
    url = 'https://www.northstarcalifornia.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx'

    def scrape(self):
        script_items = self._common_scrape()

        # get script body that contains snow report numbers
        script_snow_report = script_items[1].text

        # create regex pattern to find snowReportData json
        # only grabs stuff in parens
        pattern = re.compile("snowReportData = ({.*})")
        # returns a list, grab first and only element
        snow_data = re.findall(pattern, script_snow_report)[0]

        # use json module to read json snow_data
        json_snow_data = json.loads(snow_data)

        return json_snow_data

    def unpack_json(self, json_data):

        return {
            'overnight': json_data['OvernightSnowfall']['Inches'],
            '24hr': json_data['TwentyFourHourSnowfall']['Inches'],
            '48hr': json_data['FortyEightHourSnowfall']['Inches'],
            '7day': json_data['SevenDaySnowfall']['Inches'],
            'base_depth': json_data['BaseDepth']['Inches'],
            'current_season': json_data['CurrentSeason']['Inches'],
        }


class Command(BaseCommand):
    help = "Scrapes ski resort website and updates database"

    def handle(self, *args, **options):
        # Trail and Lift Conditions
        scrapers = [
            KeystoneScraper(),
            HeavenlyScraper(),
            NorthstarScraper(),
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

        # Snow Conditions
        snow_reports = [
            KirkwoodSnowReport(),
            HeavenlySnowReport(),
            NorthstarSnowReport(),
        ]

        for snow in snow_reports:
            name = snow.name
            snow_json_data = snow.scrape()
            snow_data = snow.unpack_json(snow_json_data)

            SkiResort.objects.update_or_create(
                resort_name=name,
                defaults={
                    'overnight_snowfall': snow_data['overnight'],
                    'twenty_four_hour_snowfall': snow_data['24hr'],
                    'forty_eight_hour_snowfall': snow_data['48hr'],
                    'seven_day_snowfall': snow_data['7day'],
                    'base_depth': snow_data['base_depth'],
                    'current_season': snow_data['current_season'],
                }
            )

        self.stdout.write('SkiResort model updated')
