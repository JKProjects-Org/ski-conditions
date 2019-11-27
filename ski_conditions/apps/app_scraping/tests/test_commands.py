import os

import pytest
import responses
from django.core import management

from ..management.commands.do_scraping import KeystoneScraper, HeavenlyScraper, NorthstarScraper
from ..models import SkiResort


# pylint: disable=no-member
@responses.activate
@pytest.mark.django_db()
def test_scraping():
    assert SkiResort.objects.count() == 0

    body_Keystone = open(os.path.join(os.path.dirname(__file__), 'data', 'keystone.html'))
    responses.add(responses.GET, KeystoneScraper.url, status=200, body=body_Keystone.read())

    body_Heavenly = open(os.path.join(os.path.dirname(__file__), 'data', 'heavenly.html'))
    responses.add(responses.GET, HeavenlyScraper.url, status=200, body=body_Heavenly.read())

    body_Northstar = open(os.path.join(os.path.dirname(__file__), 'data', 'northstar.html'))
    responses.add(responses.GET, NorthstarScraper.url, status=200, body=body_Northstar.read())

    management.call_command('do_scraping')

    assert SkiResort.objects.count() == 3

    keystone = SkiResort.objects.get(resort_name='Keystone')
    assert keystone.acres_open == 230
    assert keystone.terrain_percent == 7
    assert keystone.trails_open == 13
    assert keystone.total_trails == 128
    assert keystone.lifts_open == 10
    assert keystone.total_lifts == 21

    heavenly = SkiResort.objects.get(resort_name='Heavenly')
    assert heavenly.acres_open == 22
    assert heavenly.terrain_percent == 0
    assert heavenly.trails_open == 4
    assert heavenly.total_trails == 97
    assert heavenly.lifts_open == 4
    assert heavenly.total_lifts == 28

    northstar = SkiResort.objects.get(resort_name='Northstar')
    assert northstar.acres_open == 0
    assert northstar.terrain_percent == 0
    assert northstar.trails_open == 0
    assert northstar.total_trails == 100
    assert northstar.lifts_open == 0
    assert northstar.total_lifts == 20

