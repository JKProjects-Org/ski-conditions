import os

import pytest
import responses
from django.core import management

from ..management.commands.do_scraping import HeavenlyScraper, KirkwoodScraper, NorthstarScraper,\
        KirkwoodSnowReport, HeavenlySnowReport, NorthstarSnowReport
from ..models import SkiResort


# pylint: disable=no-member
@responses.activate
@pytest.mark.django_db()
def test_scraping():
    assert SkiResort.objects.count() == 0

    body_Kirkwood = open(os.path.join(os.path.dirname(__file__), 'data', 'kirkwood.html'))
    responses.add(responses.GET, KirkwoodScraper.url, status=200, body=body_Kirkwood.read())

    body_Heavenly = open(os.path.join(os.path.dirname(__file__), 'data', 'heavenly.html'))
    responses.add(responses.GET, HeavenlyScraper.url, status=200, body=body_Heavenly.read())

    body_Northstar = open(os.path.join(os.path.dirname(__file__), 'data', 'northstar.html'))
    responses.add(responses.GET, NorthstarScraper.url, status=200, body=body_Northstar.read())

    body_Kirkwood_snow = open(os.path.join(os.path.dirname(__file__), 'data', 'kirkwood_snow.html'))
    responses.add(responses.GET, KirkwoodSnowReport.url, status=200, body=body_Kirkwood_snow.read())

    body_Heavenly_snow = open(os.path.join(os.path.dirname(__file__), 'data', 'heavenly_snow.html'))
    responses.add(responses.GET, HeavenlySnowReport.url, status=200, body=body_Heavenly_snow.read())

    body_Northstar_snow = open(os.path.join(os.path.dirname(__file__), 'data', 'northstar_snow.html'))
    responses.add(responses.GET, NorthstarSnowReport.url, status=200, body=body_Northstar_snow.read())


    management.call_command('do_scraping')

    assert SkiResort.objects.count() == 3

    kirkwood = SkiResort.objects.get(resort_name='Kirkwood')
    assert kirkwood.acres_open == 1031
    assert kirkwood.terrain_percent == 45
    assert kirkwood.trails_open == 52
    assert kirkwood.total_trails == 88
    assert kirkwood.lifts_open == 7
    assert kirkwood.total_lifts == 14
    assert kirkwood.overnight_snowfall == 1
    assert kirkwood.twenty_four_hour_snowfall == 2
    assert kirkwood.forty_eight_hour_snowfall == 2
    assert kirkwood.seven_day_snowfall == 19
    assert kirkwood.base_depth == 49
    assert kirkwood.current_season == 127

    heavenly = SkiResort.objects.get(resort_name='Heavenly')
    assert heavenly.acres_open == 22
    assert heavenly.terrain_percent == 0
    assert heavenly.trails_open == 4
    assert heavenly.total_trails == 97
    assert heavenly.lifts_open == 4
    assert heavenly.total_lifts == 28
    assert heavenly.overnight_snowfall == 0
    assert heavenly.twenty_four_hour_snowfall == 0
    assert heavenly.forty_eight_hour_snowfall == 0
    assert heavenly.seven_day_snowfall == 19
    assert heavenly.base_depth == 30
    assert heavenly.current_season == 109


    northstar = SkiResort.objects.get(resort_name='Northstar')
    assert northstar.acres_open == 1182
    assert northstar.terrain_percent == 37
    assert northstar.trails_open == 57
    assert northstar.total_trails == 100
    assert northstar.lifts_open == 10
    assert northstar.total_lifts == 20
    assert northstar.overnight_snowfall == 2
    assert northstar.twenty_four_hour_snowfall == 3
    assert northstar.forty_eight_hour_snowfall == 3
    assert northstar.seven_day_snowfall == 28
    assert northstar.base_depth == 46
    assert northstar.current_season == 113

