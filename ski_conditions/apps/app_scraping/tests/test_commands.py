import os

import pytest
import responses
from django.core import management

from ..management.commands.do_scraping import KeystoneScraper
from ..models import SkiResort


# pylint: disable=no-member
@responses.activate
@pytest.mark.django_db()
def test_scraping():
    assert SkiResort.objects.count() == 0

    body = open(os.path.join(os.path.dirname(__file__), 'data', 'keystone.html'))
    responses.add(responses.GET, KeystoneScraper.url, status=200, body=body.read())

    management.call_command('do_scraping')

    assert SkiResort.objects.count() == 1

    keystone = SkiResort.objects.get(resort_name='Keystone')
    assert keystone.acres_open == 230
    assert keystone.terrain_percent == 7
    assert keystone.trails_open == 13
    assert keystone.total_trails == 128
    assert keystone.lifts_open == 10
    assert keystone.total_lifts == 21
